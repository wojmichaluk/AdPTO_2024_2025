from dimacs import edgeList, saveSolution, loadGraph
from multiprocessing import Process
import pycosat
from graphs import graphs

# można użyć własny solwer (z poprzedniego laboratorium)
# from sat_solver import solve


# pomocnicza funkcja do jednoznacznego indeksowania
def index(i, j, shift):
    return ((i+j) * (i+j+1)) // 2 + i + shift


# wymuszenie, żeby najwyżej k zmiennych miało wartość prawda
def dp_correction(G, k, name):
    n = len(G)
    E = edgeList(G)
    CNF = []

    # nie zapominajmy o krawędziach
    for (vi, vj) in E:
        CNF.append([vi, vj])

    # zmienne y_{i,0} są prawdziwe
    for i in range(n+1):
        CNF.append([index(i, 0, n+1)])

    # zmienne y_{0,j} są fałszywe
    for j in range(1, n+1):
        CNF.append([-index(0, j, n+1)])

    # odpowiednie implikacje
    for i in range(1, n+1):
        for j in range(1, n+1):
            CNF.append([-index(i-1, j, n+1), index(i, j, n+1)])
            CNF.append([-index(i-1, j-1, n+1), -i, index(i, j, n+1)])

    CNF.append([-index(n, k+1, n+1)])

    # V = solve(CNF)
    V = pycosat.solve(CNF)
    C = []

    for v in V:
        # if 0 < v <= n and V[v] == 1:
        if 0 < v <= n:
            C.append(v)

    saveSolution(name + ".sol", C)
    return C


# główna część programu
if __name__ == "__main__":
    for graph in graphs:
        G = loadGraph("graph/" + graph)

        # ograniczenie liczby wierzchołków - podejście dynamiczne
        p = Process(
            target=dp_correction,
            args=(G, len(G), "graph_sol2/" + graph),
            name='p'
        )
        p.start()
        p.join(timeout=15) # 15 wystarcza dla wszystkich testów poza b_100,
                           # dla 120 ten test dalej nie przechodzi - odpuściłem
        p.terminate()
