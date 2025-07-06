from dimacs import edgeList, saveSolution, loadGraph
from multiprocessing import Process
import pycosat
from graphs import graphs

# można użyć własny solwer (z poprzedniego laboratorium)
# from sat_solver import solve


# prosta redukcja VC do SAT
def vc_to_sat_reduction(G, name):
    E = edgeList(G)
    CNF = []

    for (vi, vj) in E:
        CNF.append([vi, vj])

    # V = solve(CNF)
    V = pycosat.solve(CNF)
    C = []

    for v in V:
        # if v > 0 and V[v] == 1:
        if v > 0:
            C.append(v)

    saveSolution(name + ".sol", C)
    return C


# główna część programu
if __name__ == "__main__":
    for graph in graphs:
        G = loadGraph("graph/" + graph)

        # redukcja vertex cover do sat bez ograniczenia liczby wierzchołków
        p = Process(
            target=vc_to_sat_reduction,
            args=(G, "graph_sol1/" + graph),
            name='p'
        )
        p.start()
        p.join(timeout=5)
        p.terminate()
