from dimacs import *
from pulp import *
from multiprocessing import Process
from graphs import coloring_graphs
import os


# funkcja realizująca redukcję graph coloring do ilp
def gc_to_ilp_reduction(G, k, sol_name):
    n = len(G)
    E = edgeList(G)

    model = LpProblem("graph_coloring_to_ilp_reduction", LpMinimize)
    xs = [
        [LpVariable(f"x_{i+1}_{j+1}", cat="Binary") for j in range(k)]
        for i in range(n)
    ]

    # dodanie funkcji celu
    model += len(set([color_used(xs[i]) for i in range(n)]))

    # każdy wierzchołek posiada dokładnie jeden kolor
    for i in range(n):
        model += sum(xs[i]) <= 1
        model += sum(xs[i]) >= 1

    # oba wierzchołki w krawędzi nie mają tego samego koloru jednocześnie
    for (u, v) in E:
        for j in range(k):
            model += xs[u-1][j] + xs[v-1][j] <= 1

    # rozwiązanie układu z użyciem solwera GLPK
    model.solve(pulp.GLPK_CMD(path="C:/glpk-4.65/w64/glpsol.exe", msg=False))

    # odczytanie rozwiązania
    S = []

    for i in range(n):
        for j in range(k):
            if xs[i][j].value() == 1.0:
                S.append(j+1)

    # zapisanie rozwiązania
    with open(sol_name, "w") as f:
        for color in S:
            f.write(f"{color + 1} ")


# pomocnicza funkcja do określenia użytego koloru dla wierzchołka
def color_used(xsi):
    for j in range(len(xsi)):
        if xsi[j].value() == 1.0:
            return j


# funkcja weryfikująca poprawność rozwiązania
def verify(G, sol_name):
    E = edgeList(G)

    with open(sol_name, "r") as f:
        colors = [0] + list(map(int, f.readline().split(' ')[:-1]))
        
    for u, v in E:
        if colors[u] == colors[v]:
            return False
        
    return True


if __name__ == "__main__":
    # wartości k
    k_vals = [
        4, 6, 12, 28, 25, 31, 7, 40, 5, 7, 47, 65, 25, 31, 12, 42, 6, 8, 126, 30,  
        5, 31, 9, 50, 5, 9, 12, 30, 5, 4, 10, 40, 6, 4, 85, 9, 5, 5, 20, 41,  
        7, 5, 122, 13, 5, 6, 98, 40, 5, 8, 10, 11, 42, 7, 234, 7, 6, 9, 11, 54,  
        73, 8, 5, 49, 7, 20, 4, 31, 8, 11, 46, 30, 4, 82, 4, 31, 20, 11, 36, 30,  
        5, 222, 4, 10, 31, 12, 8, 6, 5, 11, 15, 4, 13, 64, 6, 17, 50, 15, 4, 14,  
        65, 7, 44, 60, 15, 4, 15, 14, 8, 8, 81, 15, 4, 16, 14, 4, 28, 20, 25, 49,  
        5, 41, 5, 72, 26, 25, 31, 7, 40
    ]

    for i, (k, graph) in enumerate(zip(k_vals, coloring_graphs)):
        G = loadGraph("coloring/" + graph)
        sol_name = f"colors/{graph[:-4]}.sol"

        # ograniczenie czasowe redukcji graph coloring do ilp
        p = Process(target=gc_to_ilp_reduction, args=(G, k, sol_name), name='red')
        p.start()
        p.join(timeout=60)
        p.terminate()

        # sprawdzenie poprawności rozwiązania
        if os.path.exists(sol_name):
            if verify(G, sol_name):
                print(f"Test: {i+1}, for: {graph} passed!")
            else:
                print(f"Test: {i+1}, for: {graph} failed!")
        else:
            print(f"Test: {i+1}, for: {graph} - no solution found!")


# ------------------------------------------------------------------
# P.S. 
# W tym przypadku żaden test nie dał błędnego wyniku (failed),
# ale przy porównywalnym ograniczeniu czasowym, co dla redukcji
# graph coloring -> SAT (łącznie 60s) jedynie w 37/129 testów 
# algorytm zdążył wykonać pełne obliczenia i zwrócić wynik.
