import unittest

import numpy as np

from tak_env.TakBoard import TakBoard
from tak_env.TakPiece import TakPiece


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
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], np.zeros((6, 6, 1), dtype=int))
        board = TakBoard(3)
        expected_matrix = np.zeros((3, 3, 1), dtype=int)
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], np.zeros((3, 3, 1), dtype=int))
        board.place_piece((1, 1), TakPiece.WHITE_FLAT)
        expected_matrix[1, 1, 0] = 1
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.BLACK_FLAT)
        expected_matrix[1, 0, 0] = -1
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.WHITE_STANDING)
        expected_matrix = np.zeros((3, 3, 2), dtype=int)
        expected_matrix[1, 1, 0] = 1
        expected_matrix[1, 0, 0] = -1
        expected_matrix[1, 0, 1] = 2
        self.assertNumpyArrayEqual(board.as_3d_matrix()[0], expected_matrix)
        board.place_piece((1, 0), TakPiece.BLACK_CAPSTONE)
        expected_matrix = np.zeros((3, 3, 3), dtype=int)
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


if __name__ == '__main__':
    unittest.main()
