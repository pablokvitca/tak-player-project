from tqdm import trange

from TakPlayerAgent import TakPlayerAgent
from policies import RandomPolicyLessLikelyPlace
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPlayer import TakPlayer

# register(id=TakEnvironment.ENV_NAME, entry_point="tak_env:TakEnvironment")

# env = make(TakEnvironment.ENV_NAME, board_size=3)
env = TakEnvironment(board_size=5)

agent_white_player = TakPlayerAgent(TakPlayer.WHITE, policy=RandomPolicyLessLikelyPlace())
agent_black_player = TakPlayerAgent(TakPlayer.BLACK, policy=RandomPolicyLessLikelyPlace())

info = {'ended_with_path': False}


def log(log_pre, s):
    return log_pre + s + '\n'


log_str = "Nothing here"

for _ in trange(10000):
    state = env.reset()
    log_str = ""

    done = False
    while not done:
        action = agent_white_player.select_action(state)
        state, reward, done, info = env.step(action)
        log_str = log(log_str, f"WHITE ACTION: {action} -> {reward}, {done}")
        # env.render()
        if done:
            break

        action = agent_black_player.select_action(state)
        state, reward, done, info = env.step(action)
        log_str = log(log_str, f"BLACK ACTION: {action} -> {reward}, {done}")
        # env.render()
        if done:
            break

    # env.render()

    log_str = log(log_str, "GAME END INFO:")
    log_str = log(log_str, f"""
    GAME END INFO:
        Winning Player: {info['winning_player']}
        Ended with path: {info['ended_with_path']}
        Ended with no pieces left: {info['ended_with_no_pieces_left']}
        Ended with no spaces left: {info['ended_with_no_spaces_left']}
        WHITE: Remaining Pieces: {info['white_pieces_available']} Remaining Capstone: {info['white_capstone_available']}
        BLACK: Remaining Pieces: {info['black_pieces_available']} Remaining Capstone: {info['black_capstone_available']}
    """)

    if info['ended_with_path']:
        break

print(log_str)

env.render()

env.state.board.as_3d_matrix()[0].tofile("savedboard_1.txt")

env.close()
