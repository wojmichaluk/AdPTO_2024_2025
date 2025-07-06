import networkx as nx
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort
from dimacs import *
from sys    import argv



def sat2cnf( CNF, VALUE ):
    V = max( max([abs(x) for x in C]) for C in CNF )

    G = nx.DiGraph()
    G.add_nodes_from(range(1,V+1))
    G.add_nodes_from( [-x for x in range(1,V+1)] )

    for (x,y) in CNF:
        G.add_edge(-x,y)
        G.add_edge(-y,x)
    H = nx.DiGraph()
    scc = []
    v2scc = {}

    SCC = strongly_connected_components(G)
    t = 0
    for S in SCC:
        H.add_node(t)
        scc.append(S)
        for x in S:
            v2scc[x] = t
        t += 1


    for v in range(1,V+1):
        if v2scc[v] == v2scc[-v]:
            return "UNSAT"

    for (u,v) in G.edges:
        if v2scc[u] != v2scc[v]:
            H.add_edge( v2scc[u], v2scc[v] )

    O = topological_sort( H )
    
    for v in O:
        for x in scc[v]:
            if abs(x) in VALUE:
                continue
            VALUE[ x] = -1
            VALUE[-x] = 1
        
    return VALUE
