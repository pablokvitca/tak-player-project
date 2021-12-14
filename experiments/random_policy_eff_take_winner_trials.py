from os.path import isfile
from tqdm import trange
from agents.TakPlayerAgent import TakPlayerAgent
from policies.RandomPolicyEff import RandomPolicyEff
from policies.RandomPolicyEffTakeWinner import RandomPolicyEffTakeWinner
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer

# board_sizes = [3, 4, 5]
# starting_player = [TakPlayer.WHITE, TakPlayer.BLACK]
board_sizes = [5]
starting_player = [TakPlayer.BLACK]
games = 300

trial_settings = []
for board_size in board_sizes:
    for player in starting_player:
        trial_settings.append((board_size, player))

run_number = 1
path = f"./results/random_eff_run_takewin_{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/random_eff_run_takewin_{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "starting_player",
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player"
    ]) + "\n")

print(f"Will run {len(trial_settings)} configurations {games} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    last_board_size = 0
    for board_size, starting_player in trial_settings:
        white_won = 0
        # Init the environment
        with TakEnvironment(board_size=board_size) as env:
            # Init agents with no knowledge of the game
            agent_white_player = TakPlayerAgent(
                TakPlayer.WHITE, policy=RandomPolicyEffTakeWinner(board_size),
                skip_possible_actions=True
            )
            agent_black_player = TakPlayerAgent(
                TakPlayer.BLACK, policy=RandomPolicyEffTakeWinner(board_size),
                skip_possible_actions=True
            )

            # Run the games
            for trial in trange(games, desc=f"Board: {board_size};"):
                # Init the game
                final_reward_for_first_player, final_reward_for_second_player = 0, 0
                done = False
                steps = 0
                state = env.reset()

                first_player_agent = agent_white_player if starting_player == TakPlayer.WHITE else agent_black_player
                second_player_agent = agent_black_player if starting_player == TakPlayer.WHITE else agent_white_player

                while not done:
                    # WHITE ACTION
                    action = first_player_agent.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_first_player = reward
                        white_won += 1 if reward > 0 else 0
                        break

                    # BLACK ACTION
                    action = second_player_agent.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_second_player = reward
                        white_won += 1 if reward < 0 else 0
                        break

                final_reward_for_white_player = final_reward_for_first_player if starting_player == TakPlayer.WHITE else final_reward_for_second_player
                final_reward_for_black_player = final_reward_for_second_player if starting_player == TakPlayer.WHITE else final_reward_for_first_player

                results_file.writelines([
                    ",".join([
                        str(board_size),                            # board_size
                        str(starting_player),                       # starting_player
                        str(trial),                                 # trial_number
                        str(steps),                                 # steps
                        str(int(final_reward_for_white_player)),    # reward_for_white_player
                        str(int(final_reward_for_black_player))     # reward_for_black_player
                    ]) + "\n"])
            results_file.flush()
        print(f"# White wins: {white_won}")

print("Done!")
