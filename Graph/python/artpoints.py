#!/usr/bin/env python
"""
Find all articulation points of a connected undirected graph.
An articulation point of a graph is a vertex whose removal causes
graph to be disconnected.

The algorithm is based on DFS. For each V in G, we calcualte
1. num(V) = depth of the node in DF spanning tree, and
2. low(V) = lowest depth of neighbors of all descendants of V.

If V is root of DFST, then V is an articulation point iff V has
more than one child. Else, V is an articulation point iff V has
some child W s.t. low(W) >= num(V).
"""
from shortpath import Graph, Vertex

FIG9_62 = { 'A' : {'B':1, 'D':1},
            'B' : {'A':1, 'C':1},
            'C' : {'B':1, 'D':1, 'G':1},
            'D' : {'A':1, 'C':1, 'E':1, 'F':1},
            'E' : {'D':1, 'F':1},
            'F' : {'D':1, 'E':1},
            'G' : {'C':1} }


def dfs(G, V, depth=1):
    """Perform DFS on graph G at vertex V and determine
    if V and its adjacent vertices are articulation points
    by calculating and comparing V.num and V.low.
    Returns a list of articulation points of graph G.

    G : Graph instance
    V : Vertex instance
    depth : depth of DFST.
    """
    # update vertex attributes
    V.visited = True
    V.num = depth
    V.low = V.num        # for now
    V.child_count = 0    # useful for depth == 1 only
    
    # find num(adj) and low(adj) for all adj
    # also find all articulation points among descendents of V
    art_list = []
    for adj in V.adj:
        # get actual Vertex obj
        adjV = G.vertices[adj]
        # if adj not visited, then it is a child
        if not adjV.visited:
            V.child_count += 1
            art_list.extend( dfs(G, adjV, depth+1) )
        # update V.low
        if adjV.num < V.num:         # e(V, adj) is back edge
            V.low = min(V.low, adjV.num)
        else:                        # adj is child
            V.low = min(V.low, adjV.low)
    # determine if V is articulation point
    if depth == 1 and V.child_count > 1:
        art_list.append(V.name)
    elif depth > 1:
        for adj in V.adj:
            adjV = G.vertices[adj]
            if adjV.low >= V.num:
                art_list.append(V.name)
                break
    return art_list
    
def art_points(G, S=None):
    """Find all articulation points for G.
    If S is given, it is to be the root of DF spanning tree.
    Else, S is taken to be the first vertex of G.

    G : Graph instance
    S : start vertex name
    
    >>> art_points(Graph(FIG9_62), 'A')
    ['D', 'C']
    >>> art_points(Graph(FIG9_62), 'C')
    ['D', 'C']
    """
    if S is None:
        S = G.vertices.keys()[0]
    for V in G.vertices:
        G.vertices[V].visited = False
    V = G.vertices[S]
    return dfs(G, V)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
