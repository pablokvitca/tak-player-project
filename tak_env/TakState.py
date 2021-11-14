from collections import Iterable
from typing import List, Tuple

from tak_env.TakAction import TakAction, TakActionPlace, TakActionMove, TakActionMoveDir
from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer

from more_itertools import flatten


class TakState(object):
    """
    TakState class.
    The state of the Tak game is represented by:
        - A 2D grid of piece PieceStacks (TakBoard)
        - The number of pieces left to the white player
        - The number of pieces left to the black player
        - Whether the the white player has a capstone available to place
        - Whether the the black player has a capstone available to place
        - Which player's turn it is
    """

    def __init__(self,
                 board_size: int,
                 board: TakBoard,
                 white_pieces_available: int,
                 black_pieces_available: int,
                 white_capstone_available: bool,
                 black_capstone_available: bool,
                 current_player: TakPlayer
                 ):
        self.board_size: int = board_size

        self.board: TakBoard = board

        self.white_pieces_available: int = white_pieces_available
        self.black_pieces_available: int = black_pieces_available

        self.white_capstone_available: bool = white_capstone_available
        self.black_capstone_available: bool = black_capstone_available

        self.current_player: TakPlayer = current_player

    def first_action(self) -> bool:
        """
        Returns whether this is the first action of the game.
        """
        return 0 <= self.board.total_pieces() <= 1

    def get_possible_place_actions(self, piece: TakPiece) -> List[TakAction]:
        """
        Returns a list of all possible PLACE TakActions that can be performed in this state.
        """
        if (piece.is_capstone() and not self.current_player_has_capstone_available()) \
                or self.current_player_has_pieces_available():
            return []
        return [TakActionPlace(pos, piece) for pos in self.board.get_empty_positions()]

    def get_possible_move_actions(self, player: TakPlayer) -> List[TakAction]:
        """
        Returns a list of all possible MOVE TakActions that can be performed in this state.
        :param player:
        :return:
        """
        return list(flatten([
            self.get_possible_move_actions_for_position(possible_from)
            for possible_from in self.board.get_positions_controlled_by_player(player)
        ]))

    def get_possible_move_actions_for_position(self, from_position: Tuple[int, int]) -> List[TakAction]:
        """
        Returns a list of all possible MOVE TakActions that can be performed in this state for a given position.
        :param from_position:
        :return: List[TakAction]
        """

        from_x, from_y = from_position
        max_pickup_size = min(self.board.position_height(from_x, from_y), self.max_pick_up_number())
        if max_pickup_size == 0:
            return []

        def possible_actions_for_direction(direction: TakActionMoveDir) -> List[TakActionMove]:
            drop_orders = self.get_possible_drop_orders(max_pickup_size)
            actions = [TakActionMove(from_position, direction, drop_order) for drop_order in drop_orders]
            return [action for action in actions if self.is_valid_action(action)]

        up_actions = possible_actions_for_direction(TakActionMoveDir.UP)
        right_actions = possible_actions_for_direction(TakActionMoveDir.RIGHT)
        down_actions = possible_actions_for_direction(TakActionMoveDir.DOWN)
        left_actions = possible_actions_for_direction(TakActionMoveDir.LEFT)

        return up_actions + right_actions + down_actions + left_actions

    def get_possible_drop_orders(self, max_pickup_size: int) -> List[Tuple[int, ...]]:
        """
        Returns a list of all possible drop orders that can be performed in this state.
        :param max_pickup_size:
        :return:
        """
        # TODO: implement properly
        return [tuple([1] * i) for i in range(1, max_pickup_size + 1)]

    def is_valid_action(self, action: TakAction) -> bool:
        """
        Returns whether the given action is valid in this state.
        :param action:
        :return:
        """
        return action.is_valid(self)

    def get_possible_actions(self) -> List[TakAction]:
        """
        Returns a list of all possible actions that can be performed in this state.
        """
        if self.first_action():
            return self.get_possible_place_actions(TakPiece.get_flat_piece_for_player(self.current_player.other()))

        flat_piece = TakPiece.get_flat_piece_for_player(self.current_player)
        standing_piece = TakPiece.get_standing_piece_for_player(self.current_player)
        capstone_piece = TakPiece.get_capstone_piece_for_player(self.current_player)

        place_actions = self.get_possible_place_actions(flat_piece) \
                        + self.get_possible_place_actions(standing_piece) \
                        + self.get_possible_place_actions(capstone_piece)

        place_capstone = TakPiece.get_flat_piece_for_player(self.current_player.other())

        move_actions = self.get_possible_move_actions(self.current_player)

        return place_actions + move_actions

    def current_player_has_pieces_available(self) -> bool:
        """
        Returns whether the current player has pieces available to play.
        :return:
        """
        if self.current_player == TakPlayer.WHITE:
            return self.white_pieces_available > 0
        return self.black_pieces_available > 0

    def current_player_has_capstone_available(self) -> bool:
        """
        Returns whether the current player has capstone available to play.
        :return:
        """
        if self.current_player == TakPlayer.WHITE:
            return self.white_capstone_available
        return self.black_capstone_available

    def max_pick_up_number(self) -> int:
        """
        Returns the maximum number of pieces that can be picked up in this state
        :return: the board size
        """
        return self.board_size

    def copy(self) -> 'TakState':
        """
        Returns a copy of this state
        :return:
        """
        return TakState(
            self.board_size,
            self.board.copy(),
            self.white_pieces_available,
            self.black_pieces_available,
            self.white_capstone_available,
            self.black_capstone_available,
            self.current_player
        )