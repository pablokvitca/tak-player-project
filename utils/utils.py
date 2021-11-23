from itertools import permutations

from more_itertools import flatten


def partitions(n, min_i=1):
    """
    Generator that yields the partitions for the number n.
    Partitions are the number of ways to positive integers can sum up to n.
    Order of the elements to sum up to n is not important.
    """
    yield n,
    for i in range(min_i, n // 2 + 1):
        for p in partitions(n - i, i):
            yield (i,) + p


def ordered_partitions(n, min_i=1):
    """
    Generator that yields the partitions for the number n.
    Partitions are teh number of ways to positive integers can sum up to n.
    Order of the elements to sum up to n IS important.
    """
    return flatten([set(permutations(partition)) for partition in partitions(n, min_i=min_i)])
