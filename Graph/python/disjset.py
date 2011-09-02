#!/usr/bin/env python
"""
Disjoint-set forest. Each disjoint set is implemented by a tree
data structure where each node hold pointer to its parent.

Employees union by rank strategy when merging two sets.
Employees path compression when finding roots.
"""

class DisjSet(object):
    """Disjoint set class.

    methods:
    --------
    makeSet( x )  -- 
    union( root1, root2 )
    find( x )

    >>> dset = DisjSet()
    >>> dset.makeSet('a')
    >>> dset.makeSet('b')
    >>> dset.makeSet('e')
    >>> dset.makeSet('f')
    >>> dset.makeSet('i')
    >>> dset
    {'a': set(['a']), 'i': set(['i']), 'b': set(['b']), 'e': set(['e']), 'f': set(['f'])}
    >>> dset.num_sets
    5
    >>> dset.find('a')
    'a'
    >>> dset.merge( dset.find('a'), dset.find('e') )
    >>> dset
    {'i': set(['i']), 'b': set(['b']), 'e': set(['a', 'e']), 'f': set(['f'])}
    >>> dset.num_sets
    4
    >>> dset.merge( dset.find('a'), dset.find('i'))
    >>> dset
    {'b': set(['b']), 'e': set(['a', 'i', 'e']), 'f': set(['f'])}
    >>> dset.num_sets
    3
    """

    def __init__(self):
        super(DisjSet, self).__init__()
        self.rank = {}    # maps element to its rank
        self.parent = {}  # maps element to its parent
        self.num_sets = 0 # total number of sets

    def __repr__(self):
        sets = {}
        for x in self.parent:
            root = self.find(x)
            root_set = sets.setdefault(root, set())
            root_set.add(x)
        return repr(sets)
    
    def makeSet(self, x):
        "Add x to disj set as a tree."
        self.parent[x] = x
        self.rank[x] = 0
        self.num_sets += 1

    def find(self, x):
        "Returns root of tree"
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

    def merge(self, root1, root2):
        "Merge two trees"
        if root1 == root2:
            return   # already merged
        if self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        elif self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        else:
            self.parent[root1] = root2
            self.rank[root2] += 1
        self.num_sets -= 1

    def num_sets(self):
        "Returns number of sets"
        return self.num_sets
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
