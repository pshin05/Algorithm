#!/usr/bin/env python
"""
Implements single path shortest path algorithms.
"""
from __future__ import division
import heapq, copy
from graph import Graph

def Dijkstra(G, start):
    """Dijkstra's SSSP Algorithm
    
    Finds single source shortest path using Dijkstra's greedy
    algorithm. G is assumed to be a directed graph where 'start' param represents
    the source vertex index. Returns two arrays: first a list of size n of
    shortest distances from source vertex to each vertices in G, and
    second a list of size n of pointers to previous vertices in computed
    shortest paths to each vertices.

    Note that Dijkstra's algorithm works only if there are no
    negative edge weights. 
    
    >>> G = Graph.loadFromFile('g0nn.txt', True)
    >>> G.numVerts, G.numEdges
    (5, 6)
    >>> Dijkstra(G, 0)
    ([0, 3, 1, 3, 6], [-1, 2, 0, 2, 1])
    """
    # Current single source shortest path distances
    A = [float('inf') for _ in xrange(G.numVerts)]
    # Current Pointer to previous vertex in shortest path (-1 means none)
    P = [-1 for _ in xrange(G.numVerts)]

    # Note that in order to maintain invariance of A and P, whenever one
    # is updated the other should be updated as well.
    
    # Holds all vertices that have been processed
    T = set()
    # Priority queue to hold all the edges connected to vertices in T.
    pq = []
    # We start by adding source vertex to T
    # and adding all edges connected to it to pq.
    T.add(start)
    A[start] = 0
    for eIdx in G.getVertTail(start):
        heapq.heappush(pq, (G.getEdgeCost(eIdx), eIdx))
        vHead = G.getEdge(eIdx)[1]
        A[vHead] = G.getEdgeCost(eIdx)
        P[vHead] = start
        #print T, A, P, pq
    while pq and len(T) < G.numVerts:
        # Get next shortest edge with at least one vertex in T
        cost, eIdx = heapq.heappop(pq) 
        # Check if head vertex of the edge is already in T
        vCur = G.getEdge(eIdx)[1]
        if vCur in T:
            continue
        # Add vCur to T
        T.add(vCur)
        #print vCur, G.getVertTail(vCur)
        for eIdx1 in G.getVertTail(vCur):
            pathlen = A[vCur] + G.getEdgeCost(eIdx1)
            vHead = G.getEdge(eIdx1)[1]
            if pathlen < A[vHead]:
                A[vHead] = pathlen
                P[vHead] = vCur
                heapq.heappush(pq, (pathlen, eIdx1))
        #print T, A, P, pq
    return A, P


def BellmanFord(G, start):
    """Bellman-Ford's SSSP Algorithm
    
    Finds single source shortest path using Bellman-Ford's dynamic programming
    algorithm. G is assumed to be a directed graph where 'start' param represents
    the source vertex index. Returns two arrays: first a list of size n of
    shortest distances from source vertex to each vertices in G, and
    second a list of size n of pointers to previous vertices in computed
    shortest paths to each vertices.

    Returns None if the algorithm detects any negative cycles
    in the graph structure.

    >>> G = Graph.loadFromFile('g0.txt', True)
    >>> G.numVerts, G.numEdges
    (4, 5)
    >>> BellmanFord(G, 0)
    ([0, -1, -2, 0], [-1, 3, 0, 2])
    >>> G = Graph(2, 2)
    >>> # Add negative cycles
    >>> G.addEdge(0, 1, 1)
    >>> G.addEdge(1, 0, -2)
    >>> A, P = BellmanFord(G, 0)
    >>> A is None and P is None
    True
    """
    # We only need 2 1-D arrays to hold shortest path values.
    A0 = [float('inf') for _ in xrange(G.numVerts)]
    A1 = copy.deepcopy(A0)
    # We need 1 1-D array to hold previous vertex pointers
    P = [-1 for _ in xrange(G.numVerts)]
    # Initialize A
    A0[start] = 0
    # Main loop
    # We run this n + 1 times so that we can detect presence
    # of negative edge cycles.
    for k in xrange(G.numVerts+1):
        if k % 2 == 0:
            Acur = A1; Aprev = A0
        else:
            Acur = A0; Aprev = A1
        for vCur in xrange(G.numVerts):
            Acur[vCur] = Aprev[vCur]
            for eIdx in G.getVertHead(vCur):
                vTail = G.getEdge(eIdx)[0]
                pathcost = Aprev[vTail] + G.getEdgeCost(eIdx)
                if pathcost < Acur[vCur]:
                    Acur[vCur] = pathcost
                    P[vCur] = vTail
    # Check for negative cycles
    for i in xrange(G.numVerts):
        if Acur[i] != Aprev[i]:
            return None, None
    return Acur, P

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
