import unittest

import numpy as np

from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakStack import PieceStack


class TestTakEnvTakActionMethods(unittest.TestCase):
    pass


class TestTakEnvTakBoardMethods(unittest.TestCase):

    def test_tak_board_init(self):
        for board_size in range(3, 10):
            board = TakBoard(board_size)
            self.assertEqual(len(board.board), board_size)
            self.assertTrue(all([len(board.board[i]) == board_size for i in range(len(board.board))]))
            self.assertEqual(len(board._positions_iterable), board_size * board_size)

    def test_tak_total_pieces(self):
        board = TakBoard(3)
        self.assertEqual(board.total_pieces(), 0)
        board.place_piece((0, 0), TakPiece.WHITE_FLAT)
        self.assertEqual(board.total_pieces(), 1)
        board.place_piece((1, 0), TakPiece.WHITE_FLAT)
        self.assertEqual(board.total_pieces(), 2)
        board.place_piece((1, 0), TakPiece.WHITE_FLAT)
        self.assertEqual(board.total_pieces(), 3)
        board.place_piece((1, 0), TakPiece.BLACK_FLAT)
        self.assertEqual(board.total_pieces(), 4)
        board.place_piece((2, 2), TakPiece.BLACK_STANDING)
        self.assertEqual(board.total_pieces(), 5)
        board.place_piece((1, 0), TakPiece.WHITE_STANDING)
        self.assertEqual(board.total_pieces(), 6)
        board.place_piece((1, 0), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(board.total_pieces(), 7)
        board.place_piece((1, 1), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(board.total_pieces(), 8)

    def test_tak_board_get_board_names_str(self):
        self.assertEqual(
            TakBoard(3).get_board_names_str(),
            "\n".join([
                "a3 b3 c3",
                "a2 b2 c2",
                "a1 b1 c1"
            ])
        )
        self.assertEqual(
            TakBoard(4).get_board_names_str(),
            "\n".join([
              "a4 b4 c4 d4",
              "a3 b3 c3 d3",
              "a2 b2 c2 d2",
              "a1 b1 c1 d1"
            ])
        )
        self.assertEqual(
            TakBoard(7).get_board_names_str(),
            "\n".join([
                "a7 b7 c7 d7 e7 f7 g7",
                "a6 b6 c6 d6 e6 f6 g6",
                "a5 b5 c5 d5 e5 f5 g5",
                "a4 b4 c4 d4 e4 f4 g4",
                "a3 b3 c3 d3 e3 f3 g3",
                "a2 b2 c2 d2 e2 f2 g2",
                "a1 b1 c1 d1 e1 f1 g1"
            ])
        )

    def test_tak_board_get_board_str(self):
        self.assertEqual(
            str(TakBoard(4)),
            "\n".join([
                "_ _ _ _",
                "_ _ _ _",
                "_ _ _ _",
                "_ _ _ _"
            ])
        )
        board = TakBoard(3)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ _ _",
                "_ _ _",
                "_ _ _"
            ])
        )
        board.place_piece((0, 0), TakPiece.WHITE_FLAT)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ _ _",
                "_ _ _",
                "F _ _"
            ])
        )
        board.place_piece((0, 0), TakPiece.WHITE_FLAT)
        board.place_piece((0, 0), TakPiece.BLACK_FLAT)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ _ _",
                "_ _ _",
                "f _ _"
            ])
        )
        board.place_piece((0, 0), TakPiece.BLACK_STANDING)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ _ _",
                "_ _ _",
                "s _ _"
            ])
        )
        board.place_piece((0, 0), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ _ _",
                "_ _ _",
                "C _ _"
            ])
        )
        board.place_piece((1, 2), TakPiece.BLACK_CAPSTONE)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ c _",
                "_ _ _",
                "C _ _"
            ])
        )
        board.place_piece((2, 1), TakPiece.WHITE_STANDING)
        self.assertEqual(
            str(board),
            "\n".join([
                "_ c _",
                "_ _ S",
                "C _ _"
            ])
        )

    def test_tak_board_get_square_name(self):
        self.assertEqual(TakBoard.get_square_name((0, 0)), "a1")
        self.assertEqual(TakBoard.get_square_name((1, 0)), "b1")
        self.assertEqual(TakBoard.get_square_name((2, 0)), "c1")
        self.assertEqual(TakBoard.get_square_name((0, 1)), "a2")
        self.assertEqual(TakBoard.get_square_name((1, 1)), "b2")
        self.assertEqual(TakBoard.get_square_name((2, 1)), "c2")
        self.assertEqual(TakBoard.get_square_name((0, 2)), "a3")
        self.assertEqual(TakBoard.get_square_name((1, 2)), "b3")
        self.assertEqual(TakBoard.get_square_name((2, 2)), "c3")

    def assertNumpyArrayEqual(self, expected: np.array, actual: np.array):
        np.testing.assert_array_equal(expected, actual)

    def test_tak_board_get_as_3d_matrix(self):
        board = TakBoard(6)
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], np.zeros((6, 6, 1), dtype=np.int))
        board = TakBoard(3)
        expected_matrix = np.zeros((3, 3, 1), dtype=np.int)
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], np.zeros((3, 3, 1), dtype=np.int))
        board.place_piece((1, 1), TakPiece.WHITE_FLAT)
        expected_matrix[1, 1, 0] = 1
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.BLACK_FLAT)
        expected_matrix[1, 0, 0] = -1
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.WHITE_STANDING)
        expected_matrix = np.zeros((3, 3, 2), dtype=np.int)
        expected_matrix[1, 1, 0] = 1
        expected_matrix[1, 0, 0] = -1
        expected_matrix[1, 0, 1] = 2
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.BLACK_CAPSTONE)
        expected_matrix = np.zeros((3, 3, 3), dtype=np.int)
        expected_matrix[1, 1, 0] = 1
        expected_matrix[1, 0, 0] = -1
        expected_matrix[1, 0, 1] = 1
        expected_matrix[1, 0, 2] = -3
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)

    def test_tak_board_is_position_in_board(self):
        board = TakBoard(3)
        self.assertTrue(board.is_position_in_board((0, 0)))
        self.assertTrue(board.is_position_in_board((1, 1)))
        self.assertTrue(board.is_position_in_board((2, 2)))
        self.assertFalse(board.is_position_in_board((-1, 0)))
        self.assertFalse(board.is_position_in_board((0, -1)))
        self.assertFalse(board.is_position_in_board((3, 0)))
        self.assertFalse(board.is_position_in_board((0, 3)))

        board = TakBoard(4)
        self.assertTrue(board.is_position_in_board((0, 0)))
        self.assertTrue(board.is_position_in_board((1, 1)))
        self.assertTrue(board.is_position_in_board((2, 2)))
        self.assertFalse(board.is_position_in_board((-1, 0)))
        self.assertFalse(board.is_position_in_board((0, -1)))
        self.assertTrue(board.is_position_in_board((3, 0)))
        self.assertTrue(board.is_position_in_board((0, 3)))
        self.assertFalse(board.is_position_in_board((4, 0)))
        self.assertFalse(board.is_position_in_board((0, 4)))


class TestTakEnvTakEnvironmentMethods(unittest.TestCase):
    pass


class TestTakEnvTakPieceMethods(unittest.TestCase):

    def test_tak_piece_flat_value(self):
        flat_piece_value = 1
        self.assertEqual(TakPiece._flat(), flat_piece_value)
        self.assertEqual(abs(TakPiece.WHITE_FLAT.value), flat_piece_value)
        self.assertEqual(abs(TakPiece.BLACK_FLAT.value), flat_piece_value)
        self.assertEqual(TakPiece.WHITE_FLAT.abs_value(), flat_piece_value)
        self.assertEqual(TakPiece.BLACK_FLAT.abs_value(), flat_piece_value)

    def test_tak_piece_standing_value(self):
        standing_piece_value = 2
        self.assertEqual(TakPiece._standing(), standing_piece_value)
        self.assertEqual(abs(TakPiece.WHITE_STANDING.value), standing_piece_value)
        self.assertEqual(abs(TakPiece.BLACK_STANDING.value), standing_piece_value)
        self.assertEqual(TakPiece.WHITE_STANDING.abs_value(), standing_piece_value)
        self.assertEqual(TakPiece.BLACK_STANDING.abs_value(), standing_piece_value)

    def test_tak_piece_capstone_value(self):
        capstone_piece_value = 3
        self.assertEqual(TakPiece._capstone(), capstone_piece_value)
        self.assertEqual(abs(TakPiece.WHITE_CAPSTONE.value), capstone_piece_value)
        self.assertEqual(abs(TakPiece.BLACK_CAPSTONE.value), capstone_piece_value)
        self.assertEqual(TakPiece.WHITE_CAPSTONE.abs_value(), capstone_piece_value)
        self.assertEqual(TakPiece.BLACK_CAPSTONE.abs_value(), capstone_piece_value)

    def test_tak_piece_get_all_pieces(self):
        all_pieces = TakPiece.get_all_pieces()
        self.assertEqual(len(all_pieces), 6)
        self.assertEqual(len(all_pieces), len(set(all_pieces)))

    def test_tak_piece_get_white_pieces(self):
        all_pieces = TakPiece.get_white_pieces()
        self.assertEqual(len(all_pieces), 3)
        self.assertEqual(len(all_pieces), len(set(all_pieces)))
        self.assertTrue(all(piece.player() == TakPlayer.WHITE for piece in all_pieces))
        self.assertTrue(all(piece.value > 0 for piece in all_pieces))

    def test_tak_piece_get_black_pieces(self):
        all_pieces = TakPiece.get_black_pieces()
        self.assertEqual(len(all_pieces), 3)
        self.assertEqual(len(all_pieces), len(set(all_pieces)))
        self.assertTrue(all(piece.player() == TakPlayer.BLACK for piece in all_pieces))
        self.assertTrue(all(piece.value < 0 for piece in all_pieces))

    def test_tak_piece_is_flat(self):
        self.assertTrue(TakPiece.WHITE_FLAT.is_flat())
        self.assertTrue(TakPiece.BLACK_FLAT.is_flat())
        self.assertFalse(TakPiece.WHITE_STANDING.is_flat())
        self.assertFalse(TakPiece.BLACK_STANDING.is_flat())
        self.assertFalse(TakPiece.WHITE_CAPSTONE.is_flat())
        self.assertFalse(TakPiece.BLACK_CAPSTONE.is_flat())

    def test_tak_piece_is_standing(self):
        self.assertFalse(TakPiece.WHITE_FLAT.is_standing())
        self.assertFalse(TakPiece.BLACK_FLAT.is_standing())
        self.assertTrue(TakPiece.WHITE_STANDING.is_standing())
        self.assertTrue(TakPiece.BLACK_STANDING.is_standing())
        self.assertFalse(TakPiece.WHITE_CAPSTONE.is_standing())
        self.assertFalse(TakPiece.BLACK_CAPSTONE.is_standing())

    def test_tak_piece_is_capstone(self):
        self.assertFalse(TakPiece.WHITE_FLAT.is_capstone())
        self.assertFalse(TakPiece.BLACK_FLAT.is_capstone())
        self.assertFalse(TakPiece.WHITE_STANDING.is_capstone())
        self.assertFalse(TakPiece.BLACK_STANDING.is_capstone())
        self.assertTrue(TakPiece.WHITE_CAPSTONE.is_capstone())
        self.assertTrue(TakPiece.BLACK_CAPSTONE.is_capstone())

    def test_task_piece_is_road(self):
        self.assertTrue(TakPiece.WHITE_FLAT.is_road())
        self.assertTrue(TakPiece.BLACK_FLAT.is_road())
        self.assertFalse(TakPiece.WHITE_STANDING.is_road())
        self.assertFalse(TakPiece.BLACK_STANDING.is_road())
        self.assertTrue(TakPiece.WHITE_CAPSTONE.is_road())
        self.assertTrue(TakPiece.BLACK_CAPSTONE.is_road())

    def test_tak_piece_can_place_on(self):
        self.assertTrue(TakPiece.WHITE_FLAT.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.WHITE_FLAT.can_place_on(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.WHITE_FLAT.can_place_on(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.WHITE_FLAT.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.WHITE_FLAT.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.WHITE_FLAT.can_place_on(TakPiece.BLACK_CAPSTONE))

        self.assertTrue(TakPiece.BLACK_FLAT.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.BLACK_FLAT.can_place_on(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.BLACK_FLAT.can_place_on(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.BLACK_FLAT.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.BLACK_FLAT.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.BLACK_FLAT.can_place_on(TakPiece.BLACK_CAPSTONE))

        self.assertTrue(TakPiece.WHITE_STANDING.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.WHITE_STANDING.can_place_on(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.WHITE_STANDING.can_place_on(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.WHITE_STANDING.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.WHITE_STANDING.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.WHITE_STANDING.can_place_on(TakPiece.BLACK_CAPSTONE))

        self.assertTrue(TakPiece.BLACK_STANDING.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.BLACK_STANDING.can_place_on(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.BLACK_STANDING.can_place_on(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.BLACK_STANDING.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.BLACK_STANDING.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.BLACK_STANDING.can_place_on(TakPiece.BLACK_CAPSTONE))

        self.assertTrue(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.BLACK_FLAT))
        self.assertTrue(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.WHITE_STANDING))
        self.assertTrue(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.can_place_on(TakPiece.BLACK_CAPSTONE))

        self.assertTrue(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.WHITE_FLAT))
        self.assertTrue(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.BLACK_FLAT))
        self.assertTrue(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.WHITE_STANDING))
        self.assertTrue(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.can_place_on(TakPiece.BLACK_CAPSTONE))

    def test_tak_piece_will_flatter(self):
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.WHITE_FLAT.will_flatten(TakPiece.BLACK_CAPSTONE))

        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.BLACK_FLAT.will_flatten(TakPiece.BLACK_CAPSTONE))

        self.assertFalse(TakPiece.WHITE_STANDING.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.WHITE_STANDING.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.WHITE_STANDING.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.WHITE_STANDING.will_flatten(TakPiece.BLACK_STANDING))
        self.assertTrue(TakPiece.WHITE_STANDING.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(TakPiece.WHITE_STANDING.will_flatten(TakPiece.BLACK_CAPSTONE))

        self.assertFalse(TakPiece.BLACK_STANDING.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.BLACK_STANDING.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.BLACK_STANDING.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.BLACK_STANDING.will_flatten(TakPiece.BLACK_STANDING))
        self.assertTrue(TakPiece.BLACK_STANDING.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(TakPiece.BLACK_STANDING.will_flatten(TakPiece.BLACK_CAPSTONE))

        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.WHITE_CAPSTONE.will_flatten(TakPiece.BLACK_CAPSTONE))

        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.WHITE_FLAT))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.BLACK_FLAT))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.WHITE_STANDING))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.BLACK_STANDING))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(TakPiece.BLACK_CAPSTONE.will_flatten(TakPiece.BLACK_CAPSTONE))

    def test_tak_piece_flatten(self):
        self.assertEqual(TakPiece.WHITE_FLAT.flatten(), TakPiece.WHITE_FLAT)
        self.assertEqual(TakPiece.BLACK_FLAT.flatten(), TakPiece.BLACK_FLAT)
        self.assertEqual(TakPiece.WHITE_STANDING.flatten(), TakPiece.WHITE_FLAT)
        self.assertEqual(TakPiece.BLACK_STANDING.flatten(), TakPiece.BLACK_FLAT)
        self.assertEqual(TakPiece.WHITE_CAPSTONE.flatten(), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(TakPiece.BLACK_CAPSTONE.flatten(), TakPiece.BLACK_CAPSTONE)

    def test_tak_piece_get_piece_for_player(self):
        self.assertEqual(TakPiece.get_piece_for_player(1, TakPlayer.WHITE), TakPiece.WHITE_FLAT)
        self.assertEqual(TakPiece.get_piece_for_player(1, TakPlayer.BLACK), TakPiece.BLACK_FLAT)
        self.assertEqual(TakPiece.get_piece_for_player(2, TakPlayer.WHITE), TakPiece.WHITE_STANDING)
        self.assertEqual(TakPiece.get_piece_for_player(2, TakPlayer.BLACK), TakPiece.BLACK_STANDING)
        self.assertEqual(TakPiece.get_piece_for_player(3, TakPlayer.WHITE), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(TakPiece.get_piece_for_player(3, TakPlayer.BLACK), TakPiece.BLACK_CAPSTONE)

    def test_tak_piece_get_flat_piece_for_player(self):
        self.assertEqual(TakPiece.get_flat_piece_for_player(TakPlayer.WHITE), TakPiece.WHITE_FLAT)
        self.assertEqual(TakPiece.get_flat_piece_for_player(TakPlayer.BLACK), TakPiece.BLACK_FLAT)

    def get_standing_piece_for_player(self):
        self.assertEqual(TakPiece.get_standing_piece_for_player(TakPlayer.WHITE), TakPiece.WHITE_STANDING)
        self.assertEqual(TakPiece.get_standing_piece_for_player(TakPlayer.BLACK), TakPiece.BLACK_STANDING)

    def test_tak_piece_get_capstone_piece_for_player(self):
        self.assertEqual(TakPiece.get_capstone_piece_for_player(TakPlayer.WHITE), TakPiece.WHITE_CAPSTONE)
        self.assertEqual(TakPiece.get_capstone_piece_for_player(TakPlayer.BLACK), TakPiece.BLACK_CAPSTONE)

    def test_tak_piece_type(self):
        self.assertEqual(TakPiece.WHITE_FLAT.type(), 'flat')
        self.assertEqual(TakPiece.BLACK_FLAT.type(), 'flat')
        self.assertEqual(TakPiece.WHITE_STANDING.type(), 'standing')
        self.assertEqual(TakPiece.BLACK_STANDING.type(), 'standing')
        self.assertEqual(TakPiece.WHITE_CAPSTONE.type(), 'capstone')
        self.assertEqual(TakPiece.BLACK_CAPSTONE.type(), 'capstone')

    def test_tak_piece_player(self):
        self.assertEqual(TakPiece.WHITE_FLAT.player(), TakPlayer.WHITE)
        self.assertEqual(TakPiece.BLACK_FLAT.player(), TakPlayer.BLACK)
        self.assertEqual(TakPiece.WHITE_STANDING.player(), TakPlayer.WHITE)
        self.assertEqual(TakPiece.BLACK_STANDING.player(), TakPlayer.BLACK)
        self.assertEqual(TakPiece.WHITE_CAPSTONE.player(), TakPlayer.WHITE)
        self.assertEqual(TakPiece.BLACK_CAPSTONE.player(), TakPlayer.BLACK)

    def test_tak_piece_view_str(self):
        self.assertEqual(TakPiece.WHITE_FLAT.view_str(), 'F')
        self.assertEqual(TakPiece.BLACK_FLAT.view_str(), 'f')
        self.assertEqual(TakPiece.WHITE_STANDING.view_str(), 'S')
        self.assertEqual(TakPiece.BLACK_STANDING.view_str(), 's')
        self.assertEqual(TakPiece.WHITE_CAPSTONE.view_str(), 'C')
        self.assertEqual(TakPiece.BLACK_CAPSTONE.view_str(), 'c')

    def test_tak_piece_str(self):
        self.assertEqual(str(TakPiece.WHITE_FLAT), 'white_flat')
        self.assertEqual(str(TakPiece.BLACK_FLAT), 'black_flat')
        self.assertEqual(str(TakPiece.WHITE_STANDING), 'white_standing')
        self.assertEqual(str(TakPiece.BLACK_STANDING), 'black_standing')
        self.assertEqual(str(TakPiece.WHITE_CAPSTONE), 'white_capstone')
        self.assertEqual(str(TakPiece.BLACK_CAPSTONE), 'black_capstone')


class TestTakEnvTakPlayerMethods(unittest.TestCase):

    def test_tak_player_value(self):
        self.assertEqual(TakPlayer.WHITE.value, "white")
        self.assertEqual(TakPlayer.BLACK.value, "black")

    def test_tak_player_opponent(self):
        self.assertEqual(TakPlayer.WHITE.other(), TakPlayer.BLACK)
        self.assertEqual(TakPlayer.BLACK.other(), TakPlayer.WHITE)

    def test_tak_player_str(self):
        self.assertEqual(str(TakPlayer.WHITE), "white")
        self.assertEqual(str(TakPlayer.BLACK), "black")


class TestTakEnvTakStackMethods(unittest.TestCase):

    def test_tak_stack_init(self):
        stack = PieceStack()
        self.assertEqual(len(stack), 0)
        self.assertEqual(stack.height(), 0)
        self.assertEqual(stack.is_empty(), True)
        self.assertEqual(len(stack.stack), 0)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack.height(), 1)
        self.assertEqual(stack.is_empty(), False)
        self.assertEqual(len(stack.stack), 1)
        self.assertEqual(stack.stack[0], TakPiece.WHITE_FLAT)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING))
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.height(), 2)
        self.assertEqual(stack.is_empty(), False)
        self.assertEqual(len(stack.stack), 2)
        self.assertEqual(stack.stack[0], TakPiece.WHITE_FLAT)
        self.assertEqual(stack.stack[1], TakPiece.BLACK_STANDING)
        self.assertEqual(stack.top(), TakPiece.BLACK_STANDING)

    def test_tak_stack_push(self):
        stack = PieceStack()
        self.assertTrue(stack.is_empty())
        stack.push(TakPiece.WHITE_FLAT)
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 1)
        self.assertEqual(stack.top(), TakPiece.WHITE_FLAT)

        stack.push(TakPiece.BLACK_CAPSTONE)
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 2)
        self.assertEqual(stack.top(), TakPiece.BLACK_CAPSTONE)

        self.assertRaises(ValueError, stack.push, TakPiece.WHITE_FLAT, False)
        self.assertRaises(ValueError, stack.push, TakPiece.WHITE_CAPSTONE, False)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertFalse(stack.is_empty())
        self.assertEqual(stack.height(), 1)
        stack.push(TakPiece.WHITE_STANDING)
        self.assertEqual(stack.height(), 2)
        self.assertRaises(ValueError, stack.push, TakPiece.WHITE_FLAT, False)
        self.assertEqual(stack.height(), 2)
        self.assertEqual(stack.as_list(), [TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING])
        stack.push(TakPiece.WHITE_CAPSTONE)
        self.assertEqual(stack.height(), 3)
        self.assertEqual(stack.as_list(), [TakPiece.WHITE_FLAT, TakPiece.WHITE_FLAT, TakPiece.WHITE_CAPSTONE])

    def test_tak_push_stack(self):
        stack = PieceStack()
        self.assertTrue(stack.is_empty())
        stack.push_stack(PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT)))
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 2)
        self.assertEqual(stack.top(), TakPiece.BLACK_FLAT)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertFalse(stack.is_empty())
        stack.push_stack(PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT)))
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 3)
        self.assertEqual(stack.top(), TakPiece.BLACK_FLAT)

    def test_tak_push_many(self):
        stack = PieceStack()
        self.assertTrue(stack.is_empty())
        stack.push_many([TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 2)
        self.assertEqual(stack.top(), TakPiece.BLACK_FLAT)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertFalse(stack.is_empty())
        stack.push_many([TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack.stack), 3)
        self.assertEqual(stack.top(), TakPiece.BLACK_FLAT)

    def test_tak_stack_pop(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.pop(), TakPiece.BLACK_FLAT)
        self.assertEqual(stack.pop(), TakPiece.WHITE_FLAT)
        self.assertTrue(stack.is_empty())

        stack = PieceStack()
        self.assertRaises(ValueError, stack.pop)

    def test_tak_stack_pop_many(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.pop_many(2), [TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT])
        self.assertTrue(stack.is_empty())

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.pop_many(1), [TakPiece.BLACK_FLAT])
        self.assertFalse(stack.is_empty())

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_STANDING))
        self.assertEqual(stack.pop_many(2), [TakPiece.WHITE_STANDING, TakPiece.BLACK_FLAT])
        self.assertFalse(stack.is_empty())

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_STANDING))
        self.assertEqual(stack.pop_many(4), [TakPiece.WHITE_STANDING, TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT])
        self.assertTrue(stack.is_empty())

        stack = PieceStack()
        self.assertEqual(stack.pop_many(1), [])
        self.assertEqual(stack.pop_many(3), [])

    def test_tak_stack_top(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.top(), TakPiece.BLACK_FLAT)

        stack = PieceStack()
        self.assertRaises(IndexError, stack.top)

    def test_tak_stack_top_n(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.top_n(1), [TakPiece.BLACK_FLAT])
        self.assertEqual(stack.top_n(2), [TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])
        self.assertEqual(stack.top_n(3), [TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])

        stack = PieceStack()
        self.assertEqual(stack.top_n(1), [])
        self.assertEqual(stack.top_n(3), [])

    def test_tak_stack_controlled_by(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.controlled_by(), TakPlayer.BLACK)
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING))
        self.assertEqual(stack.controlled_by(), TakPlayer.BLACK)
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.BLACK_STANDING))
        self.assertEqual(stack.controlled_by(), TakPlayer.BLACK)
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertEqual(stack.controlled_by(), TakPlayer.BLACK)

        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT))
        self.assertEqual(stack.controlled_by(), TakPlayer.WHITE)
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.WHITE_STANDING))
        self.assertEqual(stack.controlled_by(), TakPlayer.WHITE)
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING))
        self.assertEqual(stack.controlled_by(), TakPlayer.WHITE)
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.WHITE_STANDING))
        self.assertEqual(stack.controlled_by(), TakPlayer.WHITE)

        stack = PieceStack()
        self.assertIsNone(stack.controlled_by())

    def test_tak_stack_is_controlled_by(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE))
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK))
        stack = PieceStack(stack=(TakPiece.WHITE_CAPSTONE,))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK))

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_CAPSTONE,))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE, only_road_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_road_pieces=True))

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_FLAT))
        self.assertTrue(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.WHITE_STANDING))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))
        stack = PieceStack(stack=(TakPiece.WHITE_CAPSTONE,))
        self.assertFalse(stack.is_controlled_by(TakPlayer.WHITE, only_flat_pieces=True))
        self.assertFalse(stack.is_controlled_by(TakPlayer.BLACK, only_flat_pieces=True))

    def test_tak_stack_as_list(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.as_list(), [TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT])

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE))
        self.assertEqual(stack.as_list(), [TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE])

        stack = PieceStack()
        self.assertEqual(stack.as_list(), [])

    def test_tak_stack_is_empty(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, ))
        self.assertFalse(stack.is_empty())

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE))
        self.assertFalse(stack.is_empty())

        stack = PieceStack()
        self.assertTrue(stack.is_empty())

    def test_tak_stack_height(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT))
        self.assertEqual(stack.height(), 2)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE))
        self.assertEqual(stack.height(), 3)

        stack = PieceStack()
        self.assertEqual(stack.height(), 0)

    def test_tak_stack_valid_placement(self):
        stack = PieceStack()
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.BLACK_FLAT,))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.WHITE_STANDING,))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.BLACK_STANDING,))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertTrue(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertTrue(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.WHITE_CAPSTONE,))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

        stack = PieceStack(stack=(TakPiece.BLACK_CAPSTONE,))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_FLAT))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_STANDING))
        self.assertFalse(stack.valid_placement(TakPiece.WHITE_CAPSTONE))
        self.assertFalse(stack.valid_placement(TakPiece.BLACK_CAPSTONE))

    def test_tak_stack_flatten(self):
        stack = PieceStack()
        stack.flatten()
        self.assertTrue(stack.is_empty())

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        stack_flattened = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        stack_flattened = PieceStack(stack=(TakPiece.WHITE_STANDING,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

        stack = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE,))
        stack_flattened = PieceStack(stack=(TakPiece.BLACK_FLAT, TakPiece.WHITE_CAPSTONE,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT,))
        stack_flattened = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_FLAT,))
        stack_flattened = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_STANDING,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE,))
        stack_flattened = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE,))
        stack_flattened.flatten()
        self.assertEqual(stack, stack_flattened)

    def test_tak_stack_top_view_str(self):
        stack = PieceStack()
        self.assertEqual(stack.top_view_str(), "_")

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertEqual(stack.top_view_str(), "F")

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertEqual(stack.top_view_str(), "c")

    def test_tak_stack_get_at(self):
        stack = PieceStack(stack=(TakPiece.WHITE_FLAT,))
        self.assertEqual(stack.get_at(0), TakPiece.WHITE_FLAT)

        stack = PieceStack(stack=(TakPiece.WHITE_FLAT, TakPiece.BLACK_CAPSTONE))
        self.assertEqual(stack.get_at(0), TakPiece.WHITE_FLAT)
        self.assertEqual(stack.get_at(1), TakPiece.BLACK_CAPSTONE)


class TestTakEnvTakStateMethods(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
