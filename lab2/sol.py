from dimacs import *
from itertools import *
from multiprocessing import Process
from random import shuffle, randint, random
from math import exp
from graphs import graphs


# 2-aproksymacja
def two_approx(G, name):
    E = edgeList(G)
    C = []

    while True:
        for e in E:
            u, v = e

            if u not in C and v not in C:
                C.append(u)
                C.append(v)
                break

        if isVC(E, C):
            saveSolution(name + ".sol", C)
            return C

       
# logn-aproksymacja
def logn_approx(G, name):
    E = edgeList(G)
    C = []

    while True:
        v = find_max_degree_vertex(G)
        C.append(v)
        remove_vertex(G, v)
        
        if isVC(E, C):
            saveSolution(name + ".sol", C)
            return C


# funkcja pomocnicza
def find_max_degree_vertex(G):
    max_deg = -1
    max_v = -1

    for v, ns in enumerate(G):
        if len(ns) > max_deg:
            max_deg = len(ns)
            max_v = v

    return max_v


# funkcja pomocnicza
def remove_vertex(G, v):
    for u in G[v].copy():
        G[u].remove(v)
        G[v].remove(u)


# metoda simulated annealing
# na podstawie https://www.sciencedirect.com/science/article/abs/pii/S0925231205003565
def simulated_annealing(G, name):
    # przyjęte wartości parametrów
    T = 50
    L = 100
    alfa = 0.95

    n = len(G)
    E = edgeList(G)

    # stan początkowy
    C = set()
    v = [randint(0, 1) for _ in range(n)]

    for i, vertex in enumerate(v):
        if vertex:
            C.add(i)

    # pomocnicze zmienne
    d = [[
        1 if u in G[v] else 0 
        for u in range(n)] 
        for v in range(n)
    ]
    flag = False
    i = 0

    while i < L or not isVC(E, list(C)):
        if not flag:
            F = object_function(v, d)

        vertex = randint(0, n-1)
        if v[vertex]: C.remove(vertex)
        else: C.add(vertex)

        v[vertex] = 1 - v[vertex]
        F_prim = object_function(v, d)
        delta_F = F_prim - F
        flag = True

        if delta_F > 0:
            deg = len(G[vertex]) / len(E)
            p = p_fun(delta_F, deg, T, v[vertex])

            if random() > p:
                # reverting change
                v[vertex] = 1 - v[vertex]
                if v[vertex]: C.add(vertex)
                else: C.remove(vertex)
                flag = False

        T *= alfa
        i += 1

    C = list(C)
    saveSolution(name + ".sol", C)
    return C


# funkcja pomocnicza
def object_function(v, d):
    return sum(v) +\
        sum([
            d[i][j] * (v[i]*v[j] - v[i] - v[j]) 
            for i in range(len(v))
            for j in range(len(v)) 
        ]) +\
        sum([sum(d[i]) for i in range(len(v))])


# funkcja pomocnicza
def p_fun(delta_F, deg, T, vi):
    return exp(-delta_F * (1 + (-1)**vi * deg) / T)


# losowe usuwanie wierzchołków z rozwiązania wcześniejszymi algorytmami
def random_approx(G, sol_name, name):
    E = edgeList(G)

    try:
        f = open(sol_name + ".sol", "r")
    except IOError:
        return

    s = f.readline().strip()
    C = s.split(',')
    C = [int(c) for c in C]

    # aby usuwać wierzchołki w losowej kolejności
    shuffle(C)
    C = set(C)

    for v in C.copy():
        C.remove(v)
        
        if not isVC(E, C):
            C.add(v)

    C = list(C)
    saveSolution(name + ".sol", C)
    return C


# główna część programu
if __name__ == "__main__":
    for graph in graphs:
        G = loadGraph("graph/" + graph)

        # algorytm 2-aproksymacyjny
        p1 = Process(target=two_approx, args=(G, "graph_2aproks/" + graph), name='p1')
        p1.start()
        p1.join(timeout=22) # dla tej wartości przechodzi wszystkie testy oprócz f56
                            # dla timeout=122 dalej go nie przechodzi - większych nie testowałem
        p1.terminate()

        # algorytm logn-aproksymacyjny
        p2 = Process(target=logn_approx, args=(G, "graph_lognaproks/" + graph), name='p2')
        p2.start()
        p2.join(timeout=23) # dla tej wartości przechodzi wszystkie testy
        p2.terminate()

        # metoda simulated annealing
        p3 = Process(target=simulated_annealing, args=(G, "graph_sa/" + graph), name='p3')
        p3.start()
        p3.join(timeout=20) # aby wyniki były porównywalne
        p3.terminate()

        # usuwanie w losowej kolejności wierzchołków z rozwiązania algorytmu 2-aproksymacyjnego
        p4 = Process(target=random_approx, args=(G, "graph_2aproks/" + graph, "graph_2aproks_random/" + graph), name='p4')
        p4.start()
        p4.join(timeout=5)
        p4.terminate()

        # usuwanie w losowej kolejności wierzchołków z rozwiązania algorytmu logn-aproksymacyjnego
        p5 = Process(target=random_approx, args=(G, "graph_lognaproks/" + graph, "graph_lognaproks_random/" + graph), name='p5')
        p5.start()
        p5.join(timeout=5)
        p5.terminate()

        # usuwanie w losowej kolejności wierzchołków z rozwiązania algorytmu logn-aproksymacyjnego
        p6 = Process(target=random_approx, args=(G, "graph_sa/" + graph, "graph_sa_random/" + graph), name='p6')
        p6.start()
        p6.join(timeout=5)
        p6.terminate()
        