from typing import List, Tuple, Iterable, Optional

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

        self._positions_iterable = [(x, y) for x in range(self.board_size) for y in range(self.board_size)]

    def copy(self):
        """
        Returns a copy of the board
        :return: TakBoard
        """
        copied_board = TakBoard(self.board_size)

        for x in range(self.board_size):
            for y in range(self.board_size):
                copied_board.board[x][y] = self.board[x][y].copy()

        return copied_board

    def total_pieces(self) -> int:
        """
        Returns the total number of pieces on the board
        :return: int
        """
        return sum(sum(len(stack) for stack in row) for row in self.board)

    def get_stack(self, x: int, y: int) -> PieceStack:
        """
        Returns the stack at the given position
        :param x: int
        :param y: int
        :return: PieceStack
        """
        return self.board[x][y]

    def is_position_empty(self, x: int, y: int) -> bool:
        """
        Returns whether the given position is empty
        :param x: int
        :param y: int
        :return: bool
        """
        return self.get_stack(x, y).is_empty()

    def position_controlled_by(self, x: int, y: int) -> Optional[TakPlayer]:
        """
        Returns the player that controls the given position (or None if the position is empty)
        :param x: int
        :param y: int
        :return: TakPlayer or None
        """
        if self.is_position_empty(x, y):
            return None
        else:
            return self.get_stack(x, y).controlled_by()

    def is_position_controlled_by(self, x: int, y: int, player: TakPlayer) -> bool:
        """
        Returns whether the given position is controlled by the given player
        :param x: int
        :param y: int
        :param player: TakPlayer
        :return: bool
        """
        return self.get_stack(x, y).is_controlled_by(player)

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """
        Returns a list of empty positions on the board
        :return: List of (x, y) tuples
        """
        return [(x, y) for (x, y) in self._positions_iterable if self.is_position_empty(x, y)]

    def get_positions_controlled_by_player(self, player: TakPlayer) -> List[Tuple[int, int]]:
        """
        Returns a list of positions controlled by the given player
        :param player: a TakPlayer
        :return: List of (x, y) tuples
        """
        return [(x, y) for (x, y) in self._positions_iterable if self.is_position_controlled_by(x, y, player)]

    def position_height(self, x: int, y: int) -> int:
        """
        Returns the height of the stack at the given position
        :param x: int
        :param y: int
        :return: int
        """
        return self.get_stack(x, y).height()

    def place_piece(self, position: Tuple[int, int], piece: TakPiece) -> None:
        """
        Places the given piece at the given position
        Assumes the placement is valid
        :param position: the position to place the piece at
        :param piece: the piece to place
        """
        x, y = position
        self.get_stack(x, y).push(piece)
