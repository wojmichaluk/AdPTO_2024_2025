# implementacja własnego solwera - kombinacja mechanizmów dających 
# najlepsze rozwiązanie z poprzedniego laboratorium (nr 4)
# -----------------------------------------------

from math import inf


def solve(CNF, V=dict()):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych

    newV = V.copy()
    newCNF = unitPropagate(CNF, newV)
    newCNF = fixConst(newCNF, newV)

    if newCNF == []:
        return newV
    elif newCNF is None:
        return "UNSAT"

    v = chooseMinOccurencesVariable(newCNF)

    newV[v] = 1
    newV[-v] = -1

    sol = solve(newCNF, newV)
    if sol != "UNSAT":
        return sol

    newV[v] = -1
    newV[-v] = 1

    return solve(newCNF, newV)


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


def unitPropagate(CNF, V):
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

            return unitPropagate(newCNF, V)

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


def chooseMinOccurencesVariable(CNF):
    occurences = dict()

    for C in CNF:
        for v in C:
            v = abs(v)

            if v in occurences:
                occurences[v] += 1
            else:
                occurences[v] = 1

    minV = 0
    minOccurences = inf

    for v in occurences:
        if occurences[v] < minOccurences:
            minV = v
            minOccurences = occurences[v]

    return minV
