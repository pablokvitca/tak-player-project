from gym import register, make

from TakPlayerAgent import TakPlayerAgent
from tak_env.TakAction import TakActionPlace
from tak_env.TakEnvironment import TakEnvironment
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer

# register(id=TakEnvironment.ENV_NAME, entry_point="tak_env:TakEnvironment")

# env = make(TakEnvironment.ENV_NAME, board_size=3)
env = TakEnvironment(board_size=3)

agent_white_player = TakPlayerAgent(TakPlayer.WHITE)
agent_black_player = TakPlayerAgent(TakPlayer.BLACK)

env.state.board.print_board_names()

# TEMPORARY: do 10 actions

state = env.reset()
env.render()

for i in range(10):
    action = agent_white_player.select_action(state)
    state, reward, done, _ = env.step(action)
    print(f"ACTION: {action} -> {reward}, {done}")
    env.render()
    if done:
        break

    action = agent_black_player.select_action(state)
    state, reward, done, info = env.step(action)
    print(f"ACTION: {action} -> {reward}, {done}")
    env.render()
    if done:
        break

env.close()
