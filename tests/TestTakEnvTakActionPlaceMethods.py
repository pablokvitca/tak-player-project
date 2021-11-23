import unittest

from tak_env.TakAction import TakActionPlace
from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TestTakEnvTakActionPlaceMethods(unittest.TestCase):

    def test_tak_action_place_init(self):
        self.assertEqual(TakActionPlace((0, 0), TakPiece.WHITE_FLAT).piece, TakPiece.WHITE_FLAT)
        self.assertEqual(TakActionPlace((0, 0), TakPiece.BLACK_FLAT).piece, TakPiece.BLACK_FLAT)
        self.assertEqual(TakActionPlace((0, 0), TakPiece.WHITE_STANDING).piece, TakPiece.WHITE_STANDING)
        self.assertEqual(TakActionPlace((0, 0), TakPiece.BLACK_STANDING).piece, TakPiece.BLACK_STANDING)
        self.assertEqual(TakActionPlace((0, 0), TakPiece.WHITE_CAPSTONE).piece, TakPiece.WHITE_CAPSTONE)
        self.assertEqual(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE).piece, TakPiece.BLACK_CAPSTONE)

    def test_tak_action_place_is_valid(self):
        state = TakState(4, TakBoard(4), 5, 5, False, False, TakPlayer.WHITE)
        self.assertFalse(TakActionPlace((0, 0), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertTrue(TakActionPlace((0, 1), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 2), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((1, 1), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((2, 1), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE).is_valid(state))
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.current_player = TakPlayer.BLACK
        self.assertTrue(TakActionPlace((0, 1), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 1), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 2), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((1, 1), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((2, 1), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE).is_valid(state))
        state.board.place_piece((3, 2), TakPiece.WHITE_FLAT)
        state.current_player = TakPlayer.WHITE
        self.assertTrue(TakActionPlace((0, 1), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 1), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertTrue(TakActionPlace((0, 2), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((1, 1), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((2, 1), TakPiece.WHITE_CAPSTONE).is_valid(state))
        state.white_capstone_available = True
        self.assertTrue(TakActionPlace((2, 1), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE).is_valid(state))

        state = TakState(5, TakBoard(5), 11, 11, True, True, TakPlayer.BLACK)
        state.board.place_piece((4, 3), TakPiece.WHITE_FLAT)
        state.board.place_piece((4, 4), TakPiece.BLACK_FLAT)
        self.assertTrue(TakActionPlace((0, 1), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertTrue(TakActionPlace((1, 4), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertTrue(TakActionPlace((1, 0), TakPiece.BLACK_CAPSTONE).is_valid(state))
        state.current_player = TakPlayer.WHITE
        self.assertTrue(TakActionPlace((0, 0), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertTrue(TakActionPlace((3, 2), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertTrue(TakActionPlace((2, 1), TakPiece.WHITE_CAPSTONE).is_valid(state))

        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((1, 1), TakPiece.WHITE_FLAT)
        self.assertFalse(TakActionPlace((0, 0), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE).is_valid(state))

        state = TakState(5, TakBoard(5), 0, 1, True, False, TakPlayer.WHITE)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((1, 1), TakPiece.WHITE_FLAT)
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertTrue(TakActionPlace((3, 3), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_CAPSTONE).is_valid(state))
        state.current_player = TakPlayer.BLACK
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertTrue(TakActionPlace((3, 3), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertTrue(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_CAPSTONE).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_CAPSTONE).is_valid(state))

        state = TakState(5, TakBoard(5), 0, 0, False, False, TakPlayer.WHITE)
        state.board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        state.board.place_piece((1, 1), TakPiece.WHITE_FLAT)
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))
        state.current_player = TakPlayer.BLACK
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_FLAT).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.WHITE_STANDING).is_valid(state))
        self.assertFalse(TakActionPlace((3, 3), TakPiece.BLACK_STANDING).is_valid(state))

    def test_tak_action_place_take(self):
        state = TakState(5, TakBoard(5), 11, 10, True, True, TakPlayer.WHITE)
        self.assertEqual(state.white_pieces_available, 11)
        self.assertEqual(state.black_pieces_available, 10)
        self.assertEqual(state.white_capstone_available, True)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.WHITE)
        self.assertTrue(state.first_action())
        action = TakActionPlace((0, 0), TakPiece.BLACK_FLAT)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.white_pieces_available, 11)
        self.assertEqual(state.black_pieces_available, 9)
        self.assertEqual(state.white_capstone_available, True)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.BLACK)
        self.assertTrue(state.first_action())
        action = TakActionPlace((1, 2), TakPiece.WHITE_FLAT)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.white_pieces_available, 10)
        self.assertEqual(state.black_pieces_available, 9)
        self.assertEqual(state.white_capstone_available, True)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.WHITE)
        self.assertFalse(state.first_action())
        action = TakActionPlace((2, 2), TakPiece.WHITE_FLAT)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.white_pieces_available, 9)
        self.assertEqual(state.black_pieces_available, 9)
        self.assertEqual(state.white_capstone_available, True)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.BLACK)
        self.assertFalse(state.first_action())
        action = TakActionPlace((2, 3), TakPiece.BLACK_STANDING)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 3).top(), TakPiece.BLACK_STANDING)
        self.assertEqual(state.white_pieces_available, 9)
        self.assertEqual(state.black_pieces_available, 8)
        self.assertEqual(state.white_capstone_available, True)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.WHITE)
        self.assertFalse(state.first_action())
        action = TakActionPlace((3, 3), TakPiece.WHITE_CAPSTONE)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 3).top(), TakPiece.BLACK_STANDING)
        self.assertEqual(state.board.get_stack(3, 3).top(), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(state.white_pieces_available, 9)
        self.assertEqual(state.black_pieces_available, 8)
        self.assertEqual(state.white_capstone_available, False)
        self.assertEqual(state.black_capstone_available, True)
        self.assertEqual(state.current_player, TakPlayer.BLACK)
        self.assertFalse(state.first_action())
        action = TakActionPlace((1, 1), TakPiece.BLACK_CAPSTONE)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 3).top(), TakPiece.BLACK_STANDING)
        self.assertEqual(state.board.get_stack(3, 3).top(), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(state.board.get_stack(1, 1).top(), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(state.white_pieces_available, 9)
        self.assertEqual(state.black_pieces_available, 8)
        self.assertEqual(state.white_capstone_available, False)
        self.assertEqual(state.black_capstone_available, False)
        self.assertEqual(state.current_player, TakPlayer.WHITE)
        self.assertFalse(state.first_action())
        action = TakActionPlace((3, 0), TakPiece.WHITE_STANDING)
        action.take(state)
        self.assertEqual(state.board.get_stack(0, 0).top(), TakPiece.BLACK_FLAT)
        self.assertEqual(state.board.get_stack(1, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 2).top(), TakPiece.WHITE_FLAT)
        self.assertEqual(state.board.get_stack(2, 3).top(), TakPiece.BLACK_STANDING)
        self.assertEqual(state.board.get_stack(3, 3).top(), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(state.board.get_stack(1, 1).top(), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(state.board.get_stack(3, 0).top(), TakPiece.WHITE_STANDING)
        self.assertEqual(state.white_pieces_available, 8)
        self.assertEqual(state.black_pieces_available, 8)
        self.assertEqual(state.white_capstone_available, False)
        self.assertEqual(state.black_capstone_available, False)
        self.assertEqual(state.current_player, TakPlayer.BLACK)
        self.assertFalse(state.first_action())

    def test_tak_action_place_str(self):
        self.assertEqual(str(TakActionPlace((0, 0), TakPiece.WHITE_FLAT)), "Fa1")
        self.assertEqual(str(TakActionPlace((3, 2), TakPiece.BLACK_FLAT)), "Fd3")
        self.assertEqual(str(TakActionPlace((1, 1), TakPiece.WHITE_STANDING)), "Sb2")
        self.assertEqual(str(TakActionPlace((0, 4), TakPiece.BLACK_STANDING)), "Sa5")
        self.assertEqual(str(TakActionPlace((1, 1), TakPiece.WHITE_CAPSTONE)), "Cb2")
        self.assertEqual(str(TakActionPlace((0, 4), TakPiece.BLACK_CAPSTONE)), "Ca5")

    def test_tak_action_place_get_possible_place_actions(self):
        state = TakState(5, TakBoard(5), 11, 10, True, True, TakPlayer.WHITE)
        actual = TakActionPlace.get_possible_place_actions(state, TakPiece.BLACK_FLAT)
        self.assertEqual(len(actual), 5 * 5)
        self.assertEqual(len(set(actual)), 5 * 5)
        self.assertTrue(all(action.piece == TakPiece.BLACK_FLAT for action in actual))

        action = TakActionPlace((0, 0), TakPiece.BLACK_FLAT)
        action.take(state)
        actual = TakActionPlace.get_possible_place_actions(state, TakPiece.WHITE_FLAT)
        self.assertEqual(len(actual), 5 * 5 - 1)
        self.assertEqual(len(set(actual)), 5 * 5 - 1)
        self.assertTrue(all(action.piece == TakPiece.WHITE_FLAT for action in actual))
        self.assertTrue(TakActionPlace((0, 0), TakPiece.WHITE_FLAT) not in actual)

        action = TakActionPlace((1, 2), TakPiece.WHITE_FLAT)
        action.take(state)
        actual = TakActionPlace.get_possible_place_actions(state, TakPiece.WHITE_STANDING)
        self.assertEqual(len(actual), 5 * 5 - 2)
        self.assertEqual(len(set(actual)), 5 * 5 - 2)
        self.assertTrue(all(action.piece == TakPiece.WHITE_STANDING for action in actual))
        self.assertTrue(TakActionPlace((0, 0), TakPiece.WHITE_STANDING) not in actual)
        self.assertTrue(TakActionPlace((1, 2), TakPiece.WHITE_STANDING) not in actual)
        actual = TakActionPlace.get_possible_place_actions(state, TakPiece.BLACK_CAPSTONE)
        self.assertEqual(len(actual), 5 * 5 - 2)
        self.assertEqual(len(set(actual)), 5 * 5 - 2)
        self.assertTrue(all(action.piece == TakPiece.BLACK_CAPSTONE for action in actual))
        self.assertTrue(TakActionPlace((0, 0), TakPiece.BLACK_CAPSTONE) not in actual)
        self.assertTrue(TakActionPlace((1, 2), TakPiece.BLACK_CAPSTONE) not in actual)


if __name__ == '__main__':
    unittest.main()
