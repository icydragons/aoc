import math
import re
import numpy as np


def findSymetry(grid):
    best = 0
    for j in range(1, len(grid[0])):
      mirror = True
      for i in range(len(grid)):
        row = grid[i]
        for k in range(min(j, len(grid[0]) - j)):
          val = row[j+k]
          sym = row[j-k-1]
          if val != sym:
            mirror = False
            break
        if not mirror:
          break
      if mirror:
        return j
    return best


def main():
  grids = []
  with open("incidence.txt") as f:
    grid = []
    for line in f:
      row = [x for x in line.strip()]
      if row:
        grid.append(row)
      else:
        grids.append(grid)
        grid = []
    grids.append(grid)

  sum = 0
  for x in range(len(grids)):
    grid = np.array(grids[x])
    gridT = np.transpose(grid)
    sym = findSymetry(grid)
    if not sym:
      print(f'looking in T \n{gridT}')
      sym = findSymetry(gridT) * 100
    print(f'Found symmetry {sym} in \n{grid}')
    sum += sym
  print(sum)



        
      
                


if __name__ == "__main__":
    main()