from policies.RandomPolicy import RandomPolicy
from policies.Policy import Policy
from tak_env.TakAction import TakAction
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TakSARSAPlayerAgent(object):

    def __init__(self, player: TakPlayer, policy: Policy = RandomPolicy(), skip_possible_actions: bool = False):
        self.player = player
        self.policy = policy
        self.skip_possible_actions = skip_possible_actions

    def select_action(self, state: TakState) -> TakAction:
        possible_actions = [] if self.skip_possible_actions else TakAction.get_possible_actions(state)
        return self.policy.select_action(state, possible_actions)
