from typing import List

import numpy as np

from tak_env.TakAction import TakAction


class Policy:

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        raise NotImplementedError("The 'selection_action' method is not implemented.")


class RandomPolicy(Policy):

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        return np.random.choice(possible_actions)
