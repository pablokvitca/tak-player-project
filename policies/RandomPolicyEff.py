from typing import List, Tuple

import numpy as np

from policies.Policy import Policy
from tak_env.TakAction import TakAction, TakActionPlace
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class RandomPolicyEff(Policy):

    def __init__(self, board_size: int):
        self.first_actions = {
            TakPlayer.WHITE: TakAction.get_first_actions(board_size, TakPlayer.WHITE),
            TakPlayer.BLACK: TakAction.get_first_actions(board_size, TakPlayer.BLACK)
        }
        self.all_actions = TakAction.get_all_actions(board_size)

    def select_action(self, state: TakState, _: List[TakAction]) -> TakAction:
        actions, weights = self.get_actions_and_weights(state)
        return np.random.choice(actions, p=weights)

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
