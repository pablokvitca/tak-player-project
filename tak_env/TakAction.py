from enum import Enum
from typing import Tuple

from tak_env.TakPiece import TakPiece
from tak_env.TakState import TakState


class TakAction(object):

    def __init__(self, position: Tuple[int, int]):
        self.position = position

    def is_valid(self, state: TakState) -> bool:
        raise NotImplementedError("Method 'is_valid' not implemented")

    def take(self, state: TakState, mutate: bool = True) -> TakState:
        raise NotImplementedError("Method 'take' not implemented")


class TakActionPlace(TakAction):

    def __init__(self, position, piece: TakPiece):
        super().__init__(position)
        self.piece = piece

    def is_valid(self, state: TakState) -> bool:
        place_at_x, place_at_y = self.position

        # Can only place on empty positions
        if not state.board.is_position_empty(place_at_x, place_at_y):
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
        elif state.current_player_has_pieces_available():
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
            next_state.remove_capstone_for_player(next_state.current_player)
        else:
            next_state.remove_piece_for_player(next_state.current_player)

        next_state.current_player = next_state.current_player.other()

        return next_state


class TakActionMoveDir(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class TakActionMove(TakAction):

    def __init__(self, position: Tuple[int, int], direction: TakActionMoveDir, drop_order: Tuple[int, ...]):
        """
        TODO: docs
        """
        super().__init__(position)
        self.direction = direction
        self.drop_order = drop_order

    def is_valid(self, state: TakState) -> bool:
        from_x, from_y = self.position

        # Can only move if there is pieces on the board at the position
        if state.board.is_position_empty(from_x, from_y):
            return False

        # Can only move if the position is controlled by the current player
        if not state.board.is_position_controlled_by(from_x, from_y, state.current_player):
            return False

        # Can only move if the total number of picked up pieces is less than the game's max pick up number
        if sum(self.drop_order) > state.max_pick_up_number():
            return False

        # Can only move if the number of drop pieces fits in the board from the position in the direction
        ending_x, ending_y = self.get_ending_position()
        if not (0 <= ending_x < state.board.board_size and 0 <= ending_y < state.board.board_size):
            return False

        # Can only move if for each drop position it: is empty, has a flat stone, or flattening a standing piece
        can_flatten = self.drop_order[-1] == 1 and state.board.get_stack(from_x, from_y).top().is_capstone()
        drop_x, drop_y = from_x, from_y
        delta_x, delta_y = self.get_direction_delta()
        for i, drop_n in enumerate(self.drop_order):
            drop_x, drop_y = drop_x + delta_x, drop_y + delta_y
            position_stack = state.board.get_stack(drop_x, drop_y)
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
        :return:
        """
        from_x, from_y = self.position
        delta_x, delta_y = self.get_direction_delta(len(self.drop_order))
        return from_x + delta_x, from_y + delta_y

    def get_direction_delta(self, distance: int = 1) -> Tuple[int, int]:
        """
        Gets the delta of the direction of this action
        :param distance: the distance to move
        :return: a tuple of two ints representing the delta of the direction
        """
        if self.direction == TakActionMoveDir.UP:
            return 0, -distance
        elif self.direction == TakActionMoveDir.RIGHT:
            return distance, 0
        elif self.direction == TakActionMoveDir.DOWN:
            return 0, distance
        elif self.direction == TakActionMoveDir.LEFT:
            return -distance, 0
        else:
            raise ValueError("Invalid direction")

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
        delta_x, delta_y = self.get_direction_delta()
        for drop_n in self.drop_order:
            drop_x, drop_y = drop_x + delta_x, drop_y + delta_y
            drop_stack = next_state.board.get_stack(drop_x, drop_y)
            for _ in range(drop_n):
                # The push method will automatically flatten the piece if it is standing
                # Since we assume the move is valid, no need to check the types pieces
                drop_stack.push(picked_up_pieces.pop())

        next_state.current_player = next_state.current_player.other()

        return next_state
