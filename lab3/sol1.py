import pycosat
import random
from matplotlib import pyplot as plt


# generowanie losowej formuły logicznej
def generate_formula(vars, clauses, k):
    S = [1,-1]
    V = range(1, vars+1)
    formula = []

    for _ in range(clauses):
        clause = []

        for _ in range(k):
            x = random.choice(V) * random.choice(S)
            clause.append(x)

        formula.append(clause)     

    return formula


# narysowanie wykresu zależności S/T od a
def plot(names, ns, k):
    xss = []
    yss = []

    for name in names:
        with open(name, "r") as f:
            lines = f.readlines()
            xs = []
            ys = []

            for line in lines:
                x, y = list(map(float, line.split(' ')))
                xs.append(x)
                ys.append(y)

            xss.append(xs)
            yss.append(ys)

    for i in range(len(ns)):
        plt.plot(xss[i], yss[i], label=f"n={ns[i]}")

    # opis wykresu
    plt.title(f"Przejście fazowe dla różnych wartości n, k={k}")
    plt.xlabel("wartości współczynnika a")
    plt.ylabel("wartości ilorazu S/T")
    plt.legend()
    plt.savefig(f"graphs/graph_k{k}.png")
    plt.show()


# główna część programu
if __name__ == "__main__":
    # badane wartości parametrów
    ks = [2, 3, 4, 5]
    ns = [[10, 50, 100], [10, 50, 100], [10, 25, 50], [10, 25, 50]]
    T = 100
    As = [
        [a / 10 for a in range(10, 51)],
        [a / 10 for a in range(10, 101)],
        [a / 10 for a in range(50, 151)],
        [a / 10 for a in range(180, 221)]
    ]

    for i in range(len(ks)):
        for n in ns[i]:
            Ss = {}

            for a in As[i]:
                S = 0

                for _ in range(T):
                    formula = generate_formula(n, int(a * n), ks[i])

                    if pycosat.solve(formula) != "UNSAT":
                        S += 1

                Ss[a] = S / T

            with open(f"results/results_k{ks[i]}_n{n}", "w") as f:
                for a in As[i]:
                    f.write(f"{a:.2f} {Ss[a]}\n")

        # wyświetlenie rezultatów na wykresie
        names = [f"results/results_k{ks[i]}_n{n}" for n in ns[i]]
        plot(names, ns[i], ks[i])
                    