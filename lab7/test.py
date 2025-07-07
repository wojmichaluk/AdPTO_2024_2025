from dimacs import loadGRGraph, loadDecomposition


if __name__ == "__main__":
    filename = "graphtw/e5"
    graph = loadGRGraph(filename + ".gr")
    decomposition = loadDecomposition(filename + ".tw")
    print(graph)

    for node in decomposition[1:]:
        print(node.id)
        print(node.parent)
        print(node.children)
        print(node.bag, "\n")
