from collections import deque
from typing import Iterable, List, Optional

from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer


class PieceStack(object):
    """
    A stack of TakBoard objects.
    """

    def __init__(self, stack: Iterable[TakPiece] = ()):
        self.stack: deque[TakPiece] = deque(stack)

    def push(self, piece: TakPiece, ignore_check: bool = True) -> None:
        if ignore_check or self.valid_placement(piece):
            # If placing capstone on a standing piece, we need to flatten that piece
            if piece.is_capstone() and (not self.is_empty() and self.top().is_standing()):
                self.flatten()
            self.stack.append(piece)
        else:
            raise ValueError(f"Invalid placement (cannot place {piece.type()} on {self.top().type()}")

    def push_stack(self, pieces: 'PieceStack') -> None:
        self.push_many(pieces.as_list())

    def push_many(self, pieces: List[TakPiece]) -> None:
        for piece in pieces:
            self.push(piece)

    def pop(self) -> TakPiece:
        if self.is_empty():
            raise ValueError("Cannot move from empty position")
        return self.stack.pop()

    def pop_many(self, n: int) -> List[TakPiece]:
        return [self.pop() for _ in range(min(n, len(self.stack)))]

    def top(self) -> TakPiece:
        return self.stack[-1]

    def top_n(self, n: int) -> List[TakPiece]:
        return list(self.stack[-n:])

    def controlled_by(self) -> Optional[TakPlayer]:
        return self.top().player() if not self.is_empty() else None

    def is_controlled_by(self, player: TakPlayer, only_flat_pieces: bool = True) -> bool:
        return self.controlled_by() == player and (not only_flat_pieces or self.top().is_flat())

    def as_list(self) -> List[TakPiece]:
        return list(self.stack)

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def height(self) -> int:
        return len(self)

    def valid_placement(self, piece: TakPiece) -> bool:
        return self.is_empty() or piece.can_place_on(self.top())

    def flatten(self) -> None:
        if not self.is_empty() and self.top().is_standing():
            self.push(self.pop().flatten())

    def top_view_str(self) -> str:
        return "_" if self.is_empty() else self.top().view_str()

    def __str__(self) -> str:
        return str(self.stack)

    def __repr__(self) -> str:
        return repr(self.stack)

    def __len__(self) -> int:
        return len(self.stack)

    def copy(self) -> 'PieceStack':
        return PieceStack(self.as_list())
