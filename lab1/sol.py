from dimacs import *
from itertools import *
from copy import deepcopy
from graphs import graphs
from multiprocessing import Process


# bruteforce
def bruteforce(G, name):
    n = len(G)
    E = edgeList(G)

    for k in range(n):
        for C in combinations(range(n), k):
            if isVC(E, C):
                saveSolution(name + ".sol", C)
                return C


# rekurencja z powrotami, 2^k
def rek1_zew(G, name):
    n = len(G)

    for k in range(n):
        C = rek1(G, k, [])

        if C is not None:
            saveSolution(name + ".sol", C)
            return C


def rek1(G, k, S):
    E = edgeList(G)
    edge = None

    for e in E:
        u, v = e

        if u not in S and v not in S:
           edge = e
           break

    if edge is None:
        return S
    
    if k == 0:
        return None
    
    S1 = rek1(remove_vertex(G, edge[0]), k-1, S + [u])
    S2 = rek1(remove_vertex(G, edge[1]), k-1, S + [v])

    return S1 if S1 else S2


# funkcja pomocnicza
def remove_vertex(G, v):
    G = deepcopy(G)

    for u in G[v].copy():
        G[u].remove(v)
        G[v].remove(u)

    return G


# rekurencja z powrotami, 1.618^k
def rek2_zew(G, name):
    n = len(G)

    for k in range(n):
        C = rek2(G, k, [])

        if C is not None:
            saveSolution(name + ".sol", C)
            return C

   
def rek2(G, k, S):
    if k < 0:
        return None

    E = edgeList(G)

    if len(E) == 0:
        return S
    if k == 0:
        return None

    u = E[0][0]
    
    S1 = rek2(remove_vertex(G, u), k-1, S + [u])

    Nu = list(G[u])
    G_copy = G

    for v in Nu:
        G_copy = remove_vertex(G_copy, v)

    S2 = rek2(G_copy, k-len(Nu), S + Nu)

    return S1 if S1 else S2


# rekurencja z powrotami, 1.47^k
def rek3_zew(G, name):
    n = len(G)

    for k in range(n):
        C = rek3(G, k, [])

        if C is not None:
            saveSolution(name + ".sol", C)
            return C


def rek3(G, k, S):
    if k < 0:
        return None

    E = edgeList(G)

    if len(E) == 0:
        return S
    if k == 0:
        return None

    u, ns = choose_vertex(G)

    if ns == 1:
        G_copy = remove_vertex(G, u)
        G_copy = remove_vertex(G_copy, list(G[u])[0])

        return rek3(G_copy, k-1, S + list(G[u]))
    else:
        S1 = rek3(remove_vertex(G, u), k-1, S + [u])

        Nu = list(G[u])
        G_copy = G

        for v in Nu:
            G_copy = remove_vertex(G_copy, v)

        S2 = rek3(G_copy, k-len(Nu), S + Nu)

        return S1 if S1 else S2


# funkcja pomocnicza
def choose_vertex(G):
    high = 0
    best_v = None

    for v, ns in enumerate(G):
        if len(ns) == 1:
            return v, 1
        
        if len(ns) > high:
            high = len(ns)
            best_v = v

    return best_v, high


# kernelizacja + poprzedni algorytm
def kernelization_zew(G, name):
    n = len(G)

    for k in range(n):
        C = kernelization(G, k, [])

        if C is not None:
            saveSolution(name + ".sol", C)
            return C


def kernelization(G, k, S):
    G_copy = deepcopy(G)
    active_vertices = [True for _ in range(len(G))]

    while k >= 0:
        v, d = edge_case_vertex(G_copy, k, active_vertices)

        if v is not None:
            if d == 0:
                active_vertices[v] = False # zamiast usuwania
            elif d == 1:
                S += list(G_copy[v])
                k -= 1
            else:
                S += [v]
                k -= 1
            
            continue
            
        break

    if len(edgeList(G_copy)) > k*k:
       return None
    
    return rek3(G_copy, k, S)
            

# funkcja pomocnicza
def edge_case_vertex(G, k, active_vertices):
    for v, ns in enumerate(G):
        if active_vertices[v]: 
            if len(ns) == 0:
                return v, 0
            
            if len(ns) == 1:
                return v, 1
            
            if len(ns) > k:
                return v, 2
        
    return None, None


# główna część programu
if __name__ == "__main__":
    for graph in graphs:
        G = loadGraph("graph/" + graph)

        # bruteforce
        p1 = Process(target=bruteforce, args=(G, "graph_bruteforce/" + graph), name='p1')
        p1.start()
        p1.join(timeout=5)
        p1.terminate()

        # rekurencja z powrotami, 2^k
        p2 = Process(target=rek1_zew, args=(G, "graph_rek1/" + graph), name='p2')
        p2.start()
        p2.join(timeout=5)
        p2.terminate()
        
        # rekurencja z powrotami, 1.618^k
        p3 = Process(target=rek2_zew, args=(G, "graph_rek2/" + graph), name='p3')
        p3.start()
        p3.join(timeout=5)
        p3.terminate()

        # rekurencja z powrotami, 1.47^k
        p4 = Process(target=rek3_zew, args=(G, "graph_rek3/" + graph), name='p4')
        p4.start()
        p4.join(timeout=5)
        p4.terminate()

        # kernelizacja + rekurencja z powrotami, 1.47^k
        p5 = Process(target=kernelization_zew, args=(G, "graph_kernelization/" + graph), name='p5')
        p5.start()
        p5.join(timeout=5)
        p5.terminate()
