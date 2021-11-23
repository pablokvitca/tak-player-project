import unittest

from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer


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


if __name__ == '__main__':
    unittest.main()
