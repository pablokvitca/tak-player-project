import unittest

from utils.utils import partitions, ordered_partitions


class TestUtils(unittest.TestCase):

    def test_partitions(self):
        self.assertEqual({(1,)}, set(partitions(1)))

        self.assertEqual({(2,), (1, 1)}, set(partitions(2)))

        self.assertEqual({(3,), (1, 2), (1, 1, 1)}, set(partitions(3)))

        self.assertEqual({(4,), (1, 3), (2, 2), (1, 1, 2), (1, 1, 1, 1)}, set(partitions(4)))

        self.assertEqual(
            {(5,), (1, 4), (2, 3), (1, 1, 3), (1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1)},
            set(partitions(5))
        )

        # See https://oeis.org/A000041
        self.assertEqual(11, len(set(partitions(6))))
        self.assertEqual(15, len(set(partitions(7))))
        self.assertEqual(22, len(set(partitions(8))))
        self.assertEqual(30, len(set(partitions(9))))
        self.assertEqual(42, len(set(partitions(10))))

    def test_ordered_partitions(self):
        self.assertEqual({(1,)}, set(ordered_partitions(1)))

        self.assertEqual({(2,), (1, 1)}, set(ordered_partitions(2)))

        self.assertEqual({(3,), (2, 1), (1, 2), (1, 1, 1)}, set(ordered_partitions(3)))

        self.assertEqual(
            {(4,), (3, 1), (1, 3), (2, 2), (2, 1, 1), (1, 2, 1), (1, 1, 2), (1, 1, 1, 1)},
            set(ordered_partitions(4))
        )

        self.assertEqual(
            {
                (5,),
                (4, 1), (1, 4),
                (3, 2), (2, 3),
                (3, 1, 1), (1, 3, 1), (1, 1, 3),
                (2, 2, 1), (2, 1, 2), (1, 2, 2),
                (2, 1, 1, 1), (1, 2, 1, 1), (1, 1, 2, 1), (1, 1, 1, 2),
                (1, 1, 1, 1, 1)
            },
            set(ordered_partitions(5))
        )

        # Fun fact, apparently the count of ordered partitions of 2^(n-1)


if __name__ == '__main__':
    unittest.main()
