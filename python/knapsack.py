#!/usr/bin/env python
"""
Functions to solve Knapsack problems.
"""

import numpy as np

def BottomUp(capacity, items):
    """Build A[i,j] bottom up.

    capacity : capacity of the knapsack
    items : list of tuples (value, weight) for each item

    Returns (max_val, max_items) where max_val is the maximum
    value of the items in the knapsack and max_items are the list
    of items selected to go into the knapsack.

    >>> BottomUp(8, [(15,1),(10,5),(9,3),(5,4)])
    29
    """
    n = len(items)
    A = np.zeros(shape=(n+1, capacity+1), dtype=int)
    for j in xrange(1, capacity+1):
        for i in xrange(1, n+1):
            vi, wi = items[i-1]
            if j >= wi:
                A[i,j] = max(A[i-1,j], A[i-1,j-wi] + vi)
            else:
                A[i,j] = A[i-1,j]
    return A[n, capacity]

def TopDown(capacity, items, memoized={}):
    """Evaluate A[i,j] recursively.

    capacity : capacity of the knapsack
    items : list of tuples (value, weight) for each item

    Returns (max_val, max_items) where max_val is the maximum
    value of the items in the knapsack and max_items are the list
    of items selected to go into the knapsack.

    >>> TopDown(8, [(15,1),(10,5),(9,3),(5,4)])
    29
    """

    def SubProb(i, j):
        # Base case
        if i == 0 or j == 0:
            return 0
        # Check if result memoized
        if (i,j) not in memoized:
            # Recursively solve sub problems
            vi, wi = items[i-1]
            if j >= wi:
                memoized[(i,j)] = max(SubProb(i-1,j),
                                      SubProb(i-1,j-wi) + vi)
            else:
                memoized[(i,j)] = SubProb(i-1, j)
        return memoized[(i,j)]

    n = len(items)
    memoized = {}
    return SubProb(n, capacity)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
