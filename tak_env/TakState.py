from typing import List, Tuple
from tak_env.TakBoard import TakBoard
from tak_env.TakPlayer import TakPlayer


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

    def remove_piece_for_player(self, player: TakPlayer) -> None:
        """
        Removes a piece for the given player
        :param player:
        :return:
        """
        if player == TakPlayer.WHITE:
            if self.white_pieces_available > 0:
                self.white_pieces_available -= 1
            else:
                raise ValueError(f"No pieces available for player {player}")
        else:
            if self.black_pieces_available > 0:
                self.black_pieces_available -= 1
            else:
                raise ValueError(f"No pieces available for player {player}")

    def remove_capstone_for_player(self, player: TakPlayer) -> None:
        """
        Removes a capstone for the given player
        :param player:
        :return:
        """
        if player == TakPlayer.WHITE:
            if self.white_capstone_available:
                self.white_capstone_available = False
            else:
                raise ValueError(f"No capstone available for player {player}")
        else:
            if self.black_capstone_available:
                self.black_capstone_available = False
            else:
                raise ValueError(f"No capstone available for player {player}")

    def has_path_for_player(self, player: TakPlayer) -> bool:
        """
        Returns whether there is a path for the given player
        TODO: docs
        :param player:
        :return:
        """
        return False  # TODO: implement properly

    def pieces_left_player(self, player: TakPlayer) -> bool:
        """
        Returns whether there are pieces left for the given player
        :param player:
        :return:
        """
        if player == TakPlayer.WHITE:
            return self.white_pieces_available > 0 or self.white_capstone_available
        else:
            return self.black_pieces_available > 0 or self.black_capstone_available

    def pieces_left(self) -> bool:
        """
        Returns whether both players have pieces left
        :return: True if both players have pieces left
        """
        return self.pieces_left_player(TakPlayer.WHITE) and self.pieces_left_player(TakPlayer.BLACK)

    def spaces_left(self) -> bool:
        """
        Returns whether there are any empty spaces left on the board
        :return: True if there are any empty spaces left
        """
        return len(self.board.get_empty_positions()) > 0

    def controlled_spaces(self, player: TakPlayer, only_flat_pieces: bool = True) -> List[Tuple[int, int]]:
        """
        Returns the list of positions controlled by the given player.
        Defaults to only counting positions controlled by flat pieces

        :param player: the player to count for
        :param only_flat_pieces: (optional, True) whether to only count flat pieces
        :return: a list of positions controlled b the player
        """
        return self.board.get_positions_controlled_by_player(player, only_flat_pieces=only_flat_pieces)

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