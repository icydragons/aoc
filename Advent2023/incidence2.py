import math
import re
import numpy as np


def findSymetry(grid, smudge, colToInclude):
    best = 0
    low = 1
    high = len(grid[0])
    for j in range(1, len(grid[0])):
      if smudge:
        print(f'{colToInclude} and {j}')
        if colToInclude - j not in range(min(j, len(grid[0]) - j)):
          continue
      mirror = True
      for i in range(len(grid)):
        row = grid[i]
        for k in range(min(j, len(grid[0]) - j)):
          val = row[j+k]
          sym = row[j-k-1]
          if val != sym:
            mirror = False
            if not smudge:
              # print(f'Testing for smudge at {i},{j}')
              newGrid = grid.copy()
              newGrid[i][j+k] = sym
              best = findSymetry(newGrid, True, j+k)
              if best:
                print(f'Found symetry {best} with {i},{j+k} smudge in \n{newGrid}')
                return best
            break
        if not mirror:
          break
      if mirror and smudge:
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
    sym = findSymetry(grid, False, 0)
    if not sym:
      print(f'looking in T \n{gridT}')
      sym = findSymetry(gridT, False, 0) * 100
    print(f'Found symmetry {sym} in \n{grid[0]}')
    if sym == 0:
      break
    sum += sym
  print(sum)



        
      
                


if __name__ == "__main__":
    main()