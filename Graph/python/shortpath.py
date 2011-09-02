#!/usr/bin/env python
import heapq
import disjset

FIG9_8 = { 'v1': {'v2': 2, 'v4': 1},
           'v2': {'v4': 3, 'v5': 10},
           'v3': {'v1': 4, 'v6': 5},
           'v4': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4},
           'v5': {'v7': 6},
           'v6': {},
           'v7': {'v6': 1} }

FIG9_48 = { 'v1': {'v2': 2, 'v3': 4, 'v4': 1},
            'v2': {'v1': 2, 'v4': 3, 'v5': 10},
            'v3': {'v1': 4, 'v4': 2, 'v6': 5},
            'v4': {'v1': 1, 'v2': 3, 'v3': 2, 'v5': 7, 'v6': 8, 'v7': 4},
            'v5': {'v2': 10, 'v4': 7, 'v7': 6},
            'v6': {'v3': 5, 'v4': 8, 'v7': 1},
            'v7': {'v4': 4, 'v5': 6, 'v6': 1} }

class Vertex(object):
    """A vertex in a graph."""
    def __init__(self, name, adj):
        """Initialize with name and adj list"""
        super(Vertex, self).__init__()
        self.name = name
        self.adj = adj.copy()

    def __repr__(self):
        return "<%s: %s>" % (self.name, self.__dict__)
    
class Graph(object):
    """Dictionary of vertices

    >>> graph = Graph(FIG9_8)
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


class PriorityQueue(object):
    """Simple list based priority queue

    >>> queue = PriorityQueue()
    >>> queue.enqueue(5); queue.enqueue(4); queue.enqueue(1)
    >>> queue
    <PriorityQueue: [1, 4, 5]>
    >>> queue.change_key(4, 2)
    >>> queue
    <PriorityQueue: [1, 2, 5]>
    >>> queue.dequeue()
    1
    >>> queue.dequeue()
    2
    >>> queue
    <PriorityQueue: [5]>
    """
    
    def __init__(self, cmp=cmp):
        super(PriorityQueue, self).__init__()
        self.cmp = cmp
        self.list = []

    def __repr__(self):
        return "<PriorityQueue: %s>" % self.list

    def __len__(self):
        return len(self.list)

    def enqueue(self, key):
        """Add a new key"""
        self.list.append(key)
        self.sort()
        
    def dequeue(self):
        """Return key at the head of the queue"""
        return self.list.pop(0)

    def change_key(self, key, newkey):
        """Changes key to newkey."""
        if key in self.list:
            self.list.remove(key)
            self.list.append(newkey)
            self.sort()
        else:
            raise KeyError('No such key')
                
    def sort(self):
        """Maintain heap invariant"""
        self.list.sort(self.cmp)

def shortest_path(graph, s):
    """Single source shortest path.

    graph : a graph with no negative edge weight
    s     : source vertex

    >>> shortest_path(Graph(FIG9_8), 'v1')
    <Graph:
     <v1: {'cost': 0, 'adj': {'v2': 2, 'v4': 1}, 'name': 'v1'}>
     <v2: {'path': 'v1', 'cost': 2, 'adj': {'v4': 3, 'v5': 10}, 'name': 'v2'}>
     <v3: {'path': 'v4', 'cost': 3, 'adj': {'v1': 4, 'v6': 5}, 'name': 'v3'}>
     <v4: {'path': 'v1', 'cost': 1, 'adj': {'v3': 2, 'v5': 2, 'v6': 8, 'v7': 4}, 'name': 'v4'}>
     <v5: {'path': 'v4', 'cost': 3, 'adj': {'v7': 6}, 'name': 'v5'}>
     <v6: {'path': 'v7', 'cost': 6, 'adj': {}, 'name': 'v6'}>
     <v7: {'path': 'v4', 'cost': 5, 'adj': {'v6': 1}, 'name': 'v7'}> >
    """
    INF = 9999999999

    # set inital costs to INF except for s
    queue = PriorityQueue(lambda x,y: cmp(x.cost, y.cost))
    for v in graph:
        graph[v].cost = INF
        queue.enqueue(graph[v])
    graph[s].cost = 0
    queue.sort()

    # relax each vertex
    while len(queue):
        v = queue.dequeue().name
        for a, weight in graph[v].adj.items():
            if graph[a].cost > graph[v].cost + weight:
                graph[a].path = v
                graph[a].cost = graph[v].cost + weight
        queue.sort()
        #print queue
    print graph

def prim(graph, s=None):
    """Find minimum spanning tree for undirected graph
    using Prim's algorithm with vertex s as root.

    >>> prim(Graph(FIG9_48), 'v1')
    [('v1', 'v4'), ('v1', 'v2'), ('v4', 'v3'), ('v4', 'v7'), ('v7', 'v6'), ('v7', 'v5')]
    >>> prim(Graph(FIG9_48))
    [('v1', 'v4'), ('v1', 'v2'), ('v4', 'v3'), ('v4', 'v7'), ('v7', 'v6'), ('v7', 'v5')]
    """
    if s is None:
        s = graph.vertices.keys()[0]
    span_tree = []                             # edges of resulting span tree
    pq = []                                    # priority queue
    added = dict([(v, False) for v in graph])  # v added to span tree yet?

    # add s to span tree
    added[s] = True
    for adj, weight in graph[s].adj.items():
        heapq.heappush(pq, (weight, (adj, s)))

    # greedily add shortest edges
    while pq:
        # get the next shortest edge
        weight, (v, src) = heapq.heappop(pq)

        # discard if edge is to an added vertex
        if added[v]:
            continue

        # add vertex to span tree
        added[v] = True
        span_tree.append((src, v))
        #print span_tree

        # add all edges to adj vertices not already in span tree
        for adj, weight in graph[v].adj.items():
            if not added[adj]:
                heapq.heappush(pq, (weight, (adj, v)))
        
    return span_tree

def kruskal(graph):
    """Solve minimum spanning tree problem for undirected graphs
    using Kruskal's algorithm.
    
    >>> kruskal(Graph(FIG9_48))
    {'v2': set(['v2']), 'v3': set(['v3']), 'v4': set(['v1', 'v4']), 'v5': set(['v5']), 'v6': set(['v6']), 'v7': set(['v7'])}
    {'v2': set(['v2']), 'v3': set(['v3']), 'v4': set(['v1', 'v4']), 'v5': set(['v5']), 'v7': set(['v6', 'v7'])}
    {'v3': set(['v3']), 'v4': set(['v1', 'v2', 'v4']), 'v5': set(['v5']), 'v7': set(['v6', 'v7'])}
    {'v4': set(['v1', 'v2', 'v3', 'v4']), 'v5': set(['v5']), 'v7': set(['v6', 'v7'])}
    {'v5': set(['v5']), 'v7': set(['v1', 'v2', 'v3', 'v4', 'v6', 'v7'])}
    {'v7': set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7'])}
    [('v1', 'v4'), ('v6', 'v7'), ('v1', 'v2'), ('v3', 'v4'), ('v4', 'v7'), ('v5', 'v7')]
    """
    span_tree = []  # edges that constitute span tree
    
    # Start out by putting each vertex in its own set
    sets = disjset.DisjSet()
    for v in graph.vertices:
        sets.makeSet(v)

    # Push all edges in to priority queue. Note that
    # we'll have duplicates in form of (weight, (v1, v2)) and
    # (weight, (v2, v1)). We don't worry about it.
    
    pq = []  # priority queue of all edges by their lengths
    for v in graph.vertices:
        for a, w in graph.vertices[v].adj.items():
            heapq.heappush(pq, (w, (v, a)))

    # Join sets by shortest edges
    #import pdb; pdb.set_trace()
    edges_accepted = 0
    while edges_accepted < len(graph.vertices) - 1:
        w, (v1, v2) = heapq.heappop(pq)

        # Skip if v1 and v2 already in the same set
        root1 = sets.find(v1)
        root2 = sets.find(v2)
        if root1 == root2:
            continue
        sets.merge( root1, root2 )

        print sets
        
        # add (v1, v2) to solution
        edges_accepted += 1
        span_tree.append((v1, v2))

    return span_tree
        
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
