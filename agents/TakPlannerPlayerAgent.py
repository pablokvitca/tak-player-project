from agents.TakPlayerAgent import TakPlayerAgent
from policies.MinMaxPolicy import MinMaxPolicy
from policies.Policy import Policy
from tak_env.TakAction import TakAction
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TakPlannerPlayerAgent(TakPlayerAgent):

    @staticmethod
    def default_policy() -> Policy:
        return MinMaxPolicy(depth=3)

    def __init__(self, player: TakPlayer, policy: Policy = None):
        super().__init__(player)
        self.player = player
        self.policy = policy if policy is not None else TakPlannerPlayerAgent.default_policy()

    def select_action(self, state: TakState) -> TakAction:
        return self.policy.select_action(state, TakAction.get_possible_actions(state))

