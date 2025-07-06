from pulp import *


# stwórz model problemu o nazwie test, minimalizacja funkcji celu
model = LpProblem( "test", LpMinimize)   # LpMaximize dla maksymalizowania funkcji celu

# stwórz trzy zmienne, x, y, z
x = LpVariable( "x" , lowBound = 0, upBound = 5, cat = "Continuous" ) # zmienna ciągła z przedzialu [0,5]
y = LpVariable( "y" , lowBound = 0, upBound = 3, cat = "Integer" )    # zmienna całkowita ze zbioru {0,1,2,3}
z = LpVariable( "z" , cat = "Binary" )                                # zmienna binarna, wartosci ze zbioru {0,1}

# dodaj funkcję celu do modelu
model += 5-x+2*y-z    

# dodaj ograniczenia (konieczne do spełnienia nierówności liniowe)
model += x >= y
model += y >= z

print( model )

model.solve()                      # rozwiąż używając CBC
print( LpStatus[model.status] )    # wypisz status rozwiązania

# wypisz zmienne
for var in model.variables():
  print( var.name, "=", var.varValue )

# wypisz wartość funkcji celu
print( value(model.objective) )

print( x.value() )

# aby solwer glpk działał, muszę go użyć w nieco inny sposób
# model.solve( GLPK() )
model.solve(pulp.GLPK_CMD(path="C:/glpk-4.65/w64/glpsol.exe", msg=False))

print()
print( LpStatus[model.status] )    # wypisz status rozwiązania

# wypisz zmienne
for var in model.variables():
  print( var.name, "=", var.varValue )

# wypisz wartość funkcji celu
print( value(model.objective) )

