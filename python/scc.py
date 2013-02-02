#!/usr/bin/env python
"""
Implements strongly connected components algorithms.

Input is a directed graph. 
"""

from graph import Graph

def Kosaraju(G):
    """
    >>> G = Graph.loadFromFile('scc0.txt', one_based=True)
    >>> SCCs = Kosaraju(G)
    >>> SCCs
    [[0, 3, 6], [8, 2, 5], [7, 4, 1]]
    """
    def dfs1(vIdx):
        "First pass depth first search"
        stack = [(vIdx, G.getVertTailIter(vIdx))]
        # Set True when put on stack
        queued[vIdx] = True
        while stack:
            (v, gen) = stack[-1]
            try:
                eIdx = gen.next()
                vChild = G.getEdge(eIdx)[1]
                if not queued[vChild]:
                    genChild = G.getVertTailIter(vChild)
                    stack.append((vChild, genChild))
                    # Set True when put on stack
                    queued[vChild] = True
            except StopIteration:
                pass2Order.append(v)
                stack.pop()
                
    def dfs2(vIdx):
        "Second pass depth first search; Edges reversed"
        scc = []
        stack = [vIdx]
        # Set to True when node is inserted into stack
        queued[vIdx] = True
        while stack:
            v = stack.pop()
            scc.append(v)
            for eIdx in G.getVertHead(v):
                adjV = G.getEdge(eIdx)[0]
                if not queued[adjV]:
                    # Set to True when node is inserted into stack
                    queued[adjV] = True
                    stack.append(adjV)
        return scc
    
    #print "First pass ..."
    pass2Order = []   # Nodes are kept in order of completing pass 1
    queued = [False] * G.numVerts    # Keeps track of verts queued into stack
    
    for i in xrange(G.numVerts):
        if not queued[i]:
            dfs1(i)

    #print pass2Order
    
    #print "Second pass ..."
    queued = [False] * G.numVerts  # Keeps track of verts queued into stack

    result = []
    while pass2Order:
        v = pass2Order.pop()
        if not queued[v]:
            scc = dfs2(v)
            result.append(scc)
    return result
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    
