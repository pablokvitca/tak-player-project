from typing import List, Tuple, Optional

import numpy as np

from tak_env import TakStack
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakStack import PieceStack


class TakBoard(object):
    """
    TakBoard class
    TODO: docs
    """

    def __init__(self, board_size: int):
        self.board_size = board_size
        self.board = [[PieceStack() for _ in range(board_size)] for _ in range(board_size)]

        self._positions_iterable = [(file, rank) for file in range(self.board_size) for rank in range(self.board_size)]

        self.vertical_road_start_positions = [(file, 0) for file in range(self.board_size)]
        self.vertical_road_end_positions = [(file, self.board_size - 1) for file in range(self.board_size)]
        self.horizontal_road_start_positions = [(0, rank) for rank in range(self.board_size)]
        self.horizontal_road_end_positions = [(self.board_size - 1, rank) for rank in range(self.board_size)]

    def copy(self):
        """
        Returns a copy of the board
        :return: TakBoard
        """
        copied_board = TakBoard(self.board_size)

        for file in range(self.board_size):
            for rank in range(self.board_size):
                copied_board.board[file][rank] = self.board[file][rank].copy()

        return copied_board

    def total_pieces(self) -> int:
        """
        Returns the total number of pieces on the board
        :return: int
        """
        return sum(sum(stack.height() for stack in file) for file in self.board)

    def get_stack(self, file: int, rank: int) -> PieceStack:
        """
        Returns the stack at the given position
        TODO: docs
        :param file: int
        :param rank: int
        :return: PieceStack
        """
        return self.board[file][rank]

    def is_position_empty(self, file: int, rank: int) -> bool:
        """
        Returns whether the given position is empty
        :param file: int
        :param rank: int
        :return: bool
        """
        return self.get_stack(file, rank).is_empty()

    def position_controlled_by(self, file: int, rank: int) -> Optional[TakPlayer]:
        """
        Returns the player that controls the given position (or None if the position is empty)
        :param file: int
        :param rank: int
        :return: TakPlayer or None
        """
        if self.is_position_empty(file, rank):
            return None
        else:
            return self.get_stack(file, rank).controlled_by()

    def is_position_controlled_by(
            self,
            file: int,
            rank: int,
            player: TakPlayer,
            only_flat_pieces: bool = False,
            only_road_pieces: bool = False
    ) -> bool:
        """
        Returns whether the given position is controlled by the given player
        :param file: int
        :param rank: int
        :param player: TakPlayer
        :param only_flat_pieces: whether to only count positions with flat pieces
        :param only_road_pieces: whether to only count positions with road pieces (flat or capstone)
        :return: bool
        """
        return self.get_stack(file, rank).is_controlled_by(
            player,
            only_flat_pieces=only_flat_pieces,
            only_road_pieces=only_road_pieces
        )

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """
        Returns a list of empty positions on the board
        :return: List of (x, y) tuples
        """
        return [(file, rank) for file, rank in self._positions_iterable if self.is_position_empty(file, rank)]

    def get_positions_controlled_by_player(
            self,
            player: TakPlayer,
            only_flat_pieces: bool = False,
            only_road_pieces: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Returns a list of positions controlled by the given player
        :param player: a TakPlayer
        :param only_flat_pieces: whether to only return positions with flat pieces
        :param only_road_pieces: whether to only return positions with road pieces (flat or capstone)
        :return: List of (x, y) tuples
        """
        return [
            (file, rank) for file, rank in self._positions_iterable
            if self.is_position_controlled_by(
                file, rank,
                player,
                only_flat_pieces=only_flat_pieces, only_road_pieces=only_road_pieces
            )
        ]

    def position_height(self, file: int, rank: int) -> int:
        """
        Returns the height of the stack at the given position
        :param file: int
        :param rank: int
        :return: int
        """
        return self.get_stack(file, rank).height()

    def place_piece(self, position: Tuple[int, int], piece: TakPiece) -> None:
        """
        Places the given piece at the given position
        Assumes the placement is valid
        :param position: the position to place the piece at
        :param piece: the piece to place
        """
        file, rank = position
        self.get_stack(file, rank).push(piece)

    def get_board_names_str(self) -> str:
        """
        Gets a string show the names of each position in the board
        """
        return '\n'.join(
            ' '.join(TakBoard.get_square_name((file, rank)) for file in range(self.board_size))
            for rank in range(self.board_size - 1, -1, -1)
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the board (only shows the top piece of each stack)
        TODO: show all pieces?
        :return: str
        """

        return '\n'.join([
            ' '.join([self.get_stack(file, rank).top_view_str() for file in range(self.board_size)])
            for rank in range(self.board_size - 1, -1, -1)
        ])

    @staticmethod
    def get_square_name(position):
        files = 'abcdefghi'
        ranks = '123456789'
        file, rank = position
        return files[file] + ranks[rank]

    def as_3d_matrix(self) -> (np.ndarray, int):
        """
        Returns a 3D matrix representation of the board.

        The values 1, 2, 3 represent a white piece of type flat, standing, and capstone, respectively.
        The values -1, -2, -3 represent a black piece of type flat, standing, and capstone, respectively.
        The value 0 represents an empty position. an empty position has all values 0.
        All positions are "padded" with 0 to the height of the tallest stack on the board.

        :return: a numpy 3D matrix with shape (board_size, board_size, max_stack_height)
        """

        max_height = max(1, max([self.get_stack(file, rank).height() for file, rank in self._positions_iterable]))

        board_matrix = np.zeros((self.board_size, self.board_size, max_height), dtype=int)

        for file, rank in self._positions_iterable:
            stack: TakStack = self.get_stack(file, rank)
            for i in range(stack.height()):
                board_matrix[file, rank, i] = stack.get_at(i).value

        return board_matrix, max_height

    def is_position_in_board(self, pos: Tuple[int, int]) -> bool:
        """
        Determines if the given position is in the board (or invalid)
        :param pos: a position in (file, rank)
        :return: True if the position is valid
        """
        file, rank = pos
        return 0 <= file < self.board_size and 0 <= rank < self.board_size
