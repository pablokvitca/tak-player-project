from typing import List, Tuple, Optional, Set

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

    cache_has_path_for_player = {}

    @classmethod
    def wipe_cache(cls):
        cls.cache_has_path_for_player = {}

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

    def spaces_left(self) -> bool:
        """
        Returns whether there are any empty spaces left on the board
        :return: True if there are any empty spaces left
        """
        return len(self.get_empty_positions()) > 0

    def controlled_flat_spaces(self, player: TakPlayer) -> List[Tuple[int, int]]:
        """
        Returns the list of positions controlled by the given player.
        Defaults to only counting positions controlled by flat pieces

        :param player: the player to count for
        :return: a list of positions controlled by the player
        """
        return self.get_positions_controlled_by_player(player, only_flat_pieces=True)

    def controlled_road_spaces(self, player: TakPlayer) -> List[Tuple[int, int]]:
        """
        Returns the list of positions controlled by the player with pieces that can build a road (flat or capstone)
        :param player: the player to count for
        :return: a list of positions controlled by the player
        """
        return self.get_positions_controlled_by_player(player, only_road_pieces=True)

    def get_connected_positions(
            self,
            road_positions_controlled: List[Tuple[int, int]],
            position: Tuple[int, int],
            allowed_dirs: str = 'URDL',
            only_low_road: bool = False,
            only_high_road: bool = False
    ) -> Set[Tuple[int, int]]:
        up = (position[0], position[1] + 1) if 'U' in allowed_dirs else None
        right = (position[0] + 1, position[1]) if 'R' in allowed_dirs else None
        down = (position[0], position[1] - 1) if 'D' in allowed_dirs else None
        left = (position[0] - 1, position[1]) if 'L' in allowed_dirs else None
        return {
            pos
            for pos in [up, right, down, left]
            if (
                    pos is not None  # None means not considering going in that direction
                    and self.is_position_in_board(pos)  # Position must be in the board
                    and (not only_low_road or self.position_height(pos[0], pos[1]) == 1)  # only low road
                    and (not only_high_road or self.position_height(pos[0], pos[1]) >= 1)  # only high road
                    and pos in road_positions_controlled  # Position must be controlled by the player
            )
        }

    def has_path(
            self,
            road_positions_controlled: List[Tuple[int, int]],
            start_positions: Set[Tuple[int, int]],
            end_positions: Set[Tuple[int, int]],
            _max_steps: int, _step: int = 0,
            allowed_dirs: Optional[str] = 'URDL',
            only_low_road: bool = False,
            only_high_road: bool = False
    ) -> bool:
        allowed_dirs = allowed_dirs if allowed_dirs is not None else 'URDL'
        for current_position in start_positions:
            if current_position in end_positions:
                return True
            if _step > _max_steps:
                break
            if self.has_path(
                    road_positions_controlled,
                    self.get_connected_positions(
                        road_positions_controlled,
                        current_position,
                        allowed_dirs=allowed_dirs,
                        only_low_road=only_low_road,
                        only_high_road=only_high_road
                    ),
                    end_positions,
                    _max_steps=_max_steps,
                    _step=_step + 1
            ):
                return True
        return False

    def has_path_for_player(
            self,
            player: TakPlayer,
            only_low_road: bool = False,
            only_high_road: bool = False,
            only_straight_road: bool = False,
    ) -> bool:
        """
        Memo _has_path_for_player
        """
        params = (self, player, only_low_road, only_high_road, only_straight_road)
        if params not in self.__class__.cache_has_path_for_player:
            self.__class__.cache_has_path_for_player[params] = self._has_path_for_player(
                player,
                only_low_road=only_low_road, only_high_road=only_high_road, only_straight_road=only_straight_road
            )
        return self.__class__.cache_has_path_for_player[params]

    def _has_path_for_player(
            self,
            player: TakPlayer,
            only_low_road: bool = False,
            only_high_road: bool = False,
            only_straight_road: bool = False,
    ) -> bool:
        """
        Returns whether there is a path for the given player
        TODO: docs
        TODO: tests!
        :param player:
        :param only_low_road:
        :param only_high_road:
        :param only_straight_road:
        :return:
        """
        assert not (only_low_road and only_high_road), "Only accepts only_high_road or only_low_road, not both"

        road_positions_controlled = self.controlled_road_spaces(player)
        max_steps = len(road_positions_controlled)

        # Cannot possibly have path if there are not enough controlled spaces for the shortest possible road (straight)
        if max_steps < self.board_size:
            return False

        controlled_vertical_start_positions = {
            pos for pos in self.vertical_road_start_positions
            if pos in road_positions_controlled
        }

        controlled_vertical_end_positions = {
            pos for pos in self.vertical_road_end_positions
            if pos in road_positions_controlled
        }

        allowed_dirs_vertical = 'UD' if only_straight_road else None
        v_possible = len(controlled_vertical_start_positions) > 0 and len(controlled_vertical_end_positions) > 0
        if v_possible and self.has_path(
                road_positions_controlled,
                controlled_vertical_start_positions, controlled_vertical_end_positions,
                max_steps,
                allowed_dirs=allowed_dirs_vertical, only_low_road=only_low_road, only_high_road=only_high_road
        ):
            return True

        controlled_horizontal_start_positions = {
            pos for pos in self.horizontal_road_start_positions
            if pos in road_positions_controlled
        }

        controlled_horizontal_end_positions = {
            pos for pos in self.horizontal_road_end_positions
            if pos in road_positions_controlled
        }

        allowed_dirs_horizontal = 'RL' if only_straight_road else None
        h_possible = len(controlled_horizontal_start_positions) > 0 and len(controlled_horizontal_end_positions) > 0
        if h_possible and self.has_path(
                road_positions_controlled,
                controlled_horizontal_start_positions,
                controlled_horizontal_end_positions,
                max_steps,
                allowed_dirs=allowed_dirs_horizontal, only_low_road=only_low_road, only_high_road=only_high_road
        ):
            return True

        return False

    @staticmethod
    def from_3d_matrix(board_matrix: np.ndarray, board_size: int) -> 'TakBoard':
        """
        Builds a board with the pieces on the given matrix
        :param board_matrix: the matrix representation of the board
        :param board_size: the size of the original board
        :return: a TakBoard with the same data as the given matrix
        """
        stack_height = int(board_matrix.shape[0] / (board_size * board_size))
        board_matrix = board_matrix.reshape((board_size, board_size, stack_height))
        board = TakBoard(board_size)

        for file in range(board_size):
            for rank in range(board_size):
                for i in range(board_matrix.shape[2]):
                    piece_value = board_matrix[file, rank, i]
                    if piece_value != 0:
                        board.get_stack(file, rank).push(TakPiece(piece_value))
        return board

    def __eq__(self, other) -> bool:
        return self.board_size == other.board_size and self.board == other.board

    def __hash__(self) -> int:
        return hash((self.board_size, tuple(tuple(stack for stack in row) for row in self.board)))
