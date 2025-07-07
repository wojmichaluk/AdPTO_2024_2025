import os
from dimacs import edgeList, isVC, loadGRGraph, loadDecomposition
from graphs import graphs
from math import inf
from itertools import *
from multiprocessing import Process


# funkcja służąca do sprawdzenia, czy jeśli ograniczymy się w grafie G do wierzchołków 
# ze zbioru X, to wierzchołki ze zbioru Y stanowią pokrycie wierzchołkowe
def checkVC(G, X, Y):
    E = edgeList(G)
    E = list(filter(lambda e: e[0] in X and e[1] in X, E))
    return isVC(E, Y)


# główna funkcja w ramach algorytmu
def minVC(G, D):
    f_vals = dict()

    def f(y, C):
        nonlocal G
        nonlocal D
        nonlocal f_vals
        key = f"{C}_{y.id}"

        if f_vals.get(key) is not None:
            return f_vals[key]

        if not checkVC(G, y.bag, C):
            f_vals[key] = inf
        else:
            children = list(y.children)
            t = len(children)
            f_vals[key] = len(C)
            
            for i in range(t):
                child = D[children[i]]
                child_min = inf

                for s in range(len(child.bag) + 1):
                    for c in combinations(child.bag, s):
                        Di = set(c)

                        if Di & y.bag == C & child.bag:
                            child_min = min(
                                child_min,
                                f(child, Di) - len(child.bag & C)
                            )

                f_vals[key] += child_min
        
        return f_vals[key]
    

    min_vc = inf

    for s in range(len(D[1].bag) + 1):
        for c in combinations(D[1].bag, s):
            C = set(c)
            min_vc = min(min_vc, f(D[1], C))

    # zapisanie rozwiązania
    with open("temp.txt", "w") as f:
        f.write(f"{min_vc}")


# główna część programu
if __name__ == "__main__":
    for graph in graphs:
        G = loadGRGraph("graphtw/" + graph + ".gr")
        D = loadDecomposition("graphtw/" + graph + ".tw")

        # obliczanie rozmiaru minimalnego pokrycia wierzchołkowego
        print(f"Rozmiar minimalnego pokrycia wierzchołkowego dla grafu '{graph}':", end=' ')
        p = Process(target=minVC, args=(G, D), name='process')
        p.start()
        p.join(timeout=208) # dla takiego limitu czasu test 1. oraz 5. już się obliczyły,
                            # test 7. wymaga mniej czasu od nich, ale więcej niż pozostałe
        p.terminate()

        # sprawdzenie, czy obliczono wynik
        if os.path.exists("temp.txt"):
            with open("temp.txt", "r") as f:
                result = int(f.readlines()[0])
                print(result)

            os.remove("temp.txt")
        else:
            print("Przekroczono limit czasu!")
