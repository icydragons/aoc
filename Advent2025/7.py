import math
import re

def propegate(s, input, val, i):
   if val == '^' and input > 0:
      s[i-1], s[i], s[i+1] = input + s[i-1], 0, input + s[i+1]
      return 1
   return 0
   

def main():
  grid = []
  with open("Advent2025/7.txt") as f:
    for line in f:
       grid.append([x for x in line.strip()])
    
    s = [0] * len(grid[0])
    s[grid[0].index('S')] = 1
    splits = 0
    for row in grid[1:]:
       print(s)
       sOld = s
       hits = list(map(lambda v,i: propegate(s, sOld[i], v, i), row, range(len(row))))
       splits += sum(hits)

    print(f'solution to 1: {splits}')
    print(f'solution to 2: {sum(s)}')

    return 0
                


if __name__ == "__main__":
    main()