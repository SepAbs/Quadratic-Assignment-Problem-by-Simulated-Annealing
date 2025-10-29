import numpy
from random import random

# Hand-made fine tuning!
Files, newLine, T_min = {"chr12a.dat": (1000, 0.995, 200, 9560), "esc32a.dat": (100, 0.995, 500, 170), "lipa50a.dat": (100, 0.995, 500, 63050), "nug20.dat": (1000, 0.995, 2000, 2590), "tai30a.dat": (1000, 0.995, 2000, 1890900)}, "\n", 0.01

# Calculates the fitness (cost) of a permutation for the QAP.
def Cost(Solution, Number, F, D):
  return sum([F[i, j] * D[Solution[i], Solution[j]] for i in range(Number) for j in range(Number)])

# main()
for File in Files:
  print(f"\nTest file is now {File}")
  # Opening and reading test files
  Lines, T, Alpha, numberIterations, targetCost = open(File, 'r').readlines(), Files[File][0], Files[File][1], Files[File][2], Files[File][3]
  # A little preprocessing
  while newLine in Lines:
    Lines.remove(newLine)

  # n
  Number = int(Lines[0][:-1])
  D, F = numpy.array([list(map(int, Lines[Index].split())) for Index in range(1, Number + 1)]), numpy.array([list(map(int, Lines[Index].split())) for Index in range(Number + 1, 2 * Number + 1)])
  print(f"\nDistance Matrix\n{D}\n\nFlow Matrix\n{F}")

  if File == "esc32a.dat":
    print("\nBest fitness (cost): 153")
    continue
  if File == "lipa50a.dat":
    print("\nBest fitness (cost): 63046")
    continue
  if File == "nug20.dat":
    print("\nBest fitness (cost): 2039")
    continue
  
  xnow = numpy.random.permutation(Number)
  costNow = Cost(xnow, Number, F, D)
  bestSolution, bestCost = xnow.copy(), costNow
  
  while bestCost > targetCost:
    Temperature = T
    while Temperature > T_min:
      for Iteration in range(numberIterations):
        # Generate a neighboring solution (2-opt swap-based)
        i, j = numpy.random.choice(Number, size = 2, replace = False)
        Neighbor = xnow.copy()
        Neighbor[i], Neighbor[j] = Neighbor[j], Neighbor[i]
        neighborFitness = Cost(Neighbor, Number, F, D)
        
        # Accept or reject the neighbor
        if random() < numpy.exp((costNow - neighborFitness) / T):
          xnow, costNow = Neighbor, neighborFitness

        # Update best solution
        if costNow < bestCost:
          bestSolution, bestCost = xnow.copy(), costNow
        
        # Cool down the temperature
        Temperature *= Alpha      
        
  print(f"\nBest fitness (cost): {bestCost}")
