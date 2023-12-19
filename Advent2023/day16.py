import math
import re
import numpy as np
from functools import cache
from enum import Enum

class DIR(Enum):
   UP = 'up'
   DOWN =  'down'
   LEFT = 'left'
   RIGHT = 'right'


def goDir(grid, x, y, dir, lasers):
  match dir:
    case DIR.RIGHT:
      if y < len(grid[0]) - 1:
        lasers.append([x, y+1, DIR.RIGHT])
    case DIR.LEFT:
      if y > 0:
        lasers.append([x, y-1, DIR.LEFT])
    case DIR.UP:
      if x > 0:
        lasers.append([x -1, y, DIR.UP])
    case DIR.DOWN:
      if x < len(grid) - 1:
        lasers.append([x +1, y, DIR.DOWN])

def runGrid(initial, grid): 
  energizedGrid = np.empty([len(grid), len(grid[0])], dtype = 'object')
  lasers = [initial]
  visited = {}
  while len(lasers) > 0:
     laser = lasers.pop()
     id = "_".join([str(x) for x in laser])
     if id in visited.keys():
       continue
     visited[id] = True
     x = laser[0]
     y = laser[1]
     dir = laser[2]
     energizedGrid[x][y] = '#'
     char = grid[x][y]
     match dir:
        case DIR.RIGHT:
          if char in '.-':
            goDir(grid, x, y, DIR.RIGHT, lasers)
          if char == '/':
            goDir(grid, x, y, DIR.UP, lasers)
          if char == '\\':
            goDir(grid, x, y, DIR.DOWN, lasers)
          if char == '|':
            goDir(grid, x, y, DIR.UP, lasers)
            goDir(grid, x, y, DIR.DOWN, lasers)
        case DIR.LEFT:
          if char in '.-':
            goDir(grid, x, y, DIR.LEFT, lasers)
          if char == '/':
            goDir(grid, x, y, DIR.DOWN, lasers)
          if char == '\\':
            goDir(grid, x, y, DIR.UP, lasers)
          if char == '|':
            goDir(grid, x, y, DIR.UP, lasers)
            goDir(grid, x, y, DIR.DOWN, lasers)
        case DIR.UP:
          if char in '.|':
            goDir(grid, x, y, DIR.UP, lasers)
          if char == '/':
            goDir(grid, x, y, DIR.RIGHT, lasers)
          if char == '\\':
            goDir(grid, x, y, DIR.LEFT, lasers)
          if char == '-':
            goDir(grid, x, y, DIR.LEFT, lasers)
            goDir(grid, x, y, DIR.RIGHT, lasers)
        case DIR.DOWN:
          if char in '.|':
            goDir(grid, x, y, DIR.DOWN, lasers)
          if char == '/':
            goDir(grid, x, y, DIR.LEFT, lasers)
          if char == '\\':
            goDir(grid, x, y, DIR.RIGHT, lasers)
          if char == '-':
            goDir(grid, x, y, DIR.LEFT, lasers)
            goDir(grid, x, y, DIR.RIGHT, lasers)

  sum = 0
  for row in energizedGrid:
    for char in row:
      if char == '#':
        sum += 1

  print(f'When going in {initial} found {sum}')
  return sum


def main():
  grid = []
  with open("day16.txt") as f:
    for line in f:
      grid.append([x for x in line.strip()])

  sum = 0
  for i in range(len(grid)):    
    sum = max(sum, runGrid([i, 0, DIR.RIGHT], grid)) 
    sum = max(sum, runGrid([i, len(grid[0]) - 1, DIR.LEFT], grid)) 
  for j in range(len(grid[0])):    
    sum = max(sum, runGrid([len(grid) - 1,j,DIR.UP], grid)) 
    sum = max(sum, runGrid([0,j,DIR.DOWN], grid))    
 
  print(sum)
            


if __name__ == "__main__":
    main()
