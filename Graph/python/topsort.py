#!/usr/bin/env python
"""Topological sort.
"""

# Figure 9.3
DAG = {'v1': ('v2','v3','v4'),
       'v2': ('v4','v5'),
       'v3': ('v6',),
       'v4': ('v3','v6','v7'),
       'v5': ('v4','v7'),
       'v6': (),
       'v7': ('v6',)}

def topological_sort(graph):
    """Return a topological sorted list of vertices.

    graph : dictionary of each vertices and their adjacentcy lists.

    >>> topological_sort(DAG)
    U set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7'])
    A set(['v2', 'v3', 'v4', 'v5', 'v6', 'v7'])
    U set(['v2', 'v3', 'v4', 'v5', 'v6', 'v7'])
    A set(['v3', 'v4', 'v5', 'v6', 'v7'])
    U set(['v3', 'v4', 'v5', 'v6', 'v7'])
    A set(['v3', 'v4', 'v6', 'v7'])
    U set(['v3', 'v4', 'v6', 'v7'])
    A set(['v3', 'v6', 'v7'])
    U set(['v3', 'v6', 'v7'])
    A set(['v6'])
    U set(['v6'])
    A set([])
    ['v1', 'v2', 'v5', 'v4', 'v3', 'v7', 'v6']
    """
    #import pdb; pdb.set_trace()
    result = []
    U = set(graph.keys())
    while len(U):
        print 'U',U
        # collect all adjacent vertices for v in U
        A = set([])
        for v in U:
            A.update( set(graph[v]) )
        # if v in U but not in A, add v to result
        print 'A',A
        H = U - A
        for v in H:
            result.append(v)
        # repeat with remaining vertices
        U = A
    return result
    
def topological_sort2(graph):
    """Return a topological sorted list of vertices.
    This version calculates InDegree for each node, and keeps
    zero InDegree nodes in separate queue.

    graph : dictionary of each vertices and their adjacentcy lists.

    >>> topological_sort2(DAG)
    ['v1', 'v2', 'v5', 'v4', 'v7', 'v3', 'v6']
    """
    #import pdb; pdb.set_trace()
    res = []           # sorted list
    in_degs = {}       # in_degrees for each node
    zero_in_degs = []  # nodes with zero in_degrees
    # Collect in_degs data for all nodes
    for node in graph.keys():
        for adj in graph[node]:
            in_degs[adj] = in_degs.setdefault(adj,0) + 1
    # Populate zero_in_degs
    for node in graph:
        if node not in in_degs:
            zero_in_degs.append(node)
    # All nodes must pass through zero_in_degs.
    while len(zero_in_degs):
        # Remove a node with zero in deg
        node = zero_in_degs.pop()
        # Remove in_degs of all its adj nodes
        for adj in graph[node]:
            in_degs[adj] -= 1
            if in_degs[adj] == 0:
                zero_in_degs.append(adj)
        # Add removed node to sorted list
        res.append(node)
    return res

if __name__ == '__main__':
    import doctest
    doctest.testmod()

