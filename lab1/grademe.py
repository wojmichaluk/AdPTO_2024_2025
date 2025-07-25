# APTO Piotr Faliszewski 2018
# Test solution for the VertexCover problem



# graph list
graphs = [
("e5"),
("e10"),
("e20"),
("e40"),
("e150"),
("s25"),
("s50"),
("s500"),
("b20"),
("b30"),
("b100"),
("k330_a"),
("k330_b"),
("k330_c"),
("m20"),
("m30"),
("m40"),
("m50"),
("m100"),
("p20"),
("p35"),
("p60"),
("p150"),
("r30_01"),
("r30_05"),
("r50_001"),
("r50_01"),
("r50_05"),
("r100_005"),
]





from dimacs import *
from sys    import *


def loadSolution( name ):
  f = open( name, "r" )
  s = f.readline().strip()
  C = s.split(',')
  C = [int(c) for c in C]
  return C


# tutaj zmieniłem w stosunku do oryginału
if( len(argv) != 2 ):
  print("Invocation:")
  print("  python grademe.py <solution directory>")
  print("")
  print("Looks for graphs in the directory:")
  print("  graph")
  print("Looks for solutions in the directory:")
  print("  <solution directory>")
  print("Solutions should have name:")
  print("  <name>.sol")
  exit()

sol_path = argv[1]


def checkGraph( sol_path, name ):
  s = name + "\t :  "
  size = 99999
  try:
    G = loadGraph( "graph/" + name )
    size = len(G)
    C = loadSolution( sol_path + "/" + name + ".sol" )
  except IOError:
    s += "--- (%d)" % size
    return (s,size,False)


  E = edgeList( G )
  if isVC( E, C ):
      s += "OK  (VC = %d)" % len(C)
      return (s,len(C),True)
  else:
    s += "FAIL! (99999)" 
    return (s,99999,False)



score = 0
total = 0
output = ""


for (name) in graphs:
  (s,size,ans) = checkGraph( sol_path, name )
  total += size
  if ans: 
    score += 1
  print(s)
  output += str(size) + ","

print("")
print("SOLVED = %d/%d" % (score, len(graphs) ))
print("TOTAL  = %d" % total ) 

print("")
print("=split(\"%d,%d,%s\",\",\")" % (score, total, output) )
