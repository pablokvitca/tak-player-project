import unittest

from tak_env.TakAction import TakActionMoveDir


class TestTakEnvTakActionMoveDirMethods(unittest.TestCase):

    def test_tak_action_move_dir_render(self):
        self.assertEqual(TakActionMoveDir.UP.render(), "↑")
        self.assertEqual(TakActionMoveDir.RIGHT.render(), "→")
        self.assertEqual(TakActionMoveDir.DOWN.render(), "↓")
        self.assertEqual(TakActionMoveDir.LEFT.render(), "←")

        self.assertEqual(TakActionMoveDir.UP.render(arrows="URDL"), "U")
        self.assertEqual(TakActionMoveDir.RIGHT.render(arrows="URDL"), "R")
        self.assertEqual(TakActionMoveDir.DOWN.render(arrows="URDL"), "D")
        self.assertEqual(TakActionMoveDir.LEFT.render(arrows="URDL"), "L")

    def test_tak_action_move_dir_get_delta(self):
        self.assertEqual(TakActionMoveDir.UP.get_delta(), (0, 1))
        self.assertEqual(TakActionMoveDir.RIGHT.get_delta(), (1, 0))
        self.assertEqual(TakActionMoveDir.DOWN.get_delta(), (0, -1))
        self.assertEqual(TakActionMoveDir.LEFT.get_delta(), (-1, 0))

        self.assertEqual(TakActionMoveDir.UP.get_delta(distance=3), (0, 3))
        self.assertEqual(TakActionMoveDir.RIGHT.get_delta(distance=3), (3, 0))
        self.assertEqual(TakActionMoveDir.DOWN.get_delta(distance=3), (0, -3))
        self.assertEqual(TakActionMoveDir.LEFT.get_delta(distance=3), (-3, 0))

        self.assertEqual(TakActionMoveDir.UP.get_delta(distance=7), (0, 7))
        self.assertEqual(TakActionMoveDir.RIGHT.get_delta(distance=7), (7, 0))
        self.assertEqual(TakActionMoveDir.DOWN.get_delta(distance=7), (0, -7))
        self.assertEqual(TakActionMoveDir.LEFT.get_delta(distance=7), (-7, 0))


if __name__ == '__main__':
    unittest.main()
