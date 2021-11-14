from typing import Optional
from gym import Env
from tak_env.TakAction import TakAction
from tak_env.TakState import TakState
from tak_env.TakBoard import TakBoard
from tak_env.TakPlayer import TakPlayer


class TakEnvironment(Env):
    """
    TakEnvironment class
    TODO: docs
    """

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
        self.board_size = board_size
        self.use_capstone = use_capstone if use_capstone is not None else self.default_capstone(board_size)
        self.init_pieces = init_pieces if init_pieces is not None else self.get_default_pieces(board_size)
        self.init_player = init_player

        self.state = self.reset

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

    def step(self, action: TakAction) -> (TakState, float, bool, dict):
        """
        Take a step in the tak_env
        :param action:
        :return:
        """
        pass

    @property
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
        pass

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
