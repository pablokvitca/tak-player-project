from typing import List

from tak_env.TakAction import TakAction


class Policy:

    def select_action(self, possible_actions: List[TakAction]) -> TakAction:
        raise NotImplementedError("The 'selection_action' method is not implemented.")