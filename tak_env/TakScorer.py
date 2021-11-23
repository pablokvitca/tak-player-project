from typing import Optional, Dict, Callable
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TakScorer(object):

    scorers: Dict[str, Callable[[], 'TakScorer']] = {
            'default': lambda: TakScorerDefault(),
            'downings': lambda: TakScorerDownings(),
            'middletown': lambda: TakScorerMiddletown(),
            'tarway': lambda: TakScorerTarway(),
        }

    def score(
            self,
            state: TakState,
            current_player: TakPlayer,
            winning_player: Optional[TakPlayer],
            discount: bool = False
    ) -> float:
        raise NotImplementedError("Score metric not implemented")

    @staticmethod
    def get(rules: str) -> 'TakScorer':
        if rules in TakScorer.scorers:
            return TakScorer.scorers[rules]()
        return TakScorerDefault()


class TakScorerDefault(TakScorer):

    def score(
            self,
            state: TakState,
            current_player: TakPlayer,
            winning_player: Optional[TakPlayer],
            discount: bool = False
    ) -> float:
        board_size = state.board_size
        score = (board_size * board_size) + state.pieces_left_player(current_player)
        return score if current_player == winning_player else (-score if discount else 0.0)


class TakScorerDownings(TakScorer):

    def score(
            self,
            state: TakState,
            current_player: TakPlayer,
            winning_player: Optional[TakPlayer],
            discount: bool = False
    ) -> float:
        board_size = state.board_size
        score = (board_size * board_size) + state.pieces_left_player(current_player)
        if current_player == winning_player:
            if state.has_path_for_player(current_player, only_straight_road=True):
                return score * 2
            return score
        else:
            return -score if discount else 0.0


class TakScorerMiddletown(TakScorer):

    def score(
            self,
            state: TakState,
            current_player: TakPlayer,
            winning_player: Optional[TakPlayer],
            discount: bool = False
    ) -> float:
        board_size = state.board_size
        score = (board_size * board_size) + state.pieces_left_player(current_player)
        if current_player == winning_player:
            if state.current_player_has_capstone_available():
                return score * 2
            return score
        else:
            return -score if discount else 0.0


class TakScorerTarway(TakScorer):

    def score(
            self,
            state: TakState,
            current_player: TakPlayer,
            winning_player: Optional[TakPlayer],
            discount: bool = False
    ) -> float:
        board_size = state.board_size
        score = (board_size * board_size) + state.pieces_left_player(current_player)
        if current_player == winning_player:
            if state.has_path_for_player(current_player, only_low_road=True):
                return score * 2
            if state.has_path_for_player(current_player, only_high_road=True):
                return score * 3
            return score
        else:
            return -score if discount else 0.0
