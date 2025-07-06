from dimacs import loadCNF
import sats as s


def solve(CNF, V, rec):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych

    newV = V.copy()
    newCNF = unitPropagate(CNF, newV, rec)
    newCNF = fixConst(newCNF, newV)

    if newCNF == []:
        return newV
    elif newCNF is None:
        return "UNSAT"

    v = abs(newCNF[0][0])

    newV[v] = 1
    newV[-v] = -1
    rec[0] += 1

    sol = solve(newCNF, newV, rec) 
    if sol != "UNSAT": return sol

    newV[v] = -1
    newV[-v] = 1
    rec[0] += 1

    return solve(newCNF, newV, rec) 


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


def unitPropagate(CNF, V, rec):
    newCNF = simplifyCNF(CNF, V)
    if newCNF is None:
        return

    for C in newCNF:
        if len(C) == 1:
            L = C[0]

            if V.get(L) == -1:
                return

            V[L] = 1
            V[-L] = -1

            rec[1] += 1
            return unitPropagate(newCNF, V, rec)

    return newCNF


def fixConst(CNF, V):
    if CNF is None:
        return

    checked = dict()

    for C in CNF:
        for v in C:
            if v not in checked:
                checked[v] = 1
                checked[-v] = 0
            else:
                checked[v] += 1

    for v in checked:
        if checked[v] == 0:
            V[v] = -1
            V[-v] = 1

    newCNF = simplifyCNF(CNF, V)
    return newCNF


# główna część programu
if __name__ == "__main__":
    # podzbiór instancji testowych
    sats = s.sats[:26]

    # spełnialność formuł
    satisfiable = [
        False, True, False, True, False, True, False, True, False, True, False, True,
        False, True, False, True, False, True, False, True, False, True, False, True,
        True, True
    ]

    for i, sat in enumerate(sats):
        _, CNF = loadCNF(f"sat/{sat}")
        rec = [0, 0]
        result = solve(CNF, dict(), rec) != "UNSAT"
        print(f"Recursive `solve` calls: {rec[0]}")
        print(f"Recursive `unitPropagate` calls: {rec[1]}")

        # sprawdzenie poprawności działania solwera
        assert result == satisfiable[i]
        print(f"Test {i+1}: {sat} passed!\n")
