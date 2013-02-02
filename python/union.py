#/usr/bin/env python
"""
Implements a simple UnionFind data structure.
"""

class UnionFind(object):
    """Implements a simple UnionFind data structure.

    >>> uf = UnionFind(10)
    >>> uf
    {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9]}
    >>> uf.numSets
    10
    >>> uf.union(3, 2)
    >>> uf
    {0: [0], 1: [1], 2: [2, 3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9]}
    >>> uf.numSets
    9
    >>> uf.union(1, 3)
    >>> uf
    {0: [0], 2: [1, 2, 3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9]}
    >>> uf.numSets
    8
    >>> uf.union(5, 6)
    >>> uf.union(2, 6)
    >>> uf
    {0: [0], 2: [1, 2, 3, 5, 6], 4: [4], 7: [7], 8: [8], 9: [9]}
    >>> uf.numSets
    6
    """
    def __init__(self, numItems):
        self.items = range(numItems)
        self.sizes = [[1] for _ in self.items]
        self.numSets = numItems

    def union(self, i, j):
        "Join item i and j into a single set"
        set_i = self.find(i)
        set_j = self.find(j)
        if set_i != set_j:
            self.numSets -= 1
            if self.sizes[set_i] > self.sizes[set_j]:
                self.items[set_j] = set_i
                self.sizes[set_i] += self.sizes[set_j]
            else:
                self.items[set_i] = set_j
                self.sizes[set_j] += self.sizes[set_i]

    def find(self, i):
        "Returns the set id of an item"
        while self.items[i] != i:
            i = self.items[i]
        return self.items[i]

    def asDict(self):
        "Returns content as dictionary"
        sets = {}
        for idx, item in enumerate(self.items):
            aSet = sets.setdefault(self.find(item), [])
            aSet.append(idx)
        return sets
        
    def __repr__(self):
        "For debugging"
        return repr(self.asDict())

if __name__ == '__main__':
    import doctest
    doctest.testmod()
