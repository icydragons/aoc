import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
import pprint

class Brick():
  def __init__(self, end1, end2, id):
    self.end1 = [int(x) for x in end1.split(',')]
    self.end2 = [int(x) for x in end2.split(',')]
    self.id = id
    self.drop = False
  
  def __repr__(self):
    return f'B{self.id}'

  def populateMap(self, map):
    for x in range(self.end1[0], self.end2[0] + 1):
      for y in range(self.end1[1], self.end2[1] + 1):
        for z in range(self.end1[2], self.end2[2] + 1):
          map[x][y][z] = self.id
  
  def resetMap(self, map):
    for x in range(self.end1[0],self.end2[0] + 1):
      for y in range(self.end1[1],self.end2[1] + 1):
        for z in range(self.end1[2],self.end2[2] + 1):
          map[x][y][z] = 0
  
  def doDrop(self, map):
    if self.drop:
      return
    self.drop = True
    bottom = min(self.end1[2],self.end2[2])
    below = bottom - 1
    while below != 0:
      empty = True
      for x in range(self.end1[0], self.end2[0] + 1):
        for y in range(self.end1[1],self.end2[1] + 1):
          if map[x][y][below]:
            empty = False
            break
      if not empty:
        break
      below -= 1
    # would be one lower by the end
    below += 1
    if bottom != below:
      drop = bottom - below
      print(f'Dropping brick {self.id} by {drop}')
      self.resetMap(map)
      self.end1[2] = self.end1[2] - drop
      self.end2[2] = self.end2[2] - drop
      self.populateMap(map)  

  def bricksAbove(self, map): 
    top = max(self.end1[2],self.end2[2])
    above = top + 1
    brickIds = set() 
    if above < len(map[0][0]):
      for x in range(self.end1[0], self.end2[0] + 1):
        for y in range(self.end1[1],self.end2[1] + 1):
          brick = map[x][y][above]
          if brick:
            brickIds.add(brick)
    return list(brickIds)


  def bricksBelow(self, map): 
    bottom = min(self.end1[2],self.end2[2])
    below = bottom - 1
    brickIds = set() 
    if below > 0:
      for x in range(self.end1[0], self.end2[0] + 1):
        for y in range(self.end1[1],self.end2[1] + 1):
          brick = map[x][y][below]
          if brick:
            brickIds.add(brick)
    return list(brickIds)



def run(filename):
  bricks = {}
  with open(filename) as f:
    num = 1
    for line in f:
      end1,end2 = [x for x in line.strip().split("~")]
      bricks[num] = Brick(end1, end2, num)
      num += 1
  
  bigx = 0
  bigy = 0
  bigz = 0
  for brick in bricks.values():
    bigx = max(bigx, brick.end1[0], brick.end2[0])
    bigy = max(bigy, brick.end1[1], brick.end2[1])
    bigz = max(bigz, brick.end1[2], brick.end2[2])

  bigx += 1
  bigy += 1
  bigz += 1
  print(bigx, bigy, bigz)
  map = np.zeros([bigx, bigy, bigz], dtype=int)
  print(map)
  for brick in bricks.values():
    brick.populateMap(map)
  
  print(map)
  
  # Drop all the bricks
  for z in range(bigz):
    for y in range(bigy):
      for x in range(bigx):
        id = map[x][y][z]
        if id != 0:
          bricks[id].doDrop(map)
  
  # Part1
  removable = []
  for brick in bricks.values():
    safe = True
    above = brick.bricksAbove(map)
    for aboveId in above:
      aboveBrick = bricks[aboveId]
      if len(aboveBrick.bricksBelow(map)) == 1:
        safe = False
    if safe:
      print(f'Safe to remove {brick}')
      removable.append(brick)
  print(len(removable))
  
  # Part2
  sum = 0
  for brick in bricks.values():
    toFall = set()
    above = brick.bricksAbove(map)
    while len(above) > 0:
      aboveId = above.pop(0)
      if aboveId in toFall:
        continue
      aboveBrick = bricks[aboveId]
      bricksBelow = aboveBrick.bricksBelow(map)
      if all(x in toFall or x == brick.id for x in bricksBelow):
        toFall.add(aboveId)
        above.extend(aboveBrick.bricksAbove(map))
    print(f'Removing {brick} causes {len(toFall)} to fall')
    sum += len(toFall)
        

  print(sum) 
  
def main():
  run("day22.txt")


if __name__ == "__main__":
    main()