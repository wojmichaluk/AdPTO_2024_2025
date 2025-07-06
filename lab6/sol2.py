from dimacs import *
from pulp import *
from multiprocessing import Process
from graphs import graphs


# funkcja realizująca redukcję
def vc_to_ilp_reduction(G, name, pow, solver):
    n = len(G)
    E = edgeList(G)

    model = LpProblem("vc_to_ilp_reduction", LpMinimize)
    xs = [LpVariable(f"x_{i+1}", cat="Binary") for i in range(n)]
    degs = [len(v) for v in G]
    model += sum([xs[i] * power_fun(degs[i], pow) for i in range(n)])

    for (u, v) in E: 
        model += xs[u-1] + xs[v-1] >= 1

    if solver == "CBC":
        model.solve()
    elif solver == "GLPK":
        model.solve(pulp.GLPK_CMD(path="C:/glpk-4.65/w64/glpsol.exe", msg=False))

    C = []
    for i, x in enumerate(xs):
        if x.value() == 1.0:
            C.append(i+1)

    saveSolution(name + ".sol", C)
    return C


# pomocnicza funkcja potęgowa
def power_fun(deg, pow):
    return deg ** pow


# relaksacja LP - wariant ciągły
def vc_to_ilp_reduction_continuous(G, name, solver):
    n = len(G)
    E = edgeList(G)

    model = LpProblem("vc_to_ilp_reduction_continuous", LpMinimize)
    xs = [LpVariable(f"x_{i+1}", lowBound=0, upBound=1, cat="Continuous") for i in range(n)]
    model += sum(xs)

    for (u, v) in E: 
        model += xs[u-1] + xs[v-1] >= 1

    if solver == "CBC":
        model.solve()
    elif solver == "GLPK":
        model.solve(pulp.GLPK_CMD(path="C:/glpk-4.65/w64/glpsol.exe", msg=False))

    C = []
    for i, x in enumerate(xs):
        if x.value() >= 0.5:
            C.append(i+1)

    saveSolution(name + ".sol", C)
    return C


if __name__ == "__main__":
    for graph in graphs:
        G = loadGraph("graph/" + graph)

        # solwer CBC
        # podstawowa redukcja
        p1 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_cbc/deg_pow_0/" + graph, 0, "CBC"), name='p1')
        p1.start()
        p1.join(timeout=30)
        p1.terminate()

        # weighted vertex cover - wykładnik 1
        p2 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_cbc/deg_pow_1/" + graph, 1, "CBC"), name='p2')
        p2.start()
        p2.join(timeout=30)
        p2.terminate()

        # weighted vertex cover - wykładnik 3
        p3 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_cbc/deg_pow_3/" + graph, 3, "CBC"), name='p3')
        p3.start()
        p3.join(timeout=30)
        p3.terminate()

        # relaksacja LP
        p4 = Process(target=vc_to_ilp_reduction_continuous, args=(G, "vc_red_cbc/lp_relax/" + graph, "CBC"), name='p4')
        p4.start()
        p4.join(timeout=30)
        p4.terminate()

        # solwer GLPK
        # podstawowa redukcja
        p5 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_glpk/deg_pow_0/" + graph, 0, "GLPK"), name='p5')
        p5.start()
        p5.join(timeout=30)
        p5.terminate()

        # weighted vertex cover - wykładnik 1
        p6 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_glpk/deg_pow_1/" + graph, 1, "GLPK"), name='p6')
        p6.start()
        p6.join(timeout=30)
        p6.terminate()

        # weighted vertex cover - wykładnik 3
        p7 = Process(target=vc_to_ilp_reduction, args=(G, "vc_red_glpk/deg_pow_3/" + graph, 3, "GLPK"), name='p7')
        p7.start()
        p7.join(timeout=30)
        p7.terminate()

        # relaksacja LP
        p8 = Process(target=vc_to_ilp_reduction_continuous, args=(G, "vc_red_glpk/lp_relax/" + graph, "GLPK"), name='p8')
        p8.start()
        p8.join(timeout=30)
        p8.terminate()
