## Laboratorium 6

- katalog _graph_ zawiera grafy do laboratorium zapisane w formacie DIMACS ASCII
- katalogi *vc_red_cbc* oraz *vc_red_glpk* zawierają podkatalogi (z plikami **.sol** o nazwach odpowiadających grafom, z obliczonymi rozwiązaniami) dla odpowiednio używanych solwerów CBC oraz GLPK oraz różnych konfiguracji z zadania 2. w ramach laboratorium
- katalog _coloring_ zawiera instancje grafów (pliki **.col**) do zadania 3. w ramach laboratorium
- katalog _colors_ zawiera pliki **.sol** z obliczonymi rozwiązaniami dla problemu kolorowania grafów
- plik **dimacs.py** to plik dołączony do laboratorium, zawierający funkcje do operowania na grafach w używanym formacie
- plik **grademe2.py** to plik pomocniczy, służy do sprawdzania poprawności rozwiązań
- plik **graphs.py** zawiera listę nazw plików z grafami
- plik **pulp_tutorial.py** zawiera podstawowe operacje z wykorzystaniem biblioteki PULP, w ramach zadania 1. z laboratorium
- pliki **sol1.py**, **sol2.py** oraz **sol3.py** to pliki z rozwiązaniami kolejnych zadań
- plik **lab6.pdf** zawiera treść laboratorium

### Uwagi
- patrz _post scriptum_ w pliku **sol3.py**
- solwer GLPK należy zainstalować lokalnie i wskazać ścieżkę właściwą dla swojego przypadku. Powinna być też opcja użycia przez PULP, ale u mnie nie działała
