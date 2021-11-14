from typing import Optional
from gym import Env, register
from tak_env.TakAction import TakAction
from tak_env.TakState import TakState
from tak_env.TakBoard import TakBoard
from tak_env.TakPlayer import TakPlayer


class TakEnvironment(Env):
    """
    TakEnvironment class
    TODO: docs
    """

    ENV_NAME = "TakEnvironment-v0"

    def __init__(self,
                 board_size,
                 use_capstone: Optional[bool] = None,
                 init_pieces: Optional[int] = None,
                 init_player: TakPlayer = TakPlayer.WHITE
                 ):
        """
        Initialize the tak_env
        TODO: docs
        :param board_size:
        :param use_capstone:
        :param init_pieces:
        :param init_player:
        """
        self.board_size: int = board_size
        self.use_capstone: bool = use_capstone if use_capstone is not None else TakEnvironment.default_capstone(board_size)
        self.init_pieces: int = init_pieces if init_pieces is not None else TakEnvironment.get_default_pieces(board_size)
        self.init_player: TakPlayer = init_player

        self.state: TakState = self.reset()

    def force_state(self, state: TakState) -> None:
        """
        Force the tak_env to a specific state
        :param state:
        :return:
        """

        self.state = state

    def current_state(self) -> TakState:
        """
        Get the current state of the tak_env
        :return:
        """

        return self.state

    def step(self, action: TakAction, mutate: bool = False) -> (TakState, float, bool, dict):
        """
        Take a step in the environment

        :param action: the action to take
        :param mutate: whether to mutate the state or not
        :return: the resulting state, the reward, if the game is over, and the info
        """
        if not action.is_valid(self.state):
            raise ValueError(f"Invalid action: {action}")

        current_player = self.state.current_player

        next_state: TakState = action.take(self.state, mutate=mutate)

        has_path_for_white = next_state.has_path_for_player(TakPlayer.WHITE)
        has_path_for_black = next_state.has_path_for_player(TakPlayer.BLACK)

        has_path = has_path_for_white and has_path_for_black

        done = has_path or (not next_state.pieces_left() or not next_state.spaces_left())

        reward = 0.0
        if done:
            winning_player = self.winning_player(current_player)
            reward = self.compute_score(current_player, winning_player)

        self.state = next_state

        return next_state, reward, done, {}

    def compute_score(self, current_player: TakPlayer, winning_player: Optional[TakPlayer]) -> float:
        """
        Computes the score of the given state. Assumes that the game is over.
        The score is computed for either player

        :param current_player: The player who is currently playing
        :param winning_player: The player who won the game
        :return: The score of the ended game
        """
        # TODO: compute scoring
        if winning_player is None:
            return 0.0
        return 1.0 if current_player == winning_player else -1.0

    def winning_player(self, last_play_by: TakPlayer) -> Optional[TakPlayer]:
        """
        Determines which player won the game. Assumes that the game is over.

        :param last_play_by: The player who last played
        :return: The winning player
        """
        has_path_for_white = self.state.has_path_for_player(TakPlayer.WHITE)
        has_path_for_black = self.state.has_path_for_player(TakPlayer.BLACK)

        # Did the last player to play win?
        if last_play_by == TakPlayer.WHITE and has_path_for_white:
            return TakPlayer.WHITE
        if last_play_by == TakPlayer.BLACK and has_path_for_black:
            return TakPlayer.BLACK

        # Did the other player win?
        if has_path_for_white:
            return TakPlayer.WHITE
        if has_path_for_black:
            return TakPlayer.BLACK

        # Secondary condition:
        flat_controlled_spaces_white: int = len(self.state.controlled_spaces(TakPlayer.WHITE))
        flat_controlled_spaces_black: int = len(self.state.controlled_spaces(TakPlayer.BLACK))

        if flat_controlled_spaces_white > flat_controlled_spaces_black:
            return TakPlayer.WHITE
        if flat_controlled_spaces_black > flat_controlled_spaces_white:
            return TakPlayer.BLACK

        # Tie
        return None

    def reset(self) -> TakState:
        """
        Reset the tak_env to its initial state
        :return:
        """

        self.state = TakState(
                 self.board_size,
                 TakBoard(self.board_size),
                 self.init_pieces,
                 self.init_pieces,
                 self.use_capstone,
                 self.use_capstone,
                 self.init_player
        )

        return self.state

    def render(self, mode="human") -> None:
        """
        Render the tak_env to the screen
        TODO: docs
        :param mode:
        :return:
        """
        # TODO: implement render method
        print("TAK ENVIRONMENT RENDER --- START")

        print(f"Current player: {self.state.current_player}")
        print(f"WHITE: pieces available: {self.state.white_pieces_available}, capstone available: {self.state.white_capstone_available}")
        print(f"BLACK: pieces available: {self.state.black_pieces_available}, capstone available: {self.state.black_capstone_available}")

        print(f"Board: \n{self.state.board}")

        print("TAK ENVIRONMENT RENDER --- END")

    @staticmethod
    def get_default_pieces(board_size) -> int:
        """
        Get the default number of pieces for a player at the start a game

        :param board_size: The size of the board
        :return: The default number of pieces for that board size
        """
        return board_size * board_size  # TODO: get from rulebook

    @staticmethod
    def default_capstone(board_size) -> bool:
        """
        TODO; docs

        :param board_size: The size of the board
        :return:
        """
        return board_size > 4  # TODO: get from rulebook
