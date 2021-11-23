from os.path import isfile

from tqdm import tqdm, trange
from agents.TakPlannerPlayerAgent import TakPlannerPlayerAgent
from tak_env.TakBoard import TakBoard
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState

board_sizes = [3, 4, 5]
action_selection_percents = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
rollout_runs = [1, 2, 5, 10, 25, 50, 100]
games = 100

trial_settings = []
for board_size in board_sizes:
    for action_selection_percent in action_selection_percent:
        for rollout_run in rollout_runs:
            trial_settings.append((board_size, action_selection_percent, rollout_run))

run_number = 1
path = f"./results/mcts_run_{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/mcts_run_{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "action_selection_percent",
        "rollout_runs"
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player",
        "knowledge_graph_nodes",
        "knowledge_graph_total_rollouts"
    ]) + "\n")

print(f"Will run {len(trial_settings)} configurations {games} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    last_board_size = 0
    for board_size, action_selection_percent, rollout_run in trial_settings:
        print(f"RUN: Board: {board_size}; Expanding {action_selection_percent:.2f}% of actions, {rollout_run} times")
        if last_board_size != board_size:
            # TakAction.wipe_cache()
            TakState.wipe_cache()
            TakBoard.wipe_cache()
            last_board_size = board_size

        # Init agents with no knowledge of the game
        game_knowledge_graph = MCTSPlayerKnowledgeGraph()
        agent_white_player = TakMCTSPlayerAgent(TakPlayer.WHITE, game_knowledge_graph=game_knowledge_graph)
        agent_black_player = TakMCTSPlayerAgent(TakPlayer.BLACK, game_knowledge_graph=game_knowledge_graph)

        # Init the environment
        with TakEnvironment(board_size=board_size) as env:

            # Run the games
            for trial in trange(games):
                # Init the game
                final_reward_for_white_player, final_reward_for_black_player = 0, 0
                done = False
                steps = 0
                state = env.reset()

                while not done:
                    # WHITE ACTION
                    action = agent_white_player.select_action(state)
                    state, reward, done, info = env.step(action)
                    steps += 1
                    if done:
                        final_reward_for_white_player = reward
                        white_won = reward > 0
                        break

                    # BLACK ACTION
                    action = agent_black_player.select_action(state)
                    state, reward, done, info = env.step(action)
                    steps += 1
                    if done:
                        final_reward_for_black_player = reward
                        white_won = reward < 0
                        break

                results_file.writelines([
                    ",".join([
                        str(board_size),                                # board_size
                        str(action_selection_percent),                  # action_selection_percent
                        str(rollout_run),                               # rollout_runs
                        str(trial),                                     # trial_number
                        str(steps),                                     # steps
                        str(int(final_reward_for_white_player)),        # reward_for_white_player
                        str(int(final_reward_for_black_player)),        # reward_for_black_player
                        str(game_knowledge_graph.total_nodes()),        # knowledge_graph_nodes
                        str(game_knowledge_graph.total_rollouts())      # knowledge_graph_total_rollouts
                    ]) + "\n"])
            results_file.flush()

print("Done!")
