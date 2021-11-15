from typing import List

import numpy as np

from tak_env.TakAction import TakAction, TakActionMove, TakActionPlace


class Policy:

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        raise NotImplementedError("The 'selection_action' method is not implemented.")


class RandomPolicy(Policy):

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        return np.random.choice(possible_actions)


class RandomPolicyLessLikelyPlace(Policy):
    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        select_move = np.random.choice([True, False])
        if select_move:
            move_actions = [action for action in possible_actions if isinstance(action, TakActionMove)]
            return np.random.choice(move_actions if len(move_actions) > 0 else possible_actions)
        else:
            place_actions = [action for action in possible_actions if isinstance(action, TakActionPlace)]
            return np.random.choice(place_actions)
