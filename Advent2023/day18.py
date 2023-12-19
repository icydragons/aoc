import math
import re
import numpy as np
from functools import cache
from enum import Enum


class Instruction:
  def __init__(self, dir, len, color):
    self.dir = dir
    self.len = int(len)
    self.color = color

  def __repr__(self):
    #return f"dir is {self.dir} for {self.len} in {self.color}"
    return '#'
  


def main():
  instructions = []
  size = 1000
  grid = np.zeros([size, size], dtype = 'object')
  with open("day18-e.txt") as f:
    for line in f:
      l = [x.strip() for x in line.strip().split(" ")]
      instructions.append(Instruction(l[0], l[1], l[2]))
  
  i = 0
  j = 0
  vertices = []
  boundaryPoints = 1
  for instruction in instructions:
    dir = instruction.dir
    for d in range(instruction.len):
      match dir:
        case 'R':
          j+=1
        case 'L':
          j-=1
        case 'U':
          i-=1
        case 'D':
          i+=1
      grid[i][j] = instruction
      vertices.append([i, j])
      boundaryPoints +=1
  
  print(grid)
  
  area = 0
  for i in range(len(vertices)):
    next = (i + 1) % len(vertices)
    vertex = vertices[i]
    nextV = vertices[next]
    area += vertex[0] * nextV[1] - vertex[1] * nextV[0]
  
  area = abs(area) / 2

  print(f'the area is {area}, the boundary is {boundaryPoints} and ' \
        f'{area + boundaryPoints / 2 + 1}')
  
  # 1256 is too high

      


    


if __name__ == "__main__":
    main()