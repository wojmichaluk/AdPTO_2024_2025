from dimacs import loadGraph, edgeList
from graphs import graphs
from multiprocessing import Process
import pycosat
import os


# budowanie formuły logicznej - realizacja redukcji
def build_and_save_formula(G, k):
    n = len(G)
    E = edgeList(G)
    formula = []

    # klauzule dla wierzchołków
    for i in range(1, n):
        # wierzchołek ma co najmniej jeden kolor
        formula.append([(i-1) * n + c for c in range(1, k+1)])

        # wierzchołek ma dokładnie jeden kolor
        for j in range(1, k):
            for l in range(j+1, k+1):
                formula.append([-((i-1) * n + j), -((i-1) * n + l)])

    # klauzule dla krawędzi
    for vi, vt in E:
        for j in range(1, k+1):
            formula.append([-((vi-1) * n + j), -((vt-1) * n + j)])

    # zapis w tymczasowym pliku
    with open("temp.txt", "w") as f:
        for clause in formula:
            for literal in clause:
                f.write(f"{literal} ")
            
            f.write("\n")


# odczytanie formuły
def read_formula():
    formula = []

    with open("temp.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            clause = list(map(int, line.split(' ')[:-1]))
            formula.append(clause)

    os.remove("temp.txt")
    return formula


# rozwiązanie formuły i zapisanie rozwiązania
def solve_and_save(formula, n, sol_name):
    result = pycosat.solve(formula)

    with open(sol_name, "w") as f:
        for i, val in enumerate(result):
            if val > 0:
                color = (i+1) % n
                f.write(f"{color} ")


# weryfikacja poprawności rozwiązania
def verify(G, sol_name):
    E = edgeList(G)

    with open(sol_name, "r") as f:
        colors = [0] + list(map(int, f.readline().split(' ')[:-1]))
        
    for u, v in E:
        if colors[u] == colors[v]:
            return False
        
    return True


# główna część programu
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

    for i, (k, graph) in enumerate(zip(k_vals, graphs)):
        G = loadGraph(f"coloring/{graph}")
        sol_name = f"colors/{graph[:-4]}.sol"

        # ograniczenie czasowe na budowanie formuły
        p = Process(target=build_and_save_formula, args=(G, k), name='build')
        p.start()
        p.join(timeout=30)
        p.terminate()

        # odczytanie zapisanej formuły i rozwiązanie jej
        if os.path.exists("temp.txt"):
            formula = read_formula()

            # ograniczenie czasowe dla solwera pycosat
            p = Process(target=solve_and_save, args=(formula, len(G), sol_name), name='solve')
            p.start()
            p.join(timeout=30)
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
# Testy: DSJC500.9.col, DSJR500.1c.col, DSJ1000.5.col, flat1000_60_0.col, 
# flat1000_76_0.col dały niepoprawne wyniki (failed).
# Możliwe, że jest to spowodowane przerwaniem podczas zapisywania formuły
# do pliku / błędnym spisaniem wartości `k` z arkusza z grafami.
