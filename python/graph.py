#!/usr/bin/env python
"""
Graph classes.

Contains graph data structure implementations.

1/11/2013   created   Yong Shin
"""

from __future__ import division
import heapq, copy

class Graph(object):
    """Adjacency list implemetation of graph data structure.

    Graph instance is created by specifying number of vertices
    and edges. The details of the graph structure are constructed
    by adding edges. Directed and undirected graphs are both
    constructed the same way; only the interpretation of edge
    tuple (v1, v2) is different. In a directed graph v1 is the tail
    and v2 is the head; in an undirected graph there is no such
    distinction.

    Contents of the graph structure, including edges and vertices, can be
    accessed via getter methods using vertex and edge index.

    Note that all indices are zero based. When importing data from a file
    where vertex index are 1-based, set 1_based parameter to True.

    >>> G = Graph(4, 2)
    >>> G.addEdge(0, 1, 10)
    >>> G.addEdge(1, 2, 40)
    >>> G
    <Graph m=2, n=4, edges=[((0, 1), 10), ((1, 2), 40)] verts=[[0], [0, 1], [1], []]>
    >>> G.getEdge(1)
    (1, 2)
    >>> G.getEdgeCost(1)
    40
    >>> G.getVert(1)
    [0, 1]
    >>> G.getVertHead(1)
    [0]
    >>> list(G.getVertHeadIter(1))
    [0]
    >>> G.getVertTail(1)
    [1]
    >>> list(G.getVertTailIter(1))
    [1]
    >>> G = Graph.loadFromFile('g0nn.txt', True)
    >>> G
    <Graph m=6, n=5, edges=[((0, 1), 4), ((1, 4), 3), ((0, 2), 1), ((2, 1), 2), ((2, 3), 2), ((3, 4), 3)] verts=[[0, 2], [0, 1, 3], [2, 3, 4], [4, 5], [1, 5]]>
    >>> G.clone()
    <Graph m=6, n=5, edges=[((0, 1), 4), ((1, 4), 3), ((0, 2), 1), ((2, 1), 2), ((2, 3), 2), ((3, 4), 3)] verts=[[0, 2], [0, 1, 3], [2, 3, 4], [4, 5], [1, 5]]>
    >>> [G.getVertTail(v) for v in range(G.numVerts)]
    [[0, 2], [1], [3, 4], [5], []]
    >>> [G.getVertHead(v) for v in range(G.numVerts)]
    [[], [0, 3], [2], [4], [1, 5]]
    """
    def __init__(self, numVerts, numEdges):
        self.numVerts = numVerts
        self.numEdges = numEdges
        self.edges = []                            # (v1, v2)
        self.edgeCosts = []
        self.verts = [[] for _ in range(numVerts)] # list of adj edges

    def addEdge(self, v1, v2, cost=1):
        """Adds an edge and its cost
        v1 : vertex index (1-based)
        Duplicate edges are not checked"""
        edgeIdx = len(self.edges)
        self.edges.append((v1, v2))
        self.edgeCosts.append(cost)
        self.verts[v1].append(edgeIdx)
        self.verts[v2].append(edgeIdx)

    def getEdge(self, idx):
        "Returns (v1, v2) corresponding to edge index"
        return self.edges[idx]

    def getEdgeCost(self, idx):
        "Returns edge cost corresponding to edge index"
        return self.edgeCosts[idx]

    def setEdgeCost(self, idx, cost):
        "Set new edge cost"
        self.edgeCosts[idx] = cost
        
    def getVert(self, idx):
        """Returns list of adjacent edges for given vertex index

        Note that for directed graphs, this returns both the
        in-edges and out-edges attached to the vertex.
        """
        return self.verts[idx]

    def getVertHead(self, idx):
        """Returns list of adjacent edges for which given vertex is head.

        This is a convenience method for directed graphs.
        """
        return [eIdx for eIdx in self.verts[idx]
                if self.edges[eIdx][1] == idx]

    def getVertHeadIter(self, idx):
        "Same as getVertHead but returns a generator"
        for eIdx in self.verts[idx]:
            if self.edges[eIdx][1] == idx:
                yield eIdx
                
    def getVertTail(self, idx):
        """Returns list of adjacent edges for which given vertex is tail.

        This is a convenience method for directed graphs.
        """
        return [eIdx for eIdx in self.verts[idx]
                if self.edges[eIdx][0] == idx]

    def getVertTailIter(self, idx):
        "Same as getVertTail but returns a generator"
        for eIdx in self.verts[idx]:
            if self.edges[eIdx][0] == idx:
                yield eIdx
                
    def clone(self):
        "Returns a deep copy of self"
        cloned = Graph(self.numVerts, self.numEdges)
        cloned.edges = copy.deepcopy(self.edges)
        cloned.edgeCosts = copy.deepcopy(self.edgeCosts)
        cloned.verts = copy.deepcopy(self.verts)
        return cloned
    
    def __repr__(self):
        return "<Graph m=%d, n=%d, edges=%s verts=%s>" % (
            self.numEdges, self.numVerts, zip(self.edges, self.edgeCosts), self.verts)

    @staticmethod
    def loadFromFile(datafile, one_based = False):
        """Read data from file return Graph object
        The first row of the data file is assumed to contain number of vertices
        and edges. All subsequent rows must have 'V1 V2 Cost' format where
        V1 and V2 are vertex index and Cost is the edge cost. Vertex index are
        assumed to be zero based but can be overridden by specifying one_based
        parameter.
        """
        data = []
        f = open(datafile)
        numVerts, numEdges = [int(x) for x in f.readline().strip().split()]
        G = Graph(numVerts, numEdges)
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            parts = [int(x) for x in line.split()]
            if len(parts) == 3:
                v1, v2, cost = parts
            elif len(parts) == 2:
                v1, v2 = parts
                cost = 1
            else:
                raise Exception, 'Invalid data'
            if one_based:
                G.addEdge(v1-1, v2-1, cost)
            else:
                G.addEdge(v1, v2, cost)
        assert(G.numEdges == len(G.edges))
        f.close()
        return G

if __name__ == "__main__":
    import doctest
    doctest.testmod()


