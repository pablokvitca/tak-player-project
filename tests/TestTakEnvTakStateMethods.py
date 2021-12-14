import unittest

import numpy as np

from tak_env.TakBoard import TakBoard
from tak_env.TakPlayer import TakPlayer
from tak_env.TakState import TakState


class TestTakEnvTakStateMethods(unittest.TestCase):

    def test_tak_state_first_action(self):
        pass  # TODO: test

    def test_tak_state_current_player_has_pieces_available(self):
        pass  # TODO: test

    def test_tak_state_current_player_has_capstone_available(self):
        pass  # TODO: test

    def test_tak_state_max_pick_up_number(self):
        pass  # TODO: test

    def test_tak_state_remove_piece_for_player(self):
        pass  # TODO: test

    def test_tak_state_remove_capstone_for_player(self):
        pass  # TODO: test

    def test_tak_state_has_path_for_player(self):
        pass  # TODO: test

    def test_tak_state_pieces_left_player(self):
        pass  # TODO: test

    def test_tak_state_pieces_left(self):
        pass  # TODO: test

    def test_tak_state_spaces_left(self):
        pass  # TODO: test

    def test_tak_state_controlled_flat_spaces(self):
        pass  # TODO: test

    def test_tak_state_controlled_road_spaces(self):
        pass  # TODO: test

    def test_tak_state_has_path_for_player_from_file_test_1(self):
        board_data = np.fromfile("../test_files/savedboard_1.txt", dtype=int)
        board = TakBoard.from_3d_matrix(board_data, 5)
        self.assertEqual(board.board_size, 5)
        self.assertEqual(board.total_pieces(), 23)
        state = TakState(5, board, 16, 13, False, False, TakPlayer.WHITE)

        self.assertFalse(state.board.has_path_for_player(TakPlayer.WHITE))
        self.assertFalse(state.board.has_path_for_player(TakPlayer.BLACK))


if __name__ == '__main__':
    unittest.main()
