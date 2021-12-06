from policies.RandomPolicy import RandomPolicy
from policies.Policy import Policy
from tak_env.TakAction import TakAction
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TakPlayerAgent(object):

    def __init__(self, player: TakPlayer, policy: Policy = RandomPolicy()):
        self.player = player
        self.policy = policy

    def select_action(self, state: TakState) -> TakAction:
        return self.policy.select_action(state, TakAction.get_possible_actions(state))
