from dimacs import loadCNF
from sat2cnf import sat2cnf
import sats as s


def solve(CNF, V, rec):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych

    newV = V.copy()
    newCNF = unitPropagate(CNF, newV, rec)

    if onlyTwoVariablesClauses(newCNF):
        return sat2cnf(newCNF, newV)

    newCNF = fixConst(newCNF, newV)

    if newCNF == []:
        return newV
    elif newCNF is None:
        return "UNSAT"

    v = chooseMaxOccurencesVariable(newCNF)

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


def chooseMaxOccurencesVariable(CNF):
    occurences = dict()

    for C in CNF:
        for v in C:
            v = abs(v)

            if v in occurences:
                occurences[v] += 1
            else:
                occurences[v] = 1

    maxV = 0
    maxOccurences = 0

    for v in occurences:
        if occurences[v] > maxOccurences:
            maxV = v
            maxOccurences = occurences[v]

    return maxV


def onlyTwoVariablesClauses(CNF):
    if CNF is None or CNF == []:
        return False

    for C in CNF:
        if len(C) != 2:
            return False
        
    return True


# główna część programu
if __name__ == "__main__":
    # wszystkie instancje testowe
    sats = s.sats

    # spełnialność formuł
    satisfiable = [
        False, True, False, True, False, True, False, True, False, True, False, True,
        False, True, False, True, False, True, False, True, False, True, False, True,
        True, True, False, # dotąd znane są prawidłowe wartościowania
        False, False, False, False, False, False # tutaj nie są znane
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
