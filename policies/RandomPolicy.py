from typing import List

import numpy as np

from policies.Policy import Policy
from tak_env.TakAction import TakAction


class RandomPolicy(Policy):

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        return np.random.choice(possible_actions)