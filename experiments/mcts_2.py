from os.path import isfile

from tqdm import tqdm, trange

from agents.TakMCTSPlayerAgent import TakMCTSPlayerAgent, MCTSPlayerKnowledgeGraph
from agents.TakMCTSPlayerAgent2 import TakMCTSPlayerAgent2
from agents.TakPlannerPlayerAgent import TakPlannerPlayerAgent
from tak_env.TakBoard import TakBoard
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState

# board_sizes = [3, 4, 5]
# mcts_expansion_depths = [1, 3, 5]
# mcts_expansion_epsilons = [0.0, 0.1, 0.5, 0.9]
# mcts_iterations = [1, 3, 5, 10]
# rollout_runs = [1, 10, 25, 50, 100]
# games = 100

board_sizes = [3]
mcts_expansion_depths = [3]
mcts_expansion_epsilons = [1.0]
mcts_iterations = [5]
rollout_runs = [32]
games = 100

trial_settings = []
for board_size in board_sizes:
    for mcts_expansion_depth in mcts_expansion_depths:
        for mcts_expansion_e in mcts_expansion_epsilons:
            for mcts_iters in mcts_iterations:
                for rollout_run in rollout_runs:
                    trial_settings.append((board_size, mcts_expansion_depth, mcts_expansion_e, mcts_iters, rollout_run))

run_number = 1
path = f"./results/mcts2_run_{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/mcts2_run_{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "mcts_expansion_depth",
        "mcts_expansion_epsilon",
        "mcts_iterations",
        "rollout_runs",
        "trial_number",
        "steps",
        "reward_for_white_player",
        "reward_for_black_player",
        # "knowledge_graph_nodes",
        # "knowledge_graph_total_rollouts"
    ]) + "\n")

print(f"Will run {len(trial_settings)} configurations {games} times each.")
print(f"Output file: {path}")

with open(path, "a") as results_file:

    last_board_size = 0
    for board_size, mcts_expansion_depth, mcts_expansion_e, mcts_iters, rollout_run in trial_settings:
        # if last_board_size != board_size:
        #     # TakAction.wipe_cache()
        #     TakState.wipe_cache()
        #     TakBoard.wipe_cache()
        #     last_board_size = board_size

        # Init the environment
        with TakEnvironment(board_size=board_size) as env:
            game_knowledge_graph=MCTSPlayerKnowledgeGraph(env.reset())
            # Init agents with no knowledge of the game
            agent_white_player = TakMCTSPlayerAgent2(
                env.get_copy_at_state(env.reset()),
                TakPlayer.WHITE,
                game_knowledge_graph,
                mcts_expansion_depth=mcts_expansion_depth,
                mcts_expansion_epsilon=mcts_expansion_e,
                mcts_iterations=mcts_iters,
                rollout_runs=rollout_run
            )
            agent_black_player = TakMCTSPlayerAgent2(
                env.get_copy_at_state(env.reset()),
                TakPlayer.BLACK,
                game_knowledge_graph,
                mcts_expansion_depth=mcts_expansion_depth,
                mcts_expansion_epsilon=mcts_expansion_e,
                mcts_iterations=mcts_iters,
                rollout_runs=rollout_run
            )

            # Run the games
            for trial in trange(
                    games,
                    desc=f"Board: {board_size}; D={mcts_expansion_depth}, E={mcts_expansion_e}, I={mcts_iters}, R={rollout_run};"
            ):
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
                        white_won = reward > 0
                        break

                    # BLACK ACTION
                    action = agent_black_player.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_black_player = reward
                        white_won = reward < 0
                        break

                results_file.writelines([
                    ",".join([
                        str(board_size),                                # board_size
                        str(mcts_expansion_depth),                      # mcts_expansion_depth
                        str(mcts_expansion_e),                          # mcts_expansion_epsilon
                        str(mcts_iters),                                # mcts_iterations
                        str(rollout_run),                               # rollout_runs
                        str(trial),                                     # trial_number
                        str(steps),                                     # steps
                        str(int(final_reward_for_white_player)),        # reward_for_white_player
                        str(int(final_reward_for_black_player)),        # reward_for_black_player
                        # str(game_knowledge_graph.total_nodes()),        # knowledge_graph_nodes
                        # str(game_knowledge_graph.total_rollouts())      # knowledge_graph_total_rollouts
                    ]) + "\n"])
            results_file.flush()

print("Done!")
