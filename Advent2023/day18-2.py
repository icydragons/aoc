import math
import re
import numpy as np
from functools import cache
from enum import Enum

dirmap = {
  '0': 'R',
  '1': 'D',
  '2': 'L',
  '3': 'U'
}

class Instruction:
  def __init__(self, dir, len, color):
    dir = color[-2]
    self.dir = dirmap[dir]
    self.len = x = int(color[2:-2], 16)
    self.color = color

  def __repr__(self):
    #return f"dir is {self.dir} for {self.len} in {self.color}"
    return '#'
  


def main():
  instructions = []
  size = 10000
  # grid = np.zeros([size, size], dtype = 'object')
  with open("day18.txt") as f:
    for line in f:
      l = [x.strip() for x in line.strip().split(" ")]
      instructions.append(Instruction(l[0], l[1], l[2]))
  
  i = 0
  j = 0
  vertices = []
  boundaryPoints = 1
  for instruction in instructions:
    dir = instruction.dir
    match dir:
      case 'R':
        j+=instruction.len
      case 'L':
        j-=instruction.len
      case 'U':
        i-=instruction.len
      case 'D':
        i+=instruction.len
    # grid[i][j] = instruction
    boundaryPoints +=instruction.len
    vertices.append([i, j])
  
  # print(grid)
  print(f'Len of {len(vertices)}')
  area = 0
  for i in range(len(vertices)):
    next = (i + 1) % len(vertices)
    vertex = vertices[i]
    nextV = vertices[next]
    area += vertex[0] * nextV[1] - vertex[1] * nextV[0]
  
  area = abs(area) / 2

  print(f'the area is {area}, the boundary is {boundaryPoints} and ' \
        f'{area + boundaryPoints / 2 + 1}')

      


    


if __name__ == "__main__":
    main()