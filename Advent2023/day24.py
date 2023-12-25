import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
from typing import NamedTuple
import pprint


class Hailstone(NamedTuple):
  px: int
  py: int
  pz: int
  vx: int
  vy: int
  vz: int

  def collide(self, other):
    # print(f'Test collide {self} and {other}')
    cx = self.px - other.px
    cy = self.py - other.py
    # t*vx - ot*ovx + cx = 0
    # t*vy - ot*ovy + cy = 0
    t1d = (-self.vx*other.vy + other.vx*self.vy)
    t2d = (-self.vx*other.vy + other.vx*self.vy)
    if t1d == 0 or t2d == 0:
      return 0,0,0
    t1 = (-other.vx*cy + other.vy*cx) / t1d
    t2 = (cx*self.vy - cy*self.vx) / t2d
    if t1 < 0 or t2 < 0:
      # print('Would collide in the past')
      return 0,0,0
    return (t1*self.vx + self.px),(t1*self.vy + self.py),0


def run(filename, low, high):
  hailstones = []
  with open(filename) as f:
    for line in f:
      pos, vel = line.strip().split('@')
      pos = pos.strip().split(', ')
      vel = vel.strip().split(', ')
      hailstones.append(Hailstone(int(pos[0]),int(pos[1]),int(pos[2]),
                                  int(vel[0]),int(vel[1]),int(vel[2])))

  collide = 0
  for i,hailstone in enumerate(hailstones):
    for j in range(i + 1, len(hailstones)):
      x,y,z = hailstone.collide(hailstones[j])
      # print(x, y, z)
      if low <= x <= high and low <= y <= high: 
        collide +=1
        # print((f'{hailstone} collides with {hailstones[j]} at {x},{y},{z}'))
  print(collide)
  
def main():
  run("day24-e.txt", 7, 24)
  run("day24.txt", 200000000000000, 400000000000000)


if __name__ == "__main__":
    main()