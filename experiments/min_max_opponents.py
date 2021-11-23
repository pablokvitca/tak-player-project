from os.path import isfile

from tqdm import tqdm
from agents.TakPlannerPlayerAgent import TakPlannerPlayerAgent
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer

board_sizes = [3, 4, 5]
min_max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

trials = 100

board_settings = []
for board_size in board_sizes:
    for min_max_depth in min_max_depths:
        for trial in range(trials):
            board_settings.append((board_size, min_max_depth, trial))

run_number = 1
path = f"./results/min_max_opponents_run_{run_number}.csv"
while isfile(path):
    run_number = 1
    path = f"./results/min_max_opponents_run_{run_number}.csv"

with open(path, "w") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "min_max_depth",
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player"
    ]) + "\n")

print(f"Will run {len(board_settings)} configurations {trials} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    pbar = tqdm(board_settings)
    done = False
    for board_size, min_max_depth, trial in pbar:
        pbar.set_description(
            desc=f"Board Size: {board_size}x{board_size}. MinMaxDepth: {min_max_depth}. Last Result: {done}"
        )

        with TakEnvironment(board_size=board_size) as env:

            final_reward_for_white_player = 0
            final_reward_for_black_player = 0

            agent_white_player = TakPlannerPlayerAgent(TakPlayer.WHITE)
            agent_black_player = TakPlannerPlayerAgent(TakPlayer.BLACK)

            state = env.reset()
            done = False
            steps = 0

            while not done:
                action = agent_white_player.select_action(state)
                state, reward, done, info = env.step(action)
                steps += 1
                if done:
                    final_reward_for_white_player = reward
                    break

                action = agent_black_player.select_action(state)
                state, reward, done, info = env.step(action)
                steps += 1
                if done:
                    final_reward_for_black_player = reward
                    break

            results_file.writelines([
                ",".join([
                    board_size,                     # board_size
                    min_max_depth,                  # min_max_depth
                    trial,                          # trial_number
                    steps,                          # steps
                    final_reward_for_white_player,  # reward_for_white_player
                    final_reward_for_black_player   # reward_for_black_player
                ]) + "\n"])
            results_file.flush()

print("Done!")
