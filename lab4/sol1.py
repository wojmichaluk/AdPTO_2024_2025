from dimacs import loadCNF
import sats as s


def solve(CNF, V):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych

    newCNF = simplifyCNF(CNF, V)

    if newCNF == []:
        return V
    elif newCNF is None:
        return "UNSAT"

    v = abs(newCNF[0][0])

    V[v] = 1
    V[-v] = -1

    if solve(newCNF, V) != "UNSAT":
        return V

    V[v] = -1
    V[-v] = 1

    if solve(newCNF, V) != "UNSAT":
        return V

    del V[v]
    del V[-v]

    return "UNSAT"


def simplifyClause(C, V):
    # C - klauzula, czyli lista literałów
    # V - wartościowanie zmiennych

    newC = []

    for c in C:
        if V.get(c) == 1:
            return
        elif V.get(c) != -1:
            newC.append(c) 

    return newC


def simplifyCNF(CNF, V):
    # CNF - formuła do uproszczenia
    # V   - wartościowanie zmiennych

    newCNF = []

    for C in CNF:
        newC = simplifyClause(C, V)

        if newC == []:
            return
        elif newC is not None:
            newCNF.append(newC)

    return newCNF


# główna część programu
if __name__ == "__main__":
    # podzbiór instancji testowych
    sats = s.sats[:8]

    # spełnialność formuł
    satisfiable = [False, True, False, True, False, True, False, True]

    for i, sat in enumerate(sats):
        _, CNF = loadCNF(f"sat/{sat}")
        result = solve(CNF, dict()) != "UNSAT"

        # sprawdzenie poprawności działania solwera
        assert result == satisfiable[i]
        print(f"Test {i+1}: {sat} passed!\n")
