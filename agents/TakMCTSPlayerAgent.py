from typing import Optional, Tuple, Union, Set, List

import numpy as np
from igraph import Graph, Vertex

from agents.TakPlayerAgent import TakPlayerAgent
from policies.Policy import Policy
from policies.RandomPolicy import RandomPolicy
from tak_env.TakAction import TakAction
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


# NOTE: consider using only board as the elements of the MCTS graph

class MCTSPlayerKnowledgeGraph(object):

    def __init__(self, initial_state: TakState):
        self.g = Graph(directed=True)
        self.initial_state_node_id = self._add_state(initial_state)

    def get_root(self) -> Tuple[TakState, float, int]:
        return self.g.vs[self.initial_state_node_id]

    def state_in_graph(self, state: TakState) -> bool:
        return state in self.g.vs['state']

    def state_node_id(self, state: TakState) -> Optional[int]:
        return self.g.vs.find(state=state).index if self.state_in_graph(state) else None

    def _add_state(self, state: TakState) -> int:
        node = self.g.add_vertex(state=state, visits=0, sum_reward=0)
        return node.index

    def add_state(self, parent: Union[int, TakState], state: TakState, action: TakAction) -> int:
        parent_node_id = parent if isinstance(parent, int) else self.state_node_id(parent)
        state_node_id = self.state_node_id(state) or self._add_state(state)
        self.g.add_edge(parent_node_id, state_node_id, action=action)
        return state_node_id

    def add_action_result(self, parent: TakState, action: TakAction) -> int:
        return self.add_state(parent, action.take(parent, mutate=False), action)

    def add_visit(self, state: Union[int, TakState], reward: float, backpropagate: bool = True) -> None:
        state_node_id = state if isinstance(state, int) else self.state_node_id(state)
        self.g.vs[state_node_id]['visits'] += 1
        self.g.vs[state_node_id]['sum_reward'] += reward
        if backpropagate:
            self._backpropagate_visit(state_node_id, reward, set())

    def _backpropagate_visit(self, state_id: int, reward: float, visited: Set[int]) -> None:
        for edge_index in self.g.incident(state_id, mode='IN'):
            parent_index = self.g.es[edge_index].source
            if parent_index not in visited:
                visited.add(parent_index)
                self.add_visit(parent_index, reward, False)
                self._backpropagate_visit(parent_index, reward, visited)

    def get_state_node(self, state: TakState) -> Optional[Vertex]:
        return self.g.vs.find(state=state) if self.state_in_graph(state) else None

    def get_state_value(self, state: Union[int, TakState]) -> float:
        state_node_id = state if isinstance(state, int) else self.state_node_id(state)
        if state_node_id is not None:
            return self.g.vs[state_node_id]['sum_reward'] / max(1, self.g.vs[state_node_id]['visits'])
        else:
            return 0.0

    def total_nodes(self) -> int:
        return len(self.g.vs)

    def total_rollouts(self):
        return sum(self.g.vs['visits'])


class TakMCTSPlayerAgent(TakPlayerAgent):

    @classmethod
    def default_rollout_policy(cls):
        return RandomPolicy()

    def __init__(
            self,
            env: TakEnvironment,
            player: TakPlayer,
            graph: MCTSPlayerKnowledgeGraph,
            rollout_policy: Optional[Policy] = None,
            mcts_expansion_depth: int = 3,
            mcts_expansion_epsilon: float = 0.5,
            mcts_iterations: int = 10,
            rollout_runs: int = 10,
            parallel_rollouts: bool = False,
    ):
        super().__init__(player)
        self.env = env
        self.player = player
        self.graph = graph
        self.rollout_policy = TakMCTSPlayerAgent.default_rollout_policy() if rollout_policy is None else rollout_policy
        self.mcts_expansion_depth = mcts_expansion_depth
        self.mcts_expansion_epsilon = mcts_expansion_epsilon
        self.mcts_iterations = mcts_iterations
        self.rollout_runs = rollout_runs
        self.parallel_rollouts = parallel_rollouts

    def select_action(self, state: TakState) -> TakAction:
        # SELECTION?
        state = state.copy()
        root_node = self.graph.get_state_node(state)
        for i in range(self.mcts_iterations):
            # EXPANSION
            expansion_leaf_state = self.expand(state)

            # SIMULATION
            rewards = self.rollout(expansion_leaf_state)

            # BACKUP
            self.backup(expansion_leaf_state, rewards)
        return self.get_best_action(root_node)

    def get_best_black_action(self, root_node: Vertex) -> Optional[TakAction]:
        best_action_value = float('inf')
        best_action = None
        for out_edge in root_node.out_edges():
            if out_edge['action']:
                action_value = self.graph.get_state_value(out_edge.target)
                if action_value < best_action_value:
                    best_action_value = action_value
                    best_action = out_edge['action']
        return best_action

    def get_best_white_action(self, root_node: Vertex) -> Optional[TakAction]:
        best_action_value = -float('inf')
        best_action = None
        for out_edge in root_node.out_edges():
            if out_edge['action']:
                action_value = self.graph.get_state_value(out_edge.target)
                if action_value > best_action_value:
                    best_action_value = action_value
                    best_action = out_edge['action']
        return best_action

    def get_best_action(self, root_node: Vertex) -> Optional[TakAction]:
        best_action = self.get_best_white_action(root_node) if self.player == TakPlayer.WHITE \
            else self.get_best_black_action(root_node)
        if best_action is not None:
            return best_action
        possible_actions = TakAction.get_possible_actions(root_node['state'])
        return np.random.choice(possible_actions)

    def expand(self, state: TakState) -> TakState:
        current_state, was_in_graph, depth = state, self.graph.state_in_graph(state), 0
        while not current_state.is_terminal()[0] and (was_in_graph or depth < self.mcts_expansion_depth):
            depth += 1  # Increment expanded depth

            # EXPLORE?
            if np.random.rand() < self.mcts_expansion_epsilon:
                possible_actions = TakAction.get_possible_actions(current_state)
                action = np.random.choice(possible_actions)
            else:  # Greedy
                action = self.get_best_action(self.graph.get_state_node(current_state))

            next_state = action.take(current_state, mutate=False)
            was_in_graph = self.graph.state_in_graph(next_state)
            if not was_in_graph:
                self.graph.add_state(current_state, next_state, action)
            current_state = next_state
        return current_state

    def rollout(self, leaf: TakState) -> List[float]:
        # TODO: parallelize
        rewards = [0] * self.rollout_runs
        for i in range(self.rollout_runs):
            env = self.env.get_copy_at_state(leaf)
            done, info = leaf.is_terminal()
            state, reward = leaf, 0.0 if not done else self._compute_score_for_terminal_state(leaf, info)
            while not done:
                possible_actions = TakAction.get_possible_actions(state)
                action = self.rollout_policy.select_action(state, possible_actions)
                next_state, reward, done, info = env.step(action)
                state = next_state
            rewards[i] = abs(reward) * (1.0 if info['winning_player'] == self.player else -1.0)
        return rewards

    def _compute_score_for_terminal_state(self, state: TakState, info) -> float:
        current_player = state.current_player.other()
        winning_player = info["winning_player"]
        return self.env.compute_score(current_player, winning_player, discount=True)

    def backup(self, expansion_end_state: TakState, rewards: List[float]) -> None:
        for reward in rewards:
            self.graph.add_visit(expansion_end_state, reward, backpropagate=True)


