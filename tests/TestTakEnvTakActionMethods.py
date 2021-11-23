import unittest

from tak_env.TakAction import TakAction


class TestTakEnvTakActionMethods(unittest.TestCase):

    def test_tak_action_init(self):
        self.assertEqual(TakAction((0, 0)).position, (0, 0))
        self.assertEqual(TakAction((1, 6)).position, (1, 6))


if __name__ == '__main__':
    unittest.main()
