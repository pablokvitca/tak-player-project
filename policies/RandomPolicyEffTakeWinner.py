from typing import List, Tuple

import numpy as np

from policies.Policy import Policy
from tak_env.TakAction import TakAction, TakActionPlace
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class RandomPolicyEffTakeWinner(Policy):

    def __init__(self, board_size: int, place_action_prob: float = 0.5):
        self.first_actions = {
            TakPlayer.WHITE: TakAction.get_first_actions(board_size, TakPlayer.WHITE),
            TakPlayer.BLACK: TakAction.get_first_actions(board_size, TakPlayer.BLACK)
        }
        self.all_actions = TakAction.get_all_actions(board_size)
        self.place_action_prob = place_action_prob

    def select_action(self, state: TakState, _: List[TakAction] = None) -> TakAction:
        actions, weights = self.get_actions_and_weights(state)
        return np.random.choice(actions, p=weights)

    def get_actions_and_weights(
            self,
            current_state: TakState,
    ) -> Tuple[List[TakAction], np.ndarray]:
        place_action_prob = self.place_action_prob
        actions = self.all_actions if not current_state.first_action() \
            else self.first_actions[current_state.current_player]

        weights = np.zeros(len(actions))
        valid_place_actions, valid_move_actions = [], []
        winning_actions = []
        losing_actions = []
        for i, action in enumerate(actions):
            # is valid?
            if action.is_valid(current_state):
                if isinstance(action, TakActionPlace):
                    valid_place_actions.append(i)
                else:
                    valid_move_actions.append(i)
                # is winning?
                next_state = action.take(current_state, mutate=False)
                if next_state.is_terminal():
                    if next_state.winning_player() == current_state.current_player:
                        winning_actions.append(action)
                    else:
                        losing_actions.append(action)
                        weights[i] = 0
            else:
                weights[i] = 0

        if len(winning_actions) > 0:
            return winning_actions, np.ones(len(winning_actions)) / len(winning_actions)

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

    def update(self, state, action, reward, next_state, next_action):
        pass