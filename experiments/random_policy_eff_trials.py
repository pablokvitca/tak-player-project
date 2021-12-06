from os.path import isfile

from tqdm import tqdm, trange

from agents.TakMCTSPlayerAgent import TakMCTSPlayerAgent, MCTSPlayerKnowledgeGraph
from agents.TakPlannerPlayerAgent import TakPlannerPlayerAgent
from agents.TakPlayerAgent import TakPlayerAgent
from policies.RandomPolicyEff import RandomPolicyEff
from tak_env.TakBoard import TakBoard
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState

board_sizes = [3, 4, 5]
epsilons = [1.0]
games = 10000

trial_settings = []
for board_size in board_sizes:
    for eps in epsilons:
        trial_settings.append((board_size, eps))

run_number = 1
path = f"./results/random_eff_run_{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/random_eff_run_{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "epsilon",
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player"
    ]) + "\n")

print(f"Will run {len(trial_settings)} configurations {games} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    last_board_size = 0
    for board_size, eps in trial_settings:
        white_won = 0
        # Init the environment
        with TakEnvironment(board_size=board_size) as env:
            # Init agents with no knowledge of the game
            agent_white_player = TakPlayerAgent(TakPlayer.WHITE, policy=RandomPolicyEff(board_size))
            agent_black_player = TakPlayerAgent(TakPlayer.BLACK, policy=RandomPolicyEff(board_size))

            # Run the games
            for trial in trange(games, desc=f"Board: {board_size}; E={eps}"):
                # Init the game
                final_reward_for_white_player, final_reward_for_black_player = 0, 0
                done = False
                steps = 0
                state = env.reset()

                while not done:
                    # WHITE ACTION
                    action = agent_white_player.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_white_player = reward
                        white_won += 1 if reward > 0 else 0
                        break

                    # BLACK ACTION
                    action = agent_black_player.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_black_player = reward
                        white_won += 1 if reward < 0 else 0
                        break

                results_file.writelines([
                    ",".join([
                        str(board_size),                            # board_size
                        str(eps),                                   # eps
                        str(trial),                                 # trial_number
                        str(steps),                                 # steps
                        str(int(final_reward_for_white_player)),    # reward_for_white_player
                        str(int(final_reward_for_black_player))     # reward_for_black_player
                    ]) + "\n"])
            results_file.flush()
        print(f"# White wins: {white_won}")

print("Done!")
