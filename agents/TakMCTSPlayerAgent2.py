from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Tuple, Union, Set, List

import numpy as np
from igraph import Graph, Vertex

from agents.TakMCTSPlayerAgent import MCTSPlayerKnowledgeGraph
from agents.TakPlayerAgent import TakPlayerAgent
from policies.Policy import Policy
from policies.RandomPolicy import RandomPolicy
from policies.RandomPolicyEff import RandomPolicyEff
from tak_env.TakAction import TakAction, TakActionPlace
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TakMCTSPlayerAgent2(TakPlayerAgent):

    max_parallel_rollouts_threads: int = 16

    @classmethod
    def default_rollout_policy(cls, board_size: int = 19) -> Policy:
        return RandomPolicyEff(board_size)

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
            parallel_rollouts: bool = True,
    ):
        super().__init__(player)
        self.env: TakEnvironment = env
        self.player: TakPlayer = player
        self.graph: MCTSPlayerKnowledgeGraph = graph
        self.rollout_policy: Policy = rollout_policy or TakMCTSPlayerAgent2.default_rollout_policy(env.board_size)
        self.mcts_expansion_depth: int = mcts_expansion_depth
        self.mcts_expansion_epsilon: float = mcts_expansion_epsilon
        self.mcts_iterations: int = mcts_iterations
        self.rollout_runs: int = rollout_runs
        self.parallel_rollouts: bool = parallel_rollouts if self.rollout_runs > 1 else False
        self.parallel_rollouts_threads = max(self.rollout_runs, self.__class__.max_parallel_rollouts_threads)

        self.first_actions = {
            TakPlayer.WHITE: TakAction.get_first_actions(self.env.board_size, TakPlayer.WHITE),
            TakPlayer.BLACK: TakAction.get_first_actions(self.env.board_size, TakPlayer.BLACK)
        }
        self.all_actions = TakAction.get_all_actions(self.env.board_size)

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
        possible_actions, weights = self.get_actions_and_weights(root_node['state'])
        return np.random.choice(possible_actions, p=weights)

    def expand(self, state: TakState) -> TakState:
        current_state, was_in_graph, depth = state, self.graph.state_in_graph(state), 0
        while not current_state.is_terminal()[0] and (was_in_graph or depth < self.mcts_expansion_depth):
            depth += 1  # Increment expanded depth

            # EXPLORE?
            if np.random.rand() < self.mcts_expansion_epsilon:
                actions, weights = self.get_actions_and_weights(current_state)
                action = np.random.choice(actions, p=weights)
            else:  # Greedy
                action = self.get_best_action(self.graph.get_state_node(current_state))

            next_state = action.take(current_state, mutate=False)
            was_in_graph = self.graph.state_in_graph(next_state)
            if not was_in_graph:
                self.graph.add_state(current_state, next_state, action)
            current_state = next_state
        return current_state

    def rollout(self, leaf: TakState) -> List[float]:
        if self.parallel_rollouts:
            return self._rollout_parallel(leaf)
        else:
            return [self._rollout_single(leaf) for _ in range(self.rollout_runs)]

    def _rollout_single(self, leaf: TakState) -> float:
        env = self.env.get_copy_at_state(leaf)
        done, info = leaf.is_terminal()
        state, reward = leaf, 0.0 if not done else self._compute_score_for_terminal_state(leaf, info)
        while not done:
            possible_actions = TakAction.get_possible_actions(state)
            action = self.rollout_policy.select_action(state, possible_actions)
            next_state, reward, done, info = env.step(action)
            state = next_state
        return abs(reward) * (1.0 if info['winning_player'] == self.player else -1.0)

    def _rollout_parallel(self, leaf: TakState, threads: int = 10) -> List[float]:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self._rollout_single, leaf) for _ in range(self.rollout_runs)]
            return [future.result() for future in futures]

    def _compute_score_for_terminal_state(self, state: TakState, info) -> float:
        current_player = state.current_player.other()
        winning_player = info["winning_player"]
        return self.env.compute_score(current_player, winning_player, discount=True)

    def backup(self, expansion_end_state: TakState, rewards: List[float]) -> None:
        for reward in rewards:
            self.graph.add_visit(expansion_end_state, reward, backpropagate=True)

    def get_actions_and_weights(
            self,
            current_state: TakState,
            place_action_prob: float = 0.5
    ) -> Tuple[List[TakAction], np.ndarray]:
        actions = self.all_actions if not current_state.first_action() \
            else self.first_actions[current_state.current_player]

        weights = np.zeros(len(actions))
        valid_place_actions, valid_move_actions = [], []
        for i, action in enumerate(actions):
            # is valid?
            if action.is_valid(current_state):
                if isinstance(action, TakActionPlace):
                    valid_place_actions.append(i)
                else:
                    valid_move_actions.append(i)
            else:
                weights[i] = 0

        if len(valid_move_actions) == 0:
            place_action_prob = 1.0
        if len(valid_place_actions) > 0:
            single_place_action_prob = place_action_prob / len(valid_place_actions)
            for i in valid_place_actions:
                weights[i] = single_place_action_prob

        if len(valid_place_actions) == 0:
            place_action_prob = 0.0
        if len(valid_move_actions) > 0:
            single_move_action_prob = (1 - place_action_prob) / len(valid_move_actions)
            for i in valid_move_actions:
                weights[i] = single_move_action_prob

        return actions, weights

    def add_adv_action(self, state, action, next_state, _):
        self.graph.add_state(state, next_state, action)
