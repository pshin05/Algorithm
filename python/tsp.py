#!/bin/env python
"""
Algorithms to solve TSP.

Traveling salesman problem takes a complete undirected graph
with non-negative edges as inputs and returns a minimum-cost
tour.
"""
import numpy as np
import itertools as it

def BruteForce(G):
    """Examines all n! permutations of the vertices to find the
    minimum-cost tour.

    G : n x n matrix containing distances between any two vertices.
    
    Returns (Cost, Path), where Cost is the cost of the minimal
    tour and Path is the list of vertices visited.
    
    >>> G = np.zeros(shape=(4, 4))
    >>> G[0,1] = 20; G[1,0] = 20
    >>> G[0,2] = 42; G[2,0] = 42
    >>> G[0,3] = 35; G[3,0] = 35
    >>> G[1,2] = 30; G[2,1] = 30
    >>> G[1,3] = 34; G[3,1] = 34
    >>> G[2,3] = 12; G[3,2] = 12
    >>> BruteForce(G)
    (97.0, (0, 1, 2, 3, 0))
    """
    numVerts = G.shape[0]
    Cost = float('inf')
    Path = []
    for perm in it.permutations(range(1, numVerts)):
        curCost = G[0, perm[0]] + G[perm[-1], 0]
        for i in range(len(perm)-1):
            curCost += G[perm[i], perm[i+1]]
        #print curCost, perm
        if curCost < Cost:
            Cost = curCost
            Path = (0,) + perm + (0,)
    return Cost, Path

def DynProg(G):
    """Recursively computes (with memoization) optimal solutions
    in terms of optimal solutions of smaller problems where the
    number of vertices participating in the tour is one smaller.

    Returns (Cost, Path), where Cost is the cost of the minimal
    tour and Path is the list of vertices visited.
    
    >>> G = np.zeros(shape=(4, 4))
    >>> G[0,1] = 20; G[1,0] = 20
    >>> G[0,2] = 42; G[2,0] = 42
    >>> G[0,3] = 35; G[3,0] = 35
    >>> G[1,2] = 30; G[2,1] = 30
    >>> G[1,3] = 34; G[3,1] = 34
    >>> G[2,3] = 12; G[3,2] = 12
    >>> DynProg(G)
    m: 2
    m: 3
    m: 4
    97.0
    """
    numVerts = G.shape[0]
    V = range(numVerts)
    # A 2-D array indexed by S (a subset of vertices) that
    # contain vertex 0 and destinations j.
    A = {}
    # Iterate by number of verts in a subset
    for m in xrange(2, numVerts+1):
        print "m:", m
        # Do not include vertex 0 in S for now
        for S in it.combinations(V[1:], m-1):
            A[(0,)+S] = np.zeros(numVerts)
            for jIdx, j in enumerate(S):
                # Base case (k == 0)
                if len(S) == 1:
                    curMin = G[0, j]
                else:
                    curMin = float('inf')
                # k != 0
                Sj = S[:jIdx] + S[jIdx+1:]  # S - {j}
                for k in Sj:
                    val = prevA[(0,)+Sj][k] + G[k, j]
                    curMin = min(curMin, val)
                A[(0,)+S][j] = curMin
        #print A
        prevA = A
        A = {}
    # Complete the tour and find min
    Av = prevA[tuple(V)]
    return min([Av[j] + G[j,0] for j in range(len(Av)) if j != 0])
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
