#!/usr/bin/env python
"""
Find an Euler circuit of a graph.

Implementation is flawed: the algorithm may not visit all edges.
"""
from graph import Vertex, Graph

FIG9_70 = { 'v1': {'v3': 1, 'v4': 1},
            'v2': {'v3': 1, 'v8': 1},
            'v3': {'v1': 1, 'v2': 1, 'v4': 1, 'v6': 1, 'v7': 1, 'v9': 1},
            'v4': {'v1': 1, 'v3': 1, 'v5': 1, 'v7': 1, 'v10': 1, 'v11': 1},
            'v5': {'v4': 1, 'v10': 1},
            'v6': {'v3': 1, 'v9': 1},
            'v7': {'v3': 1, 'v4': 1, 'v9': 1, 'v10': 1},
            'v8': {'v2': 1, 'v9': 1},
            'v9': {'v3': 1, 'v6': 1, 'v7': 1, 'v8': 1, 'v10': 1, 'v12': 1},
            'v10': {'v4': 1, 'v5': 1, 'v7': 1, 'v9': 1, 'v11': 1, 'v12': 1},
            'v11': {'v4': 1, 'v10': 1},
            'v12': {'v9': 1, 'v10': 1} }

def euler_tour(G, Vs, Ve):
    """
    Returns an Euler tour (i.e. beginning and ending vertices are
    different) of graph G.

    G : instance of Graph
    Vs : starting vertex
    Ve : ending vertex
    return: a list of vertice names representing euler tour.
    """
    if Vs == Ve:
        return euler_circuit(G, Vs)
    verts = G.vertices
    num_edges = G.num_edges()/2  # Assume undirected
    if num_edges == 1:
        return [Vs, Ve]
    else:
        adjs = verts[Vs].adj.keys()[0]
        G.remove_edge(Vs, adjs)
        # above line should precede below line because
        # adjs may equal adje
        adje = verts[Ve].adj.keys()[0]
        G.remove_edge(Ve, adje)
        return [Vs] + euler_tour(G, adjs, adje) + [Ve]
    
def euler_circuit(G, V):
    """
    Returns an Euler circuit of graph G terminating at vertex V.
    
    The strategy is to remove two edges
    attached to V to use as starting and ending edges. If these
    two edges were attached to U and W, then next we find an Euler
    tour from U and W. We only need to append the beginning and
    ending vertices to Euler tour to find Euler circuit.
    
    Note:
    1. Algorithm is intended only for undirected graphs.
    2. Algorithm is intended only for graphs that have
       Euler circuits.

    G : instance of Graph
    V : vertex name
    returns: a list of vertice names representing euler circuit.
    
    >>> G = Graph(FIG9_70)
    >>> euler_circuit(G, 'v1')
    ['v1', 'v3', 'v2', 'v8', 'v9', 'v3', 'v7', 'v4', 'v5', 'v10', 'v12', 'v9', 'v10', 'v11', 'v4', 'v10', 'v7', 'v9', 'v6', 'v3', 'v4', 'v1']
    >>> G = Graph(FIG9_70)
    >>> euler_circuit(G, 'v7')
    ['v7', 'v9', 'v8', 'v2', 'v3', 'v4', 'v5', 'v10', 'v12', 'v9', 'v10', 'v11', 'v4', 'v7', 'v3', 'v9', 'v6', 'v3', 'v1', 'v4', 'v10', 'v7']
    """
    if len(G.vertices[V].adj) == 0:
        return [V]
    else:
        verts = G.vertices
        adj0 = verts[V].adj.keys()[0]
        adj1 = verts[V].adj.keys()[1]
        G.remove_edge(V, adj0)
        G.remove_edge(V, adj1)
        tour = euler_tour(G, adj0, adj1)
        return [V] + tour + [V]
    
if __name__ == '__main__':
    print "Implementation flawed!"
    import doctest
    doctest.testmod()
    
