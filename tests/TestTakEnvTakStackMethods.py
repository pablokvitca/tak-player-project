import unittest

from tak_env.TakPiece import TakPiece
from tak_env.TakPlayer import TakPlayer
from tak_env.TakStack import PieceStack


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


if __name__ == '__main__':
    unittest.main()
