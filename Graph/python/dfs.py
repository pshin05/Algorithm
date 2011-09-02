#!/usr/bin/env python
"""
Depth first search.
"""
from graph import Graph, Vertex

# A directed graph
FIG9_74 = { 'va': {'vb':1, 'vd':1},
            'vb': {'vc':1, 'vf':1},
            'vc': {'va':1, 'vd':1, 've':1},
            'vd': {'ve':1},
            've': {},
            'vf': {'vc':1},
            'vg': {'vf':1, 'vh':1},
            'vh': {'vf':1, 'vj':1},
            'vi': {'vh':1},
            'vj': {'vi':1} }

def dfs_memoize(G, V=None):
    """Perform a dfs where each vertices are visited at
    most once. Returns a dictionary consisting of several
    relevant lists:
    1. result['dfs list'] = list of dfs scans over the graph.
       There will be multiple scans if the graph is not strongly
       connected.
    2. result['tree edges'] = list of all tree edges
    3. result['forward edges'] = list of all forward edges
    4. result['backward edges'] = list of all backward edges.
    5. result['cross edges'] = list of all cross edges.

    G : graph instance
    V : start vertice name

    >>> G = Graph(FIG9_74)
    >>> dfs_memoize(G)
    """

    def do_dfs(v_name):
        """
        Perform recursive dfs at Vs.
        v_name : vertex name
        """
        pass
    
    result = {}
    result['dfs list'] = []
    result['tree edges'] = []
    result['forward edges'] = []
    result['cross edges'] = []
    
    # Mark all vertices as not visited

    # Check if V is visited. If not, start dfs at V
    if V and G.vertices[V].visited == False:
        do_dfs(V)
    
    # Find the next unvisited vertex and perform dfs until
    # all vertices are visited.

    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
