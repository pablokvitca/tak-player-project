from typing import Optional

import numpy as np
import pandas as pd
from gym import Env
from tak_env.TakAction import TakAction
from tak_env.TakPiece import TakPiece
from tak_env.TakState import TakState
from tak_env.TakBoard import TakBoard
from tak_env.TakPlayer import TakPlayer
import plotly.express as px


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

        has_pieces_left = next_state.pieces_left()
        has_spaces_left = next_state.spaces_left()
        done = has_path or not has_pieces_left or not has_spaces_left

        reward = 0.0
        info = {}
        if done:
            winning_player = self.winning_player(current_player)
            reward = self.compute_score(current_player, winning_player)
            info = {
                "winning_player": winning_player,
                "ended_with_path": has_path,
                "ended_with_no_pieces_left": not has_pieces_left,
                "ended_with_no_spaces_left": not has_spaces_left,
                "white_pieces_available": next_state.white_pieces_available,
                "white_capstone_available": next_state.white_capstone_available,
                "black_pieces_available": next_state.black_pieces_available,
                "black_capstone_available": next_state.black_capstone_available,
            }

        self.state = next_state

        return next_state, reward, done, info

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

    def render_image(self) -> None:
        """
        Render the current state of the game as an image
        Uses matplotlib to make a 3D plot of the board
        """
        board, max_stack_height = self.state.board.as_3d_matrix()

        color_black = 'black'
        black_flats = np.where(board == TakPiece.BLACK_FLAT.value)
        black_standing = np.where(board == TakPiece.BLACK_STANDING.value)
        black_capstone = np.where(board == TakPiece.BLACK_CAPSTONE.value)

        color_white = 'white'
        white_flats = np.where(board == TakPiece.WHITE_FLAT.value)
        white_standing = np.where(board == TakPiece.WHITE_STANDING.value)
        white_capstone = np.where(board == TakPiece.WHITE_CAPSTONE.value)

        def add_to_df(df: pd.DataFrame, file, rank, stack_index, color, piece):
            return df.append({
                'file': file + 0.5,
                'rank': rank + 0.5,
                'stack_index': stack_index,
                'color': color,
                'piece': piece
            }, ignore_index=True)

        df = pd.DataFrame(columns=['file', 'rank', 'stack_index', 'color', 'piece'])

        for file, rank, stack_index in zip(*black_flats):
            df = add_to_df(df, file, rank, stack_index, color_black, 'black_flat')
        for file, rank, stack_index in zip(*black_standing):
            df = add_to_df(df, file, rank, stack_index, color_black, 'black_standing')
        for file, rank, stack_index in zip(*black_capstone):
            df = add_to_df(df, file, rank, stack_index, color_black, 'black_capstone')
        for file, rank, stack_index in zip(*white_flats):
            df = add_to_df(df, file, rank, stack_index, color_white, 'white_flat')
        for file, rank, stack_index in zip(*white_standing):
            df = add_to_df(df, file, rank, stack_index, color_white, 'white_standing')
        for file, rank, stack_index in zip(*white_capstone):
            df = add_to_df(df, file, rank, stack_index, color_white, 'white_capstone')

        fig = px.scatter_3d(
            df,
            x='file', y='rank', z='stack_index',
            color='color',
            symbol='piece',
            opacity=0.6,
            size_max=1.0
        )

        fig.update_traces(marker={"size": 12})

        z_ticks = max(10, max_stack_height)
        fig.update_layout(
            scene={
                "xaxis": {"nticks": self.board_size,  "range": [0, self.board_size]},
                "yaxis": {"nticks": self.board_size, "range": [0, self.board_size]},
                "zaxis": {"nticks": z_ticks, "range": [0, z_ticks]}
            })

        fig.show()

    def render_text(self) -> None:
        """
        Render the board in text mode
        """
        # TODO: implement render method
        print("TAK ENVIRONMENT RENDER --- START")

        print(f"Current player: {self.state.current_player}")
        print(
            f"WHITE: pieces available: {self.state.white_pieces_available}, capstone available: {self.state.white_capstone_available}")
        print(
            f"BLACK: pieces available: {self.state.black_pieces_available}, capstone available: {self.state.black_capstone_available}")

        print(f"Board: \n{self.state.board}")

        print("TAK ENVIRONMENT RENDER --- END")

    def render(self, mode="human") -> None:
        """
        Render the tak_env to the screen
        TODO: docs
        :param mode:
        :return:
        """
        if mode == "human":
            self.render_image()
        if mode == "text":
            self.render_text()

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
