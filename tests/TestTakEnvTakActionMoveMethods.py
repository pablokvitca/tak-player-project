import unittest

from tak_env.TakAction import TakActionMove, TakActionMoveDir, TakActionPlace
from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TestTakEnvTakActionMoveMethods(unittest.TestCase):

    def test_tak_action_move_init(self):
        move_up_1 = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertEqual(move_up_1.position, (0, 0))
        self.assertEqual(move_up_1.direction, TakActionMoveDir.UP)
        self.assertEqual(move_up_1.drop_order, (1,))

        move_right_11 = TakActionMove((1, 5), TakActionMoveDir.RIGHT, (1, 1))
        self.assertEqual(move_right_11.position, (1, 5))
        self.assertEqual(move_right_11.direction, TakActionMoveDir.RIGHT)
        self.assertEqual(move_right_11.drop_order, (1, 1))

        move_down_1121 = TakActionMove((1, 5), TakActionMoveDir.DOWN, (1, 1, 2, 1))
        self.assertEqual(move_down_1121.position, (1, 5))
        self.assertEqual(move_down_1121.direction, TakActionMoveDir.DOWN)
        self.assertEqual(move_down_1121.drop_order, (1, 1, 2, 1))

    def test_tak_action_move_is_valid(self):
        state = TakState(3, TakBoard(3), 5, 5, False, False, TakPlayer.WHITE)
        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertFalse(action.is_valid(state))
        state = TakState(5, TakBoard(5), 11, 10, True, True, TakPlayer.WHITE)
        TakActionPlace((0, 0), TakPiece.BLACK_FLAT).take(state, mutate=True)  # Current player is black
        TakActionPlace((1, 2), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is white
        TakActionPlace((2, 2), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is black
        TakActionPlace((2, 3), TakPiece.BLACK_STANDING).take(state, mutate=True)  # Current player is white
        TakActionPlace((3, 3), TakPiece.WHITE_CAPSTONE).take(state, mutate=True)  # Current player is black
        TakActionPlace((1, 1), TakPiece.BLACK_CAPSTONE).take(state, mutate=True)  # Current player is white
        TakActionPlace((3, 0), TakPiece.WHITE_STANDING).take(state, mutate=True)  # Current player is black

        action = TakActionMove((2, 3), TakActionMoveDir.RIGHT, (1,))
        self.assertFalse(action.is_valid(state))

        action = TakActionMove((2, 3), TakActionMoveDir.UP, (1,))
        self.assertTrue(action.is_valid(state))

        action = TakActionMove((0, 0), TakActionMoveDir.DOWN, (1,))
        self.assertFalse(action.is_valid(state))

        action = TakActionMove((0, 0), TakActionMoveDir.LEFT, (1,))
        self.assertFalse(action.is_valid(state))

        action = TakActionMove((3, 3), TakActionMoveDir.LEFT, (1,))
        self.assertFalse(action.is_valid(state))

        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertTrue(action.is_valid(state))
        action.take(state, mutate=True)  # Current player is white

        action = TakActionMove((3, 3), TakActionMoveDir.LEFT, (1,))
        self.assertTrue(action.is_valid(state))

        TakActionPlace((4, 4), TakPiece.WHITE_STANDING).take(state, mutate=True)  # Current player is black

        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1, 1, 1))
        self.assertFalse(action.is_valid(state))
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1, 1, 1))
        self.assertTrue(action.is_valid(state))
        action = TakActionMove((0, 0), TakActionMoveDir.UP, (6, ))
        self.assertFalse(action.is_valid(state))
        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1, 4, 1))
        self.assertFalse(action.is_valid(state))

        TakActionPlace((0, 4), TakPiece.BLACK_FLAT).take(state, mutate=True)  # Current player is white
        action = TakActionMove((4, 4), TakActionMoveDir.UP, (1,))
        self.assertFalse(action.is_valid(state))
        action = TakActionMove((4, 4), TakActionMoveDir.RIGHT, (1,))
        self.assertFalse(action.is_valid(state))
        action = TakActionMove((4, 4), TakActionMoveDir.DOWN, (1,))
        self.assertTrue(action.is_valid(state))
        action = TakActionMove((4, 4), TakActionMoveDir.LEFT, (1,))
        self.assertTrue(action.is_valid(state))

        # TODO: test flattening validity check fail for flat and for standing
        # TODO: test flattening validity check fail for capstone not moving alone

    def test_tak_action_move_take(self):
        state = TakState(5, TakBoard(5), 11, 10, False, False, TakPlayer.WHITE)  # Current player is white
        TakActionPlace((0, 0), TakPiece.BLACK_FLAT).take(state, mutate=True)  # Current player is black
        TakActionPlace((1, 1), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is white
        self.assertEqual(len(state.board.get_empty_positions()), 5 * 5 - 2)
        action = TakActionMove((1, 1), TakActionMoveDir.DOWN, (1,))
        action.take(state, mutate=True)  # Current player is black
        self.assertEqual(state.board.get_stack(1, 1).height(), 0)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 0).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(len(state.board.get_empty_positions()), 5 * 5 - 2)
        action = TakActionMove((0, 0), TakActionMoveDir.RIGHT, (1,))
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(0, 0).height(), 0)
        self.assertEqual(state.board.get_stack(1, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 0).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])
        self.assertEqual(len(state.board.get_empty_positions()), 5 * 5 - 1)

        state = TakState(5, TakBoard(5), 11, 10, True, True, TakPlayer.WHITE)  # Current player is white
        TakActionPlace((0, 0), TakPiece.BLACK_FLAT).take(state, mutate=True)  # Current player is black
        TakActionPlace((1, 2), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is white
        TakActionPlace((2, 2), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is black
        TakActionPlace((2, 3), TakPiece.BLACK_STANDING).take(state, mutate=True)  # Current player is white
        TakActionPlace((3, 3), TakPiece.WHITE_CAPSTONE).take(state, mutate=True)  # Current player is black
        TakActionPlace((1, 1), TakPiece.BLACK_CAPSTONE).take(state, mutate=True)  # Current player is white
        TakActionPlace((3, 0), TakPiece.WHITE_STANDING).take(state, mutate=True)  # Current player is black

        # test move single, no flattening, flat, to empty
        action = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertEqual(str(action), "1a1↑1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(0, 0).height(), 0)
        self.assertEqual(state.board.get_stack(0, 1).height(), 1)
        self.assertEqual(state.board.get_stack(0, 1).top(), TakPiece.BLACK_FLAT)

        # test move single, no flattening, standing, to empty
        action = TakActionMove((3, 0), TakActionMoveDir.LEFT, (1,))
        self.assertEqual(str(action), "1d1←1")
        action.take(state, mutate=True)  # Current player is black
        self.assertEqual(state.board.get_stack(3, 0).height(), 0)
        self.assertEqual(state.board.get_stack(2, 0).height(), 1)
        self.assertEqual(state.board.get_stack(2, 0).top(), TakPiece.WHITE_STANDING)

        # test move single, no flattening, capstone, to empty
        action = TakActionMove((1, 1), TakActionMoveDir.RIGHT, (1,))
        self.assertEqual(str(action), "1b2→1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(1, 1).height(), 0)
        self.assertEqual(state.board.get_stack(2, 1).height(), 1)
        self.assertEqual(state.board.get_stack(2, 1).top(), TakPiece.BLACK_CAPSTONE)

        # test move single, no flattening, flat, to flat
        action = TakActionMove((1, 2), TakActionMoveDir.RIGHT, (1,))
        self.assertEqual(str(action), "1b3→1")
        action.take(state, mutate=True)  # Current player is black
        self.assertEqual(state.board.get_stack(1, 2).height(), 0)
        self.assertEqual(state.board.get_stack(2, 2).height(), 2)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.WHITE_FLAT])

        # test move single, no flattening, standing, to flat h=2
        action = TakActionMove((2, 3), TakActionMoveDir.DOWN, (1,))
        self.assertEqual(str(action), "1c4↓1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(2, 3).height(), 0)
        self.assertEqual(state.board.get_stack(2, 2).height(), 3)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.BLACK_STANDING)
        self.assertEqual(state.board.get_stack(2, 2).top_n(3),
                         [TakPiece.WHITE_FLAT, TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING])

        # test move single, no flattening, capstone, to flat
        TakActionPlace((1, 1), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is black
        action = TakActionMove((2, 1), TakActionMoveDir.LEFT, (1,))
        self.assertEqual(str(action), "1c2←1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(2, 1).height(), 0)
        self.assertEqual(state.board.get_stack(1, 1).height(), 2)
        self.assertEqual(state.board.get_stack(1, 1).top(), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(state.board.get_stack(1, 1).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE])

        # test move multiple, no flattening, single drop, all empty
        TakActionPlace((2, 3), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is black
        action = TakActionMove((1, 1), TakActionMoveDir.UP, (2,))
        self.assertEqual(str(action), "2b2↑2")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(1, 1).height(), 0)
        self.assertEqual(state.board.get_stack(1, 2).height(), 2)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(state.board.get_stack(1, 2).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE])

        # test move multiple, no flattening, multi drop, all empty
        TakActionPlace((1, 3), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is black
        action = TakActionMove((2, 2), TakActionMoveDir.RIGHT, (1, 2,))
        self.assertEqual(str(action), "3c3→12")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(2, 2).height(), 0)
        self.assertEqual(state.board.get_stack(3, 2).height(), 1)
        self.assertEqual(state.board.get_stack(4, 2).height(), 2)
        self.assertEqual(state.board.get_stack(3, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(4, 2).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING])

        # test move multiple, no flattening, multi drop, some empty some flat
        action = TakActionMove((1, 2), TakActionMoveDir.UP, (1, 1,))
        self.assertEqual(str(action), "2b3↑11")
        action.take(state, mutate=True)  # Current player is black
        self.assertEqual(state.board.get_stack(1, 2).height(), 0)
        self.assertEqual(state.board.get_stack(1, 3).height(), 2)
        self.assertEqual(state.board.get_stack(1, 4).height(), 1)
        self.assertEqual(state.board.get_stack(1, 3).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.WHITE_FLAT])
        self.assertEqual(state.board.get_stack(1, 4).top(), TakPiece.BLACK_CAPSTONE)

        # test move single, flattening
        TakActionPlace((3, 1), TakPiece.WHITE_FLAT).take(state, mutate=True)  # Current player is white
        TakActionPlace((4, 3), TakPiece.BLACK_STANDING).take(state, mutate=True)  # Current player is black
        action = TakActionMove((3, 3), TakActionMoveDir.RIGHT, (1,))
        self.assertEqual(str(action), "1d4→1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(3, 3).height(), 0)
        self.assertEqual(state.board.get_stack(4, 3).height(), 2)
        self.assertEqual(state.board.get_stack(4, 3).top_n(2), [TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE])

        # test move multiple, flattening, all empty but last standing
        action = TakActionMove((1, 4), TakActionMoveDir.DOWN, (1,))
        self.assertTrue(str(action), "1b5↓1")
        action.take(state, mutate=True)  # Current player is black
        action = TakActionMove((2, 0), TakActionMoveDir.LEFT, (1,))
        self.assertTrue(str(action), "1c1←1")
        action.take(state, mutate=True)  # Current player is white
        action = TakActionMove((1, 3), TakActionMoveDir.DOWN, (1, 1, 1))
        self.assertEqual(str(action), "3b4↓111")
        action.take(state, mutate=True)  # Current player is black
        self.assertEqual(state.board.get_stack(1, 3).height(), 0)
        self.assertEqual(state.board.get_stack(1, 2).height(), 1)
        self.assertEqual(state.board.get_stack(1, 1).height(), 1)
        self.assertEqual(state.board.get_stack(1, 0).height(), 2)
        self.assertEqual(state.board.get_stack(4, 3).height(), 2)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(1, 1).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(1, 0).top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE])

        # test move single from h>1
        action = TakActionMove((4, 3), TakActionMoveDir.LEFT, (1,))
        self.assertEqual(str(action), "1e4←1")
        action.take(state, mutate=True)  # Current player is white
        self.assertEqual(state.board.get_stack(4, 3).height(), 1)
        self.assertEqual(state.board.get_stack(3, 3).height(), 1)
        self.assertEqual(state.board.get_stack(4, 3).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(3, 3).top(), TakPiece.WHITE_CAPSTONE)

    def test_tak_action_move_get_ending_position(self):
        move_up_1 = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertEqual(move_up_1.get_ending_position(), (0, 1))
        move_right_11 = TakActionMove((1, 5), TakActionMoveDir.RIGHT, (1, 1))
        self.assertEqual(move_right_11.get_ending_position(), (3, 5))
        move_down_1121 = TakActionMove((1, 5), TakActionMoveDir.DOWN, (1, 1, 2, 1))
        self.assertEqual(move_down_1121.get_ending_position(), (1, 1))

    def test_tak_action_move_pick_up_count(self):
        move_up_1 = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertEqual(move_up_1.pick_up_count(), 1)
        move_right_11 = TakActionMove((1, 5), TakActionMoveDir.RIGHT, (1, 1))
        self.assertEqual(move_right_11.pick_up_count(), 2)
        move_down_1121 = TakActionMove((1, 5), TakActionMoveDir.DOWN, (1, 1, 2, 1))
        self.assertEqual(move_down_1121.pick_up_count(), 5)

    def test_tak_action_move_str(self):
        move_up_1 = TakActionMove((0, 0), TakActionMoveDir.UP, (1,))
        self.assertEqual(str(move_up_1), "1a1↑1")
        move_right_11 = TakActionMove((1, 5), TakActionMoveDir.RIGHT, (1, 1))
        self.assertEqual(str(move_right_11), "2b6→11")
        move_down_1121 = TakActionMove((1, 5), TakActionMoveDir.DOWN, (1, 1, 2, 1))
        self.assertEqual(str(move_down_1121), "5b6↓1121")

    def test_tak_action_move_get_possible_move_actions(self):
        pass  # TODO: test

    def test_tak_action_move_get_possible_move_actions_for_position(self):
        pass  # TODO: test

    def test_tak_action_move_get_possible_drop_orders(self):
        # See test for ordered_partitions util
        self.assertEqual(1, len(set(TakActionMove.get_possible_drop_orders(1))))
        self.assertEqual(2, len(set(TakActionMove.get_possible_drop_orders(2))))
        self.assertEqual(4, len(set(TakActionMove.get_possible_drop_orders(3))))
        self.assertEqual(8, len(set(TakActionMove.get_possible_drop_orders(4))))
        self.assertEqual(16, len(set(TakActionMove.get_possible_drop_orders(5))))
        self.assertEqual(32, len(set(TakActionMove.get_possible_drop_orders(6))))
        self.assertEqual(64, len(set(TakActionMove.get_possible_drop_orders(7))))
        self.assertEqual(128, len(set(TakActionMove.get_possible_drop_orders(8))))
        self.assertEqual(256, len(set(TakActionMove.get_possible_drop_orders(9))))
        self.assertEqual(512, len(set(TakActionMove.get_possible_drop_orders(10))))
        self.assertEqual(1024, len(set(TakActionMove.get_possible_drop_orders(11))))
        # self.assertEqual(2**19, len(set(TakActionMove.get_possible_drop_orders(20))))

        # Wow, the count is 2^(n-1) !


if __name__ == '__main__':
    unittest.main()
