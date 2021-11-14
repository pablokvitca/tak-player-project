from enum import Enum


class TakPlayer(Enum):
    """
    TODO: docs
    """

    WHITE = "white"
    BLACK = "black"

    def other(self) -> "TakPlayer":
        if self == TakPlayer.WHITE:
            return TakPlayer.BLACK
        else:
            return TakPlayer.WHITE
