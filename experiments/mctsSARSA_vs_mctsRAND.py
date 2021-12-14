from os.path import isfile

from tqdm import tqdm, trange

from agents.TakMCTSPlayerAgent import TakMCTSPlayerAgent, MCTSPlayerKnowledgeGraph
from agents.TakMCTSPlayerAgent2 import TakMCTSPlayerAgent2
from agents.TakPlannerPlayerAgent import TakPlannerPlayerAgent
from policies.EGreedyPolicy import EGreedyPolicy
from policies.RandomPolicyEffTakeWinner import RandomPolicyEffTakeWinner
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
mcts_expansion_epsilons = [0.9]
mcts_iterations = [3]
rollout_runs = [16]
starting_players = [TakPlayer.WHITE]
sarsa_epsilons = [0.1]
sarsa_alphas = [0.99]
sarsa_gammas = [0.99]
games = 50


def make_policy(board_size, policy_name, epsilon, alpha, gamma):
    if policy_name == 'egreedy-sarsa':
        return EGreedyPolicy(board_size, epsilon, alpha, gamma)
    elif policy_name == 'random':
        return None
    elif policy_name == 'random_take_win':
        return RandomPolicyEffTakeWinner(board_size)


trial_settings = []
for board_size in board_sizes:
    for mcts_expansion_depth in mcts_expansion_depths:
        for mcts_expansion_e in mcts_expansion_epsilons:
            for mcts_iters in mcts_iterations:
                for rollout_run in rollout_runs:
                    for starting_player in starting_players:
                        for sarsa_epsilon in sarsa_epsilons:
                            for sarsa_alpha in sarsa_alphas:
                                for sarsa_gamma in sarsa_gammas:
                                    trial_settings.append((
                                        board_size,
                                        mcts_expansion_depth,
                                        mcts_expansion_e,
                                        mcts_iters,
                                        rollout_run,
                                        starting_player,
                                        sarsa_epsilon,
                                        sarsa_alpha,
                                        sarsa_gamma
                                    ))

run_number = 1
path = f"./results/mcts_with_sarsa_vs_mcts_rand_run{run_number}.csv"
while isfile(path):
    run_number += 1
    path = f"./results/mcts_with_sarsa_vs_mcts_rand_run{run_number}.csv"

with open(path, "w+") as results_file:
    results_file.writelines(",".join([
        "board_size",
        "mcts_expansion_depth",
        "mcts_expansion_epsilon",
        "mcts_iterations",
        "rollout_runs",
        "starting_player",
        "sarsa_epsilon",
        "sarsa_alpha",
        "sarsa_gamma",
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
    for board_size, mcts_expansion_depth, mcts_expansion_e, mcts_iters, rollout_run, starting_player, \
            sarsa_epsilon, sarsa_alpha, sarsa_gamma in trial_settings:
        # if last_board_size != board_size:
        #     # TakAction.wipe_cache()
        #     TakState.wipe_cache()
        #     TakBoard.wipe_cache()
        #     last_board_size = board_size

        # Init the environment
        with TakEnvironment(board_size=board_size, init_player=starting_player) as env:
            game_knowledge_graph = MCTSPlayerKnowledgeGraph(env.reset())
            # Init agents with no knowledge of the game
            agent_white_policy = make_policy(board_size, "egreedy-sarsa", sarsa_epsilon, sarsa_alpha, sarsa_gamma)
            agent_white_player = TakMCTSPlayerAgent2(
                env.get_copy_at_state(env.reset()),
                TakPlayer.WHITE,
                game_knowledge_graph,
                mcts_expansion_depth=mcts_expansion_depth,
                mcts_expansion_epsilon=mcts_expansion_e,
                mcts_iterations=mcts_iters,
                rollout_runs=rollout_run,
                rollout_policy=agent_white_policy
            )
            agent_black_policy = make_policy(board_size, "random_take_win", sarsa_epsilon, sarsa_alpha, sarsa_gamma)
            agent_black_player = TakMCTSPlayerAgent2(
                env.get_copy_at_state(env.reset()),
                TakPlayer.BLACK,
                game_knowledge_graph,
                mcts_expansion_depth=mcts_expansion_depth,
                mcts_expansion_epsilon=mcts_expansion_e,
                mcts_iterations=mcts_iters,
                rollout_runs=rollout_run,
                rollout_policy=agent_black_policy
            )

            # Run the games
            for trial in trange(
                    games,
                    desc=f"Board: {board_size}; D={mcts_expansion_depth}, E={mcts_expansion_e}, I={mcts_iters}, R={rollout_run}, S={starting_player}"
            ):
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
                        white_won = reward > 0
                        break

                    # BLACK ACTION
                    action = second_player_agent.select_action(state.copy())
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    steps += 1
                    if done:
                        final_reward_for_second_player = reward
                        white_won = reward < 0
                        break

                final_reward_for_white_player = final_reward_for_first_player if starting_player == TakPlayer.WHITE else final_reward_for_second_player
                final_reward_for_black_player = final_reward_for_second_player if starting_player == TakPlayer.WHITE else final_reward_for_first_player

                results_file.writelines([
                    ",".join([
                        str(board_size),                                # board_size
                        str(mcts_expansion_depth),                      # mcts_expansion_depth
                        str(mcts_expansion_e),                          # mcts_expansion_epsilon
                        str(mcts_iters),                                # mcts_iterations
                        str(rollout_run),                               # rollout_runs
                        str(starting_player),                           # starting_player
                        str(sarsa_epsilon),                             # sarsa_epsilon
                        str(sarsa_alpha),                               # sarsa_alpha
                        str(sarsa_gamma),                               # sarsa_gamma
                        str(trial),                                     # trial_number
                        str(steps),                                     # steps
                        str(int(final_reward_for_white_player)),        # reward_for_white_player
                        str(int(final_reward_for_black_player)),        # reward_for_black_player
                        # str(game_knowledge_graph.total_nodes()),        # knowledge_graph_nodes
                        # str(game_knowledge_graph.total_rollouts())      # knowledge_graph_total_rollouts
                    ]) + "\n"])
            results_file.flush()

print("Done!")
