from dimacs import edgeList, saveSolution, loadGraph
from multiprocessing import Process
from sat_solver import solve
from sortnet import sorterNet
from graphs import graphs


# główna część programu
if __name__ == "__main__":
    # próby z siecią sortującą
    sn = sorterNet(1, [0, 1, 2, 3], True)
    sn.comp(1, 2)
    sn.comp(2, 3)
    sn.comp(1, 2)
    print(sn.getLines())
