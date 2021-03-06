from os.path import isfile
from typing import Optional, Tuple

from tqdm import trange
from agents.TakPlayerAgent import TakPlayerAgent
from policies.EGreedyPolicy import EGreedyPolicy
from tak_env.TakAction import TakAction
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState

board_sizes = [3]
epsilons = [0.1]
gammas = [0.99]
alphas = [0.99]
episodes_options = [500, 1000]
starting_players = [TakPlayer.WHITE]
games = 30

trial_settings = []
for board_size in board_sizes:
    for eps in epsilons:
        for gamma in gammas:
            for alpha in alphas:
                for episodes in episodes_options:
                    for starting_player in starting_players:
                        trial_settings.append((board_size, eps, gamma, alpha, episodes, starting_player))

run_number = 1
path = f"./results/sarsa_player_run_{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/sarsa_player_run_{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "epsilon",
        "gamma",
        "alpha",
        "starting_player",
        "episode",
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player"
    ]) + "\n")

print(f"Will run {len(trial_settings)} configurations {games} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    last_board_size = 0
    for board_size, eps, gamma, alpha, episodes, starting_player in trial_settings:
        for game in range(games):

            # Init the environment
            with TakEnvironment(board_size=board_size) as env:
                # Init agents with no knowledge of the game
                sarsa_policy = EGreedyPolicy(board_size, eps, alpha, gamma)
                agent_white_player = TakPlayerAgent(
                    TakPlayer.WHITE, policy=sarsa_policy,
                    skip_possible_actions=True
                )
                agent_black_player = TakPlayerAgent(
                    TakPlayer.BLACK, policy=sarsa_policy,
                    skip_possible_actions=True
                )
                white_won = 0
                # Run the games
                for episode in trange(
                        episodes,
                        desc=f"B:{board_size}, ????={eps}, ????={gamma}, ????={alpha}, S:{starting_player}; E:{episodes}"
                ):
                    # Init the game
                    final_reward_for_first_player, final_reward_for_second_player = 0, 0
                    done = False
                    steps = 0
                    state = env.reset()

                    first_player_agent = agent_white_player if starting_player == TakPlayer.WHITE else agent_black_player
                    second_player_agent = agent_black_player if starting_player == TakPlayer.WHITE else agent_white_player

                    prev_step_first: Optional[Tuple[TakState, TakAction, float]] = None
                    prev_step_second: Optional[Tuple[TakState, TakAction, float]] = None

                    while not done:
                        # WHITE ACTION
                        action = first_player_agent.select_action(state.copy())
                        if prev_step_first is not None:  # update from prev step
                            prev_state, prev_action, prev_reward = prev_step_first
                            sarsa_policy.update(prev_state, prev_action, prev_reward, state, action)
                        next_state, reward, done, info = env.step(action)
                        prev_step_first = (state, action, reward)
                        state = next_state
                        steps += 1
                        if done:
                            if prev_step_first is not None:  # update from prev step
                                prev_state, prev_action, prev_reward = prev_step_first
                                sarsa_policy.update(prev_state, prev_action, prev_reward, state, action)
                            final_reward_for_first_player = reward
                            white_won += 1 if reward > 0 else 0
                            break

                        # BLACK ACTION
                        action = second_player_agent.select_action(state.copy())
                        if prev_step_second is not None:  # update from prev step
                            prev_state, prev_action, prev_reward = prev_step_second
                            sarsa_policy.update(prev_state, prev_action, prev_reward, state, action)
                        next_state, reward, done, info = env.step(action)
                        prev_step_first = (state, action, reward)
                        state = next_state
                        steps += 1
                        if done:
                            if prev_step_second is not None:  # update from prev step
                                prev_state, prev_action, prev_reward = prev_step_second
                                sarsa_policy.update(prev_state, prev_action, prev_reward, state, action)
                            final_reward_for_second_player = reward
                            white_won += 1 if reward < 0 else 0
                            break

                    final_reward_for_white_player = final_reward_for_first_player \
                        if starting_player == TakPlayer.WHITE else final_reward_for_second_player
                    final_reward_for_black_player = final_reward_for_second_player \
                        if starting_player == TakPlayer.WHITE else final_reward_for_first_player

                    results_file.writelines([
                        ",".join([
                            str(board_size),                            # board_size
                            str(eps),                                   # eps
                            str(gamma),                                 # gamma
                            str(alpha),                                 # alpha
                            str(starting_player),                       # starting_player
                            str(episode),                               # episode
                            str(game),                                  # game
                            str(steps),                                 # steps
                            str(int(final_reward_for_white_player)),    # reward_for_white_player
                            str(int(final_reward_for_black_player))     # reward_for_black_player
                        ]) + "\n"])
                results_file.flush()
                print(f"# White wins: {white_won}")

print("Done!")
