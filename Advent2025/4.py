import copy
import math
import re

def countPaper(grid, row, col):
  paper = 0
  for i in row-1, row, row + 1:
    for j in col - 1, col, col + 1:
      if i == row and col == j:
        continue
      paper += hasPaper(grid, i, j)
  return paper

def hasPaper(grid, row, col):
  if len(grid) > row and row >= 0:
    if (len(grid[row]) > col and col >= 0):
      return grid[row][col] in ('@','x')
  return 0

def runSim(grid, keep):
  s = 0
  for row in range(len(grid)):
      for col in range(len(grid[row])):
        if not grid[row][col] in ('@','x'):
          continue
        paper = countPaper(grid, row, col)
        if paper < 4:
          s+=1
          grid[row][col] = 'x' if keep else '.'

  return s
  

def main():
  grid = []
  with open("Advent2025/4.txt") as f:
    for line in f:
      grid.append([x for x in line.strip()])

    s = runSim(copy.deepcopy(grid), True)
    print(f'Part 1: {s}')

    s = 0
    olds = -1
    grid2 = copy.deepcopy(grid)
    while s != olds:
      olds = s
      s += runSim(grid2, False)  
    print(f'Part 2: {s}')

    return 0
                


if __name__ == "__main__":
    main()