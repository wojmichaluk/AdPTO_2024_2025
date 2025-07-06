from dimacs import loadX3C
import pycosat
from graphs import x3cs


# budowanie formuły logicznej - realizacja redukcji
def build_formula(n, sets):
    formula = []

    for j in range(1, n+1):
        # wymuszenie wybrania zbioru
        clause = []
        
        for i, set in enumerate(sets):
            if j in set:
                clause.append(i+1)

        formula.append(clause)

        # zapewnienie, że żadne dwa zbiory zawierające 
        # ten sam element nie są wybrane jednocześnie
        clauses = []

        for k in range(len(clause)-1):
            for l in range(k+1, len(clause)):
                clauses.append([])
                clauses[-1].append(-clause[k])
                clauses[-1].append(-clause[l])

        formula += clauses

    return formula


# główna część programu
if __name__ == "__main__":
    # spełnialność formuł po redukcji
    satisfiable = [
        False, True, False, True, False, False, True, 
        False, True, False, True, False, True
    ]

    for i, x3c in enumerate(x3cs):
        n, sets = loadX3C(f"x3c/{x3c}")
        formula = build_formula(n, sets)
        result = pycosat.solve(formula) != "UNSAT"

        # sprawdzenie poprawności redukcji
        assert result == satisfiable[i]
        print(f"Test {i+1}: {x3c} passed!")
