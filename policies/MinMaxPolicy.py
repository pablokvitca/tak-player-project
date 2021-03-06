from typing import List, Optional

import numpy as np

from policies.Policy import Policy
from tak_env.TakAction import TakAction
from tak_env.TakScorer import TakScorerDefault
from tak_env.TakState import TakState


class MinMaxPolicy(Policy):

    def __init__(self, depth: int):
        self.depth = depth
        self.scorer = TakScorerDefault()

    def select_action(self, state: TakState, possible_actions: List[TakAction]) -> TakAction:
        """
        Selects an action from the given state using the MinMax algorithm.
        :param state: the state to select an action from
        :param possible_actions: the possible actions to select from
        :return: the selected action
        """

        possible_action_values = [self._evaluate_action_max(state, a, self.depth) for a in possible_actions]
        return MinMaxPolicy.argmax_action(possible_actions, possible_action_values)

    @staticmethod
    def argmax_action(actions: List[TakAction], values: List[float]) -> TakAction:
        action_values = np.array(values)
        indexes_with_max_value = np.where(action_values == np.max(action_values))[0]
        return actions[np.random.choice(indexes_with_max_value)]

    def _evaluate_action_max(self, state: TakState, action: TakAction, depth: Optional[int] = None) -> float:
        """
        Evaluates the value of taking the given action from the given state
        :param state: the current state to expand actions from
        :param action: the action to take
        :param depth: the depth to expand to
        :return: the value of the action
        """
        next_state = action.take(state, mutate=False)
        if depth == 0 or next_state.is_terminal()[0]:
            return self.state_evaluator(state)

        next_depth = (self.depth if depth is None else depth) - 1
        next_actions = TakAction.get_possible_actions(next_state)
        next_action_values = [self._evaluate_action_min(next_state, a, next_depth) for a in next_actions]
        return np.max(np.array(next_action_values))

    def _evaluate_action_min(self, state: TakState, action: TakAction, depth: Optional[int] = None) -> float:
        """
        Evaluates the value of taking the given action from the given state
        :param state: the current state to expand actions from
        :param action: the action to take
        :param depth: the depth to expand to
        :return: the value of the action
        """
        next_state = action.take(state, mutate=False)
        if depth == 0 or next_state.is_terminal()[0]:
            return self.state_evaluator(state)

        next_depth = (self.depth if depth is None else depth) - 1
        next_actions = TakAction.get_possible_actions(next_state)
        next_action_values = [self._evaluate_action_max(next_state, a, next_depth) for a in next_actions]
        return np.min(np.array(next_action_values))

    def state_evaluator(self, state: TakState) -> float:
        """
        The simple evaluator returns 0 on non-terminal states. In the terminal state it returns +/- the score of the
        winning player in the terminal state. If the winning player is the last player to move, the score is positive,
        otherwise it is negative.
        NOTE: can be overridden to use a different evaluator.

        :param state: the state to evaluate
        :return: the value of the state
        """

        done, info = state.is_terminal()
        if done:
            current_player = state.current_player
            last_player_move = state.current_player.other()
            winning_player = info['winning_player']
            multiplier = 1 if last_player_move == winning_player else -1
            return multiplier * abs(self.scorer.score(state, current_player, winning_player, discount=True))
        return 0.0

