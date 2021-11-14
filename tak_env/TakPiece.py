from enum import Enum
from typing import List

from tak_env.TakPlayer import TakPlayer


class TakPiece(Enum):
    WHITE_FLAT = 1
    WHITE_STANDING = 2
    WHITE_CAPSTONE = 3
    BLACK_FLAT = -1
    BLACK_STANDING = -2
    BLACK_CAPSTONE = -3

    @staticmethod
    def _flat() -> int:
        return 1

    @staticmethod
    def _standing() -> int:
        return 2

    @staticmethod
    def _capstone() -> int:
        return 3

    @staticmethod
    def get_all_pieces() -> List['TakPiece']:
        return TakPiece.get_white_pieces() + TakPiece.get_black_pieces()

    @staticmethod
    def get_white_pieces() -> List['TakPiece']:
        return [TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING, TakPiece.WHITE_CAPSTONE]

    @staticmethod
    def get_black_pieces() -> List['TakPiece']:
        return [TakPiece.BLACK_FLAT, TakPiece.BLACK_STANDING, TakPiece.BLACK_CAPSTONE]

    def abs_value(self):
        return abs(self.value)

    def is_flat(self) -> bool:
        return self.abs_value() == TakPiece._flat()

    def is_standing(self) -> bool:
        return self.abs_value() == TakPiece._standing()

    def is_capstone(self) -> bool:
        return self.abs_value() == TakPiece._capstone()

    def is_road(self) -> bool:
        return self.is_flat() or self.is_capstone()

    def can_place_on(self, other: 'TakPiece') -> bool:
        if self.is_flat() or self.is_standing():
            return other.is_flat()
        else:
            return not other.is_capstone()

    def will_flatten(self, other: 'TakPiece') -> bool:
        if other.is_capstone():
            return self.is_standing()
        else:
            return False

    def flatten(self) -> 'TakPiece':
        if self.is_standing():
            return self.get_piece_for_player(TakPiece._flat(), self.player())

        # Can only flatten standing pieces
        return self

    @staticmethod
    def get_piece_for_player(abs_value: int, player: TakPlayer) -> 'TakPiece':
        if player == TakPlayer.WHITE:
            return TakPiece(abs_value)
        else:
            return TakPiece(-abs_value)

    @staticmethod
    def get_flat_piece_for_player(player: TakPlayer) -> 'TakPiece':
        return TakPiece.get_piece_for_player(TakPiece._flat(), player)

    @staticmethod
    def get_standing_piece_for_player(player: TakPlayer) -> 'TakPiece':
        return TakPiece.get_piece_for_player(TakPiece._standing(), player)

    @staticmethod
    def get_capstone_piece_for_player(player: TakPlayer) -> 'TakPiece':
        return TakPiece.get_piece_for_player(TakPiece._capstone(), player)

    def get_can_place_on_top(self, player: TakPlayer) -> List['TakPiece']:
        flat = TakPiece.get_flat_piece_for_player(player)
        standing = TakPiece.getget_standing_piece_for_player_piece_for_player(player)
        if self.is_flat():
            return [flat]
        if self.is_standing() or self.is_capstone():
            return [flat, standing]

    def get_can_place_on_top_of(self, player: TakPlayer) -> List['TakPiece']:
        flat = TakPiece.get_flat_piece_for_player(player)
        standing = TakPiece.getget_standing_piece_for_player_piece_for_player(player)
        if self.is_flat() or self.is_standing():
            return [flat]
        if self.is_capstone():
            return [flat, standing]

    def type(self) -> str:
        if self.is_flat():
            return "flat"
        if self.is_standing():
            return "standing"
        if self.is_capstone():
            return "capstone"

    def player(self) -> TakPlayer:
        return TakPlayer.WHITE if self.value > 0 else TakPlayer.BLACK

    def view_str(self) -> str:
        if self == TakPiece.WHITE_FLAT:
            return "F"
        if self == TakPiece.WHITE_STANDING:
            return "S"
        if self == TakPiece.WHITE_CAPSTONE:
            return "C"
        if self == TakPiece.BLACK_FLAT:
            return "f"
        if self == TakPiece.BLACK_STANDING:
            return "s"
        if self == TakPiece.BLACK_CAPSTONE:
            return "c"

    def __str__(self):
        return f'{str(self.player()).lower()}_{self.type()}'
