from pulp import *


def linear_problem(category):
    # stworzenie modelu problemu
    model = LpProblem("min_integer", LpMinimize)

    # stworzenie zmiennych
    x = LpVariable("x", cat=category) 
    y = LpVariable("y", cat=category)

    # dodanie funkcji celu do modelu
    model += x + y    

    # dodanie ograniczeń
    model += y >= x - 1
    model += y >= -4 * x + 4
    model += y <= -0.5 * x + 3

    # rozwiązanie z wykorzystaniem solwera CBC
    model.solve()

    # wypisanie statusu rozwiązania
    print(f"Status rozwiązania: {LpStatus[model.status]}")

    # wypisanie zmiennych
    print("Wartości zmiennych:")
    for var in model.variables():
        print(var.name, "=", var.varValue)

    # wypisanie wartości funkcji celu
    print(f"Wartość funkcji celu: {value(model.objective)}")


if __name__ == "__main__":
    print("Problem w liczbach całkowitych")
    linear_problem("Integer")
    print()
    print("Problem w liczbach rzeczywistych")
    linear_problem("Continuous")
