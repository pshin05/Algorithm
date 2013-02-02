#!/usr/bin/env python
"""
Implements algorithms for finding minimum cost spanning trees.

Input : undirected graph G = (V, E) where Ce is cost
        of each edge e in E.

1/11/2013   created   Yong Shin
"""

from __future__ import division
import heapq
from graph import Graph

def prim(G):
    """
    Implements Prim's minimum spanning tree algorithm.
    G is assumed to be undirected.
    Returns a list of edge index forming the MST.

    Implementation detail: Best performance would be achieved
    by using a vertex heap, but such an implementation
    requires that the heap support delete functionality.
    This particular implementation uses an edge heap instead.

    >>> G = Graph(6, 9)
    >>> G.addEdge(0, 1, 1)
    >>> G.addEdge(1, 2, 6)
    >>> G.addEdge(0, 3, 3)
    >>> G.addEdge(3, 1, 5)
    >>> G.addEdge(1, 4, 1)
    >>> G.addEdge(4, 2, 4)
    >>> G.addEdge(2, 5, 2)
    >>> G.addEdge(3, 4, 1)
    >>> G.addEdge(4, 5, 4)
    >>> G
    <Graph m=9, n=6, edges=[((0, 1), 1), ((1, 2), 6), ((0, 3), 3), ((3, 1), 5), ((1, 4), 1), ((4, 2), 4), ((2, 5), 2), ((3, 4), 1), ((4, 5), 4)] verts=[[0, 2], [0, 1, 3, 4], [1, 5, 6], [2, 3, 7], [4, 5, 7, 8], [6, 8]]>
    >>> prim(G)
    [0, 4, 7, 5, 6]
    """
    # Holds all edges forming the MST
    MST = []
    # Holds all vertices that have been pulled into MST so far
    T = set()
    # Priority queue to hold all the edges connected to a
    # vertex in T.
    pq = []
    # We start by arbitrarily selecting vertex 1 as the root
    # and adding all edges connected to it to pq.
    T.add(1)
    for eIdx in G.getVert(1):
        heapq.heappush(pq, (G.getEdgeCost(eIdx), eIdx))
    while pq:
        # Get next shortest edge with at least one vertex
        # in T
        cost, eIdx = heapq.heappop(pq) 
        # Check if edge has vertex (if any) not yet in T
        v1, v2 = G.getEdge(eIdx)
        if v1 not in T:
            v = v1
        elif v2 not in T:
            v = v2
        else:
            # Skip if both vertices already in T
            continue
        # Add v to T, eIdx to MSt, v's edges to pq
        T.add(v)
        MST.append(eIdx)
        for edge in G.getVert(v):
            heapq.heappush(pq, (G.getEdgeCost(edge), edge))
    return MST
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()


