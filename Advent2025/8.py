import math
import re

def propegate(o, input, val, i):
   if val == '^' and input > 0:
      o[i-1], o[i], o[i+1] = input + o[i-1], 0, input + o[i+1]
      return 1
   return 0
   

def main():
  grid = []
  with open("Advent2025/7.txt") as f:
    for line in f:
       grid.append([x for x in line.strip()])
    
    o = [0] * len(grid[0])
    o[grid[0].index('S')] = 1
    splits = 0
    for row in grid[1:]:
       print(o)
       oOld = o
       hits = list(map(lambda v,i: propegate(o, oOld[i], v, i), row, range(len(row))))
       splits += sum(hits)

    print(f'solution to 1: {splits}')
    print(f'solution to 2: {sum(o)}')

    return 0
                


if __name__ == "__main__":
    main()