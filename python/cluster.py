#!/usr/bin/env python
"""
Clustering Alogirithms.
"""
import heapq
from union import UnionFind

def MaxSpacing(numNodes, dists, k):
    """
    Performs max-spacing k-clustering using a greedy algorithm.

    Basic strategy is to greedily join two closest pairs of nodes
    into a single set until we have k total number of sets
    remaining. The implementation is done using unionfind data
    structure

    numNodes : number of nodes
    dists : list of tuples (d, n1, n2) for each pair of nodes
            where n1 and n2 are node index and d is the distance
            between them.
    k : number of desired clusters

    Returns (spacing, clusters) where clusters is a dict containing
    members of each clusters.

    >>> spacing, clusters = MaxSpacing(3, [(1,1,2),(3,1,3),(2,2,3)], 2)
    >>> spacing
    2
    >>> clusters
    {1: [0, 1], 2: [2]}
    """
    heapq.heapify(dists)
    uf = UnionFind(numNodes)
    while uf.numSets > k:
        dist, n1, n2 = heapq.heappop(dists)
        uf.union(n1-1, n2-1)
    while dists:
        dist, n1, n2 = heapq.heappop(dists)
        if uf.find(n1-1) != uf.find(n2-1):
            return dist, uf.asDict()
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
