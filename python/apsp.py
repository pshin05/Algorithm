#!/usr/bin/env python
"""
Implements all pairs shortest path algorithms.
"""
from __future__ import division
import copy
from graph import Graph
from sssp import Dijkstra, BellmanFord

def FloydWarshall(G):
    """Floyd-Warshall's All pairs shortest path algorithm.
    
    Returns n x n shortest path lengthes array and a n x n largest interior
    vertex array such that (i,j)-entry contains the
    largest vertex index among all interior vertices forming
    the shortest path from vertex i to vertex j. If the shortest
    path from vertex i to vertex j is a direct link (i.e. no
    interior vertices) then (i,j)-entry contains 0.

    Returns (None, None) if the algorithm detects any negative cycles
    in the graph structure.

    >>> G = Graph.loadFromFile('g0.txt', True)
    >>> G.numVerts, G.numEdges
    (4, 5)
    >>> FloydWarshall(G)
    ([[0, -1, -2, 0], [4, 0, 2, 4], [5, 1, 0, 2], [3, -1, 1, 0]], [[-1, 3, -1, 2], [-1, -1, 0, 2], [3, 3, -1, -1], [1, -1, 1, -1]])
    >>> G = Graph(2, 2)
    >>> # Add negative cycles
    >>> G.addEdge(0, 1, 1)
    >>> G.addEdge(1, 0, -2)
    >>> A, I = FloydWarshall(G)
    >>> A is None and I is None
    True
    """
    # We only need 2 n x n arrays to hold shortest path values.
    A0 = [[float('inf') for _ in xrange(G.numVerts)]
          for _ in xrange(G.numVerts)]
    A1 = copy.deepcopy(A0)
    # We need 1 n x n array to hold largest interior vertex index.
    IntV = [[-1 for _ in xrange(G.numVerts)]
            for _ in xrange(G.numVerts)]
    # Initialize A
    for i in xrange(G.numVerts):
        A0[i][i] = 0
    for eIdx, (v1, v2) in enumerate(G.edges):
        A0[v1][v2] = G.getEdgeCost(eIdx)
    # Main loop
    for k in xrange(G.numVerts):
        if k % 2 == 0:
            Acur = A1; Aprev = A0
        else:
            Acur = A0; Aprev = A1
        for i in xrange(G.numVerts):
            for j in xrange(G.numVerts):
                Pk = Aprev[i][k] + Aprev[k][j]
                if Pk < Aprev[i][j]:
                    IntV[i][j] = k
                    Acur[i][j] = Pk
                else:
                    Acur[i][j] = Aprev[i][j]
    # Check for negative cycles
    for i in xrange(G.numVerts):
        if Acur[i][i] < 0:
            return None, None
    return Acur, IntV


def reconstructFM(G, IntV):
    """Reconstructs all path shortest paths from values returned by FloydWarshall.

    Returns ((tail_vertex, head_vertex), path_cost, path_list) for each
    pairs of vertices in the graph.
    >>> G = Graph.loadFromFile('g0.txt', True)
    >>> SP, IntV = FloydWarshall(G)
    >>> reconstructFM(G, IntV)
    (0, 0): []
    (0, 1): [0, 2, 3, 1]
    (0, 2): [0, 2]
    (0, 3): [0, 2, 3]
    (1, 0): [1, 0]
    (1, 1): []
    (1, 2): [1, 0, 2]
    (1, 3): [1, 0, 2, 3]
    (2, 0): [2, 3, 1, 0]
    (2, 1): [2, 3, 1]
    (2, 2): []
    (2, 3): [2, 3]
    (3, 0): [3, 1, 0]
    (3, 1): [3, 1]
    (3, 2): [3, 1, 0, 2]
    (3, 3): []
    """
    def SP(i, j):
        # Reconstruct shortest path from vertex i to vertex j.
        if i == j: return []
        V = IntV[i][j] 
        if V == -1:
            return [i, j]
        else:
            return SP(i, V) + SP(V, j)[1:]

    for i in xrange(len(IntV)):
        for j in xrange(len(IntV)):
            print "(%d, %d): %s" % (i, j, SP(i, j))


def Johnson(G):
    """Johnson's All pairs shortest path algorithm.

    Returns n x n shortest path lengthes array and a n x n largest interior
    vertex array such that (i,j)-entry contains the
    largest vertex index among all interior vertices forming
    the shortest path from vertex i to vertex j. If the shortest
    path from vertex i to vertex j is a direct link (i.e. no
    interior vertices) then (i,j)-entry contains 0.

    Returns (None, None) if the algorithm detects any negative cycles
    in the graph structure.

    >>> G = Graph.loadFromFile('gc.txt', True)
    >>> G.numVerts, G.numEdges
    (6, 7)
    >>> A, P = Johnson(G)
    >>> A
    [[0, -2, -3, -1, -6, inf], [3, 0, -1, 1, -4, inf], [4, 2, 0, 2, -3, inf], [inf, inf, inf, 0, inf, inf], [inf, inf, inf, inf, 0, inf], [inf, inf, inf, 1, -4, 0]]
    >>> P
    [[-1, 0, 1, 2, 2, -1], [2, -1, 1, 2, 2, -1], [2, 0, -1, 2, 2, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, 5, 5, -1]]
    >>> G = Graph(2, 2)
    >>> # Add negative cycles
    >>> G.addEdge(0, 1, 1)
    >>> G.addEdge(1, 0, -2)
    >>> A, P = Johnson(G)
    >>> A is None and P is None
    True
    """
    # Modify Graph by adding a source vertex that connects
    # to all vertices in G with edge cost of 0
    #print "Adding an extra source vertex ..."
    Vsrc = G.numVerts
    Gx = Graph(G.numVerts+1, G.numEdges+G.numVerts)
    for i in xrange(G.numEdges):
        v1, v2 = G.getEdge(i)
        cost = G.getEdgeCost(i)
        Gx.addEdge(v1, v2, cost)
    for i in xrange(G.numVerts):
        Gx.addEdge(Vsrc, i, 0)
    #print G, Gx

    # Run Bellman-Ford on the graph with s as start vertex
    #print "Running Bellman-Ford..."
    A0, P0 = BellmanFord(Gx, Vsrc)
    #print A, P
    # Check if any negative cycles
    if A0 is None and P0 is None:
        return None, None

    # Add vertex weights (A0[u] - A0[v]) to edge costs
    #print "Adding vertex weights ..."
    for i in xrange(G.numEdges):
        v1, v2 = G.getEdge(i)
        G.setEdgeCost(i, G.getEdgeCost(i) + A0[v1] - A0[v2])
    #print G

    # Run Dijkstra's algorithm for all vertices as source
    #print "Running n x Dijkstra ..."
    A = []
    P = []
    for i in xrange(G.numVerts):
        A1, P1 = Dijkstra(G, i)
        A.append(A1)
        P.append(P1)
    #print A, P

    # Adjust shortest path lengths by subtracting path source
    # vertex weight and adding path destination vertex weight.

    #print "Correcting sp weights ..."
    for i in xrange(G.numVerts):
        for j in xrange(G.numVerts):
            A[i][j] += A0[j] - A0[i]
    #print A, P
    return A, P

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
