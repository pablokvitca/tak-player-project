from enum import Enum
from typing import Tuple, List, Iterable, Dict

from more_itertools import flatten

from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState
from utils.utils import ordered_partitions


class TakAction(object):

    # cache_possible_move_actions: Dict[TakState, List['TakAction']] = {}
    # cache_possible_place_actions: Dict[TakState, List['TakAction']] = {}

    # @classmethod
    # def wipe_cache(cls):
    #     cls.cache_possible_move_actions = {}
    #     cls.cache_possible_place_actions = {}

    def __init__(self, position: Tuple[int, int]):
        self.position: Tuple[int, int] = position

    def is_valid(self, state: TakState) -> bool:
        raise NotImplementedError("Method 'is_valid' not implemented")

    def take(self, state: TakState, mutate: bool = True) -> TakState:
        raise NotImplementedError("Method 'take' not implemented")

    def __eq__(self, other):
        raise NotImplementedError("Method '__eq__' not implemented")

    def __hash__(self):
        raise NotImplementedError("Method '__eq__' not implemented")

    # @classmethod
    # def get_all_possible_move_actions(cls, state) -> List['TakAction']:
    #     """
    #     Returns a list of all possible move actions that can be performed in this state.
    #     """
    #     if state not in cls.cache_possible_move_actions:
    #         if state.is_terminal()[0]:
    #             cls.cache_possible_move_actions[state] = []
    #         else:
    #             cls.cache_possible_move_actions[state] = \
    #                 TakActionMove.get_possible_move_actions(state, state.current_player)
    #
    #     return cls.cache_possible_move_actions[state]

    @staticmethod
    def get_all_possible_move_actions(state) -> List['TakAction']:
        """
        Returns a list of all possible move actions that can be performed in this state.
        """
        # if state.is_terminal()[0]:
        #     return []
        return TakActionMove.get_possible_move_actions(state, state.current_player)

    # @classmethod
    # def get_all_possible_place_actions(cls, state) -> List['TakAction']:
    #     """
    #     Returns a list of all possible place actions that can be performed in this state.
    #     """
    #     if state not in cls.cache_possible_place_actions:
    #         if state.is_terminal()[0]:
    #             cls.cache_possible_place_actions[state] = []
    #         else:
    #             current_player = state.current_player
    #
    #             # FIRST ACTION
    #             if state.first_action():
    #                 flat_piece = TakPiece.get_flat_piece_for_player(current_player.other())
    #                 cls.cache_possible_place_actions[state] = \
    #                     TakActionPlace.get_possible_place_actions(state, flat_piece)
    #             else:
    #
    #                 # PLACE ACTIONS
    #                 flat_piece = TakPiece.get_flat_piece_for_player(current_player)
    #                 place_flat = TakActionPlace.get_possible_place_actions(state, flat_piece)
    #                 standing_piece = TakPiece.get_standing_piece_for_player(current_player)
    #                 place_standing = TakActionPlace.get_possible_place_actions(state, standing_piece)
    #                 capstone_piece = TakPiece.get_capstone_piece_for_player(current_player)
    #                 place_capstone = TakActionPlace.get_possible_place_actions(state, capstone_piece)
    #
    #                 cls.cache_possible_place_actions[state] = place_flat + place_standing + place_capstone
    #
    #     return cls.cache_possible_place_actions[state]

    @staticmethod
    def get_all_possible_place_actions(state) -> List['TakAction']:
        """
        Returns a list of all possible place actions that can be performed in this state.
        """
        # if state.is_terminal()[0]:
        #     return []

        current_player = state.current_player

        # FIRST ACTION
        if state.first_action():
            flat_piece = TakPiece.get_flat_piece_for_player(current_player.other())
            return TakActionPlace.get_possible_place_actions(state, flat_piece)

        # PLACE ACTIONS
        flat_piece = TakPiece.get_flat_piece_for_player(current_player)
        place_flat = TakActionPlace.get_possible_place_actions(state, flat_piece)
        standing_piece = TakPiece.get_standing_piece_for_player(current_player)
        place_standing = TakActionPlace.get_possible_place_actions(state, standing_piece)
        capstone_piece = TakPiece.get_capstone_piece_for_player(current_player)
        place_capstone = TakActionPlace.get_possible_place_actions(state, capstone_piece)

        return place_flat + place_standing + place_capstone

    @staticmethod
    def get_possible_actions(state: TakState) -> List['TakAction']:
        """
        Returns a list of all possible actions that can be performed in this state.
        """
        if state.is_terminal()[0]:
            return []

        place_actions = TakAction.get_all_possible_place_actions(state)
        move_actions = TakAction.get_all_possible_move_actions(state)

        return place_actions + move_actions


class TakActionPlace(TakAction):

    def __init__(self, position, piece: TakPiece):
        super().__init__(position)
        self.piece = piece

    def is_valid(self, state: TakState) -> bool:
        place_at_file, place_at_rank = self.position

        # Can only place on empty positions
        if not state.board.is_position_empty(place_at_file, place_at_rank):
            return False

        # If the first action, can only place a flat stone and must be the opponents piece
        if state.first_action():
            # Can only place a flat stones (on first action)
            if not self.piece.is_flat():
                return False

            # Can only place the opponent's piece
            opponent = state.current_player.other()
            if self.piece.player() != opponent:
                return False
        else:
            # Can only place piece of the current player
            if self.piece.player() != state.current_player:
                return False

        # Can only place a capstone if the player has a capstone available
        if self.piece.is_capstone() and not state.current_player_has_capstone_available():
            return False
        # Can only place a piece if the player has a piece available
        elif not self.piece.is_capstone() and not state.current_player_has_pieces_available():
            return False

        # Place action is valid
        return True

    def take(self, state: TakState, mutate: bool = True) -> TakState:
        """
        Takes this action on the given state and returns the state resulting from it.
        Assumes the action is valid.

        :param state: The state to take the action on
        :param mutate: If true, mutates the state to take the action on
        :return: The resulting state
        """
        next_state: TakState = state if mutate else state.copy()
        next_state.board.place_piece(self.position, self.piece)

        if self.piece.is_capstone():
            next_state.remove_capstone_for_player(self.piece.player())
        else:
            next_state.remove_piece_for_player(self.piece.player())

        next_state.current_player = next_state.current_player.other()

        return next_state

    def __str__(self) -> str:
        """
        Returns a string representation of this action.
        Uses notation format from US TAK (https://ustak.org/portable-tak-notation/).
        NOTE: the last part of the notation is ignore in all cases, since it depends on the state of the board,
        not the action itself (it is part of the notation for readability).

        :return: a string representation of this action
        """

        stone = self.piece.type().upper()[0]
        square = TakBoard.get_square_name(self.position)
        return f"{stone}{square}"

    @staticmethod
    def get_possible_place_actions(state: TakState, piece: TakPiece) -> List['TakAction']:
        """
        Returns a list of all possible PLACE TakActions that can be performed in this state.
        TODO: docs
        """

        if piece.is_capstone() and not state.current_player_has_capstone_available():
            return []
        if not state.current_player_has_pieces_available():
            return []
        return [TakActionPlace(pos, piece) for pos in state.board.get_empty_positions()]

    def __eq__(self, other):
        return isinstance(other, TakActionPlace) and self.position == other.position and self.piece == other.piece

    def __hash__(self):
        return hash((self.position, self.piece))


class TakActionMoveDir(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def render(self, arrows: str = "↑→↓←") -> str:
        return arrows[self.value - 1]

    def get_delta(self,
                  distance: int = 1,
                  deltas: Tuple[Tuple[int, int], ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))
                  ) -> Tuple[int, int]:
        """
        Gets the delta of the direction of this action
        :param distance: the distance to move
        :param deltas: the deltas to use
        :return: a tuple of two ints representing the delta of the direction
        """
        return deltas[self.value - 1][0] * distance, deltas[self.value - 1][1] * distance

    def __eq__(self, other):
        return isinstance(other, TakActionMoveDir) and self.value == other.value

    def __hash__(self):
        return self.value


class TakActionMove(TakAction):

    def __init__(self, position: Tuple[int, int], direction: TakActionMoveDir, drop_order: Tuple[int, ...]):
        """
        TODO: docs
        """
        super().__init__(position)
        self.direction: TakActionMoveDir = direction
        self.drop_order: Tuple[int, ...] = drop_order

    def is_valid(self, state: TakState) -> bool:
        from_file, from_rank = self.position

        # Can only move if there is pieces on the board at the position
        if state.board.is_position_empty(from_file, from_rank):
            return False

        # Can only move if there is enough pieces to move from the position
        if state.board.get_stack(from_file, from_rank).height() < self.pick_up_count():
            return False

        # Can only move if the position is controlled by the current player
        if not state.board.is_position_controlled_by(
                from_file, from_rank, state.current_player,
                only_flat_pieces=False, only_road_pieces=False
        ):
            return False

        # Can only move if the total number of picked up pieces is less than the game's max pick up number
        if self.pick_up_count() > state.max_pick_up_number():
            return False

        # Can only move if the number of drop pieces fits in the board from the position in the direction
        ending_file, ending_rank = self.get_ending_position()
        if not state.board.is_position_in_board((ending_file, ending_rank)):
            return False

        # Can only move if for each drop position it: is empty, has a flat stone, or flattening a standing piece
        can_flatten = self.drop_order[-1] == 1 and state.board.get_stack(from_file, from_rank).top().is_capstone()
        drop_file, drop_rank = from_file, from_rank
        delta_file, delta_rank = self.direction.get_delta()
        for i, drop_n in enumerate(self.drop_order):
            drop_file, drop_rank = drop_file + delta_file * drop_n, drop_rank + delta_rank * drop_n
            if not state.board.is_position_in_board((drop_file, drop_rank)):
                return False
            position_stack = state.board.get_stack(drop_file, drop_rank)
            if not position_stack.is_empty():
                top_piece = position_stack.top()
                # Cannot flatten if not the last drop in the move or if the piece being dropped is not a capstone
                if top_piece.is_standing() and (i + 1 != len(self.drop_order) or not can_flatten):
                    return False
                # Cannot flatten a capstone
                if top_piece.is_capstone():
                    return False

        # Move action is valid
        return True

    def get_ending_position(self) -> Tuple[int, int]:
        """
        Gets the position where the drop order of this action ends
        TODO: docs
        :return:
        """

        from_x, from_y = self.position
        delta_x, delta_y = self.direction.get_delta(len(self.drop_order))
        return from_x + delta_x, from_y + delta_y

    def take(self, state: TakState, mutate: bool = True) -> TakState:
        """
        Takes this action on the given state and returns the state resulting from it.
        Assumes the action is valid.

        :param state: The state to take the action on
        :param mutate: If true, mutates the state to take the action on
        :return: The resulting state
        """
        next_state = state if mutate else state.copy()

        from_x, from_y = self.position

        # Pick up the pieces to move
        from_stack = next_state.board.get_stack(from_x, from_y)
        picked_up_pieces = []
        for i in range(sum(self.drop_order)):
            picked_up_pieces.append(from_stack.pop())

        drop_x, drop_y = self.position
        delta_x, delta_y = self.direction.get_delta()
        for drop_n in self.drop_order:
            drop_x, drop_y = drop_x + delta_x, drop_y + delta_y
            drop_stack = next_state.board.get_stack(drop_x, drop_y)
            for _ in range(drop_n):
                # The push method will automatically flatten the piece if it is standing
                # Since we assume the move is valid, no need to check the types pieces
                drop_stack.push(picked_up_pieces.pop())

        next_state.current_player = next_state.current_player.other()

        return next_state

    def pick_up_count(self) -> int:
        """
        Gets the number of pieces that are being picked up in this action
        :return: The number of pieces being picked up
        """
        return sum(self.drop_order)

    def __str__(self) -> str:
        """
        Returns a string representation of this action.
        Uses notation format from US TAK (https://ustak.org/portable-tak-notation/).
        NOTE: the last part of the notation is ignore in all cases, since it depends on the state of the board,
        not the action itself (it is part of the notation for readability).

        :return: a string representation of this action
        """

        count = self.pick_up_count()
        square = TakBoard.get_square_name(self.position)
        direction = self.direction.render()
        drop_counts = "".join([str(drop_n) for drop_n in self.drop_order])
        return f"{count}{square}{direction}{drop_counts}"

    def __eq__(self, other):
        """
        Checks if this action is equal to another action
        :param other: The other action to compare to
        :return: True if the actions are equal, False otherwise
        """
        return isinstance(other, TakActionMove) and \
               self.position == other.position and \
               self.direction == other.direction and \
               self.drop_order == other.drop_order

    def __hash__(self):
        """
        Returns the hash of this action
        :return: The hash of this action
        """
        return hash((self.position, self.direction, self.drop_order))

    @staticmethod
    def get_possible_move_actions(state: TakState, player: TakPlayer) -> List['TakAction']:
        """
        Returns a list of all possible MOVE TakActions that can be performed in this state.
        :param state: TODO: docs
        :param player:
        :return:
        """
        return list(flatten([
            TakActionMove.get_possible_move_actions_for_position(state, possible_from)
            for possible_from in state.board.get_positions_controlled_by_player(player)
        ]))

    @staticmethod
    def get_possible_move_actions_for_position(state: TakState, from_position: Tuple[int, int]) -> List['TakAction']:
        """
        Returns a list of all possible MOVE TakActions that can be performed in this state for a given position.
        :param state: TODO: docs
        :param from_position:
        :return: List[TakAction]
        """

        from_file, from_rank = from_position
        max_pickup_size = min(state.board.position_height(from_file, from_rank), state.max_pick_up_number())
        if max_pickup_size == 0:
            return []

        def possible_actions_for_direction(direction: TakActionMoveDir) -> List[TakActionMove]:
            drop_orders = TakActionMove.get_possible_drop_orders(max_pickup_size)
            actions = [TakActionMove(from_position, direction, drop_order) for drop_order in drop_orders]
            return [action for action in actions if action.is_valid(state)]

        up_actions = possible_actions_for_direction(TakActionMoveDir.UP)
        right_actions = possible_actions_for_direction(TakActionMoveDir.RIGHT)
        down_actions = possible_actions_for_direction(TakActionMoveDir.DOWN)
        left_actions = possible_actions_for_direction(TakActionMoveDir.LEFT)

        return up_actions + right_actions + down_actions + left_actions

    @staticmethod
    def get_possible_drop_orders(max_pickup_size: int) -> Iterable[Tuple[int, ...]]:
        """
        Returns a list of all possible drop orders that can be performed in this state.
        #ODO: move to TakActionMove
        :param max_pickup_size:
        :return:
        """
        return set(ordered_partitions(max_pickup_size))
