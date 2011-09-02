#!/usr/bin/env python
"""
Graph class.
"""

DIRECTED = { 'v1': {'v2': 2, 'v4': 1},
             'v2': {'v4': 3, 'v5': 10},
             'v3': {'v1': 4, 'v6': 5},
             'v4': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4},
             'v5': {'v7': 6},
             'v6': {},
             'v7': {'v6': 1} }

UNDIRECTED = { 'v1': {'v3': 1, 'v4': 1},
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

class Vertex(object):
    """A vertex in a graph."""
    def __init__(self, name, adj):
        """Initialize with name and adj list"""
        super(Vertex, self).__init__()
        self.name = name
        self.adj = adj.copy()

    def __repr__(self):
        return "<%s: %s>" % (self.name, self.__dict__)

    def clone(self):
        return Vertex(self.name, self.adj)
    
class Graph(object):
    """Dictionary of vertices

    >>> graph = Graph(DIRECTED)
    >>> graph
    <Graph:
     <v1: {'adj': {'v2': 2, 'v4': 1}, 'name': 'v1'}>
     <v2: {'adj': {'v4': 3, 'v5': 10}, 'name': 'v2'}>
     <v3: {'adj': {'v1': 4, 'v6': 5}, 'name': 'v3'}>
     <v4: {'adj': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4}, 'name': 'v4'}>
     <v5: {'adj': {'v7': 6}, 'name': 'v5'}>
     <v6: {'adj': {}, 'name': 'v6'}>
     <v7: {'adj': {'v6': 1}, 'name': 'v7'}> >
    >>> graph['v1']
    <v1: {'adj': {'v2': 2, 'v4': 1}, 'name': 'v1'}>
    >>> graph.num_edges()
    12
    >>> graph.num_vertices()
    7
    >>> graph.remove_edge('v1', 'v2')
    >>> graph
    <Graph:
     <v1: {'adj': {'v4': 1}, 'name': 'v1'}>
     <v2: {'adj': {'v4': 3, 'v5': 10}, 'name': 'v2'}>
     <v3: {'adj': {'v1': 4, 'v6': 5}, 'name': 'v3'}>
     <v4: {'adj': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4}, 'name': 'v4'}>
     <v5: {'adj': {'v7': 6}, 'name': 'v5'}>
     <v6: {'adj': {}, 'name': 'v6'}>
     <v7: {'adj': {'v6': 1}, 'name': 'v7'}> >
    >>> graph.num_edges()
    11
    >>> graph.num_vertices()
    7
    >>> graph.clone()
    <Graph:
     <v1: {'adj': {'v4': 1}, 'name': 'v1'}>
     <v2: {'adj': {'v4': 3, 'v5': 10}, 'name': 'v2'}>
     <v3: {'adj': {'v1': 4, 'v6': 5}, 'name': 'v3'}>
     <v4: {'adj': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4}, 'name': 'v4'}>
     <v5: {'adj': {'v7': 6}, 'name': 'v5'}>
     <v6: {'adj': {}, 'name': 'v6'}>
     <v7: {'adj': {'v6': 1}, 'name': 'v7'}> >
    
    >>> graph = Graph(UNDIRECTED)
    >>> graph
    <Graph:
     <v12: {'adj': {'v9': 1, 'v10': 1}, 'name': 'v12'}>
     <v10: {'adj': {'v4': 1, 'v5': 1, 'v7': 1, 'v12': 1, 'v9': 1, 'v11': 1}, 'name': 'v10'}>
     <v11: {'adj': {'v10': 1, 'v4': 1}, 'name': 'v11'}>
     <v1: {'adj': {'v3': 1, 'v4': 1}, 'name': 'v1'}>
     <v2: {'adj': {'v8': 1, 'v3': 1}, 'name': 'v2'}>
     <v3: {'adj': {'v1': 1, 'v2': 1, 'v4': 1, 'v6': 1, 'v7': 1, 'v9': 1}, 'name': 'v3'}>
     <v4: {'adj': {'v1': 1, 'v3': 1, 'v5': 1, 'v7': 1, 'v10': 1, 'v11': 1}, 'name': 'v4'}>
     <v5: {'adj': {'v10': 1, 'v4': 1}, 'name': 'v5'}>
     <v6: {'adj': {'v9': 1, 'v3': 1}, 'name': 'v6'}>
     <v7: {'adj': {'v9': 1, 'v10': 1, 'v3': 1, 'v4': 1}, 'name': 'v7'}>
     <v8: {'adj': {'v9': 1, 'v2': 1}, 'name': 'v8'}>
     <v9: {'adj': {'v8': 1, 'v3': 1, 'v6': 1, 'v7': 1, 'v12': 1, 'v10': 1}, 'name': 'v9'}> >
    >>> graph.num_edges()
    42
    >>> graph.num_vertices()
    12
    >>> graph.remove_edge('v1', 'v3')
    >>> graph
    <Graph:
     <v12: {'adj': {'v9': 1, 'v10': 1}, 'name': 'v12'}>
     <v10: {'adj': {'v4': 1, 'v5': 1, 'v7': 1, 'v12': 1, 'v9': 1, 'v11': 1}, 'name': 'v10'}>
     <v11: {'adj': {'v10': 1, 'v4': 1}, 'name': 'v11'}>
     <v1: {'adj': {'v4': 1}, 'name': 'v1'}>
     <v2: {'adj': {'v8': 1, 'v3': 1}, 'name': 'v2'}>
     <v3: {'adj': {'v2': 1, 'v4': 1, 'v6': 1, 'v7': 1, 'v9': 1}, 'name': 'v3'}>
     <v4: {'adj': {'v1': 1, 'v3': 1, 'v5': 1, 'v7': 1, 'v10': 1, 'v11': 1}, 'name': 'v4'}>
     <v5: {'adj': {'v10': 1, 'v4': 1}, 'name': 'v5'}>
     <v6: {'adj': {'v9': 1, 'v3': 1}, 'name': 'v6'}>
     <v7: {'adj': {'v9': 1, 'v10': 1, 'v3': 1, 'v4': 1}, 'name': 'v7'}>
     <v8: {'adj': {'v9': 1, 'v2': 1}, 'name': 'v8'}>
     <v9: {'adj': {'v8': 1, 'v3': 1, 'v6': 1, 'v7': 1, 'v12': 1, 'v10': 1}, 'name': 'v9'}> >
    >>> graph.num_edges()
    40
    >>> graph.num_vertices()
    12
    """
    def __init__(self, adj={}):
        super(Graph, self).__init__()
        self.vertices = {}
        for v in adj:
            self.vertices[v] = Vertex(v, adj[v])
            
    def __repr__(self):
        res = "<Graph:"
        for name, v in self.vertices.items():
            res += "\n %s" % v
        res += " >"
        return res
    
    def __getitem__(self, name):
        return self.vertices[name]

    def __iter__(self):
        return iter(self.vertices)

    def clone(self):
        """
        Make a copy of self.
        """
        cloned = Graph()
        for v in self.vertices:
            cloned.vertices[v] = self.vertices[v].clone()
        return cloned

    def remove_edge(self, v1, v2):
        """
        Remove the edge connecting vertices v1 and v2.
        This results in removing 'two' edges in case
        of undirected graph.
        
        v1 : name of vertex
        v2 : name of vertex
        """
        verts = self.vertices
        if v1 in verts and v2 in verts[v1].adj:
            del verts[v1].adj[v2]
        if v2 in verts and v1 in verts[v2].adj:
            del verts[v2].adj[v1]

    def num_edges(self):
        """
        Return number of edges. Note that for undirected graphs
        each edges are counted twice.
        """
        return sum(len(v.adj) for v in self.vertices.values())

    def num_vertices(self):
        """
        Return number of vertices.
        """
        return len(self.vertices)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
