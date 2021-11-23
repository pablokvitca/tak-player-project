import unittest

from tak_env.TakPlayer import TakPlayer


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


if __name__ == '__main__':
    unittest.main()
