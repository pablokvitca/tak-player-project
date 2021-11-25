from typing import List, Tuple, Set, Optional, Any, Dict
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

    cache_state_is_terminal: Dict['TakState', Tuple[bool, Dict[str, Any]]] = {}

    @classmethod
    def wipe_cache(cls):
        cls.cache_state_is_terminal = {}

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

        self.cache_is_terminal: Optional[bool] = None
        self.cache_is_terminal_info: Optional[Dict[str, Any]] = None

        if self in TakState.cache_state_is_terminal:
            self.cache_is_terminal, self.cache_is_terminal_info = TakState.cache_state_is_terminal[self]

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

    def pieces_left_player(self, player: TakPlayer) -> bool:
        """
        Returns whether there are pieces left for the given player
        TODO: docs
        :param player:
        :return:
        """
        if player == TakPlayer.WHITE:
            return self.white_pieces_available > 0 or self.white_capstone_available
        else:
            return self.black_pieces_available > 0 or self.black_capstone_available

    def spaces_left(self) -> bool:
        """
        Returns whether there are any empty spaces left on the board
        :return: True if there are any empty spaces left
        """
        return self.board.spaces_left()

    def pieces_left(self) -> bool:
        """
        Returns whether both players have pieces left
        :return: True if both players have pieces left
        """
        return self.pieces_left_player(TakPlayer.WHITE) and self.pieces_left_player(TakPlayer.BLACK)

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

    # def is_terminal(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
    #     """
    #     Returns whether this state is terminal (and extra info)
    #     :return: True if this state is terminal, False otherwise, and extra info as a dictionary
    #     """
    #     if True or (self.cache_is_terminal is None and self.cache_is_terminal_info is None):
    #         has_path_for_white = self.board.has_path_for_player(TakPlayer.WHITE)
    #         has_path_for_black = self.board.has_path_for_player(TakPlayer.BLACK)
    #
    #         has_path = has_path_for_white and has_path_for_black
    #
    #         has_pieces_left = self.pieces_left()
    #         has_spaces_left = self.spaces_left()
    #
    #         last_player_to_move = self.current_player.other()
    #
    #         winning_player = self.winning_player(last_player_to_move, has_path_for_white, has_path_for_black)
    #
    #         self.cache_is_terminal = has_path or not has_pieces_left or not has_spaces_left
    #         if self.cache_is_terminal:
    #             self.cache_is_terminal_info = {
    #                 "ended_with_path": has_path,
    #                 "ended_with_no_pieces_left": not has_pieces_left,
    #                 "ended_with_no_spaces_left": not has_spaces_left,
    #                 "winning_player": winning_player,
    #             }
    #         self.__class__.cache_state_is_terminal[self] = self.cache_is_terminal, self.cache_is_terminal_info
    #     return self.cache_is_terminal, self.cache_is_terminal_info

    def is_terminal(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Returns whether this state is terminal (and extra info)
        :return: True if this state is terminal, False otherwise, and extra info as a dictionary
        """
        has_path_for_white = self.board.has_path_for_player(TakPlayer.WHITE)
        has_path_for_black = self.board.has_path_for_player(TakPlayer.BLACK)

        has_path = has_path_for_white and has_path_for_black

        has_pieces_left = self.pieces_left()
        has_spaces_left = self.spaces_left()

        last_player_to_move = self.current_player.other()

        winning_player = self.winning_player(last_player_to_move, has_path_for_white, has_path_for_black)

        done = has_path or not has_pieces_left or not has_spaces_left
        if done:
            return done, {
                    "ended_with_path": has_path,
                    "ended_with_no_pieces_left": not has_pieces_left,
                    "ended_with_no_spaces_left": not has_spaces_left,
                    "winning_player": winning_player,
                }
        return done, {}

    def winning_player(self, last_play_by: TakPlayer, has_path_for_white: bool, has_path_for_black: bool) \
            -> Optional[TakPlayer]:
        """
        Determines which player won the game. Assumes that the game is over.

        :param last_play_by: The player who last played
        :param has_path_for_white: Whether white has a path
        :param has_path_for_black: Whether black has a path
        :return: The winning player
        """

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
        flat_controlled_spaces_white: int = len(self.board.controlled_flat_spaces(TakPlayer.WHITE))
        flat_controlled_spaces_black: int = len(self.board.controlled_flat_spaces(TakPlayer.BLACK))

        if flat_controlled_spaces_white > flat_controlled_spaces_black:
            return TakPlayer.WHITE
        if flat_controlled_spaces_black > flat_controlled_spaces_white:
            return TakPlayer.BLACK

        # Tie
        return None

    def __eq__(self, other) -> bool:
        """
        Returns whether this state is equal to another state
        :param other: The other state
        :return: True if equal, False otherwise
        """
        return isinstance(other, TakState) and \
               self.board_size == other.board_size and \
               self.board == other.board and \
               self.white_pieces_available == other.white_pieces_available and \
               self.black_pieces_available == other.black_pieces_available and \
               self.white_capstone_available == other.white_capstone_available and \
               self.black_capstone_available == other.black_capstone_available and \
               self.current_player == other.current_player

    def __hash__(self) -> int:
        """
        Gets the hash of this state
        :return: int hash value
        """
        return hash((
            self.board_size, self.board,
            self.white_pieces_available, self.black_pieces_available,
            self.white_capstone_available, self.black_capstone_available,
            self.current_player
        ))