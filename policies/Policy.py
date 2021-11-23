from typing import List

from tak_env.TakAction import TakAction
from tak_env.TakState import TakState


class Policy:

    def select_action(self, state: TakState, possible_actions: List[TakAction]) -> TakAction:
        raise NotImplementedError("The 'selection_action' method is not implemented.")
