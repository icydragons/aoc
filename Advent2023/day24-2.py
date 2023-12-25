import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
from typing import NamedTuple
import pprint


class Hailstone(NamedTuple):
  id: int
  px: int
  py: int
  pz: int
  vx: int
  vy: int
  vz: int

  def atTime(self, t):
    return tuple([self[i] + t * self[i+3] for i in [1,2,3]])

  def closest(self, other):
    # Dirivate to find the max/min 
    a = self.vx - other.vx
    b = self.px - other.px
    c = self.vy - other.vy
    d = self.py - other.py
    e = self.vz - other.vz
    f = self.pz - other.pz
    denom = (a**2 + c**2 + e**2)
    if denom == 0:
      return None
    time = (-a*b-c*d-e*f) / denom
    return time, self.distanceBetween(other, time)


  def distanceBetween(self, other, t):
    a = self.atTime(t)
    b = other.atTime(t)
    dist = [(a[i] - b[i])**2 for i in [1,2]]
    return math.sqrt(sum(dist))
  
  
  def collide(self, other):
    # print(f'Test collide {self} and {other}')
    cx = self.px - other.px
    cy = self.py - other.py
    # t*vx - t*ovx + cx = 0
    # t*vy - t*ovy + cy = 0
    # t = (opx - px)/(vx - ovx)
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

def makeCycle(hailstones, start):
  nearest = []
  visited = {}
  queue = [start]
  while len(queue):
    hailstone = queue.pop(0)
    closest = None
    distance = 10000000000000000
    visited[hailstone.id]= hailstone
    for other in hailstones:
      if other.id in visited.keys():
        continue
      t,d = hailstone.closest(other)
      # print(hailstone, other)
      distance = min(d, distance)
      if distance == d:
        closest = (hailstone, other, t, d)
    if closest:
      nearest.append(closest)
      queue.append(closest[1])
  return nearest

def solveEquations(hailstones):
  first = hailstones[0]
  second = hailstones[1]
  third = hailstones[2]

  # same position (x) and (t) (let f,s,t be first second third and none be magic one)
  # x = t*vx + px
  # x = t*fvx + fpx
  # t*(vx - fvx) = (fpx - px)
  # t = (fpx - px) / (vx - fvx) 
  # same t for x, y and z gives
  # (fpx - px) / (vx - fvx) = (fpy - py) / (vy - fvy) = (fpz - pz) / (vz - fvz)
  # Multiplying:
  # (fpx - px) * (vy - fvy) = (fpy - py) * (vx - fvx)
  # fpx*vy -px * vy - fpx*fvy + px * fvy = fpy * vx - fpy * fvx - py * vx + py * fvx
  # Now using s:
  # spx*vy -px * vy - spx*svy + px * svy = spy * vx - spy * svx - py * vx + py * svx
  # Now subtract upwards ^
  # (spx - fpx)*vy - (spx*svy - fpx*fvy) + (svy - fvy) * px = (spy - fpy) * vx - (spy * svx - fpy * fvx) + (svx - fvx) * py
  # rearrange
  # (spy - fpy) * vx + (fpx - spx) * vy + 0*vz + (fvy - svy) * px + (svx - fvx) * py + 0*pz =
  #     (fpy * fvx - spy * svx) - (fpx * fvy - spx * svy) 
  # Now do it five more times to get....

  A = np.array(
      [
          [second.vy - first.vy, first.vx - second.vx, 0.0, first.py - second.py, second.px - first.px, 0.0],
          [third.vy - first.vy, first.vx - third.vx, 0.0, first.py - third.py, third.px - first.px, 0.0],
          [second.vz - first.vz, 0.0, first.vx - second.vx, first.pz - second.pz, 0.0, second.px - first.px],
          [third.vz - first.vz, 0.0, first.vx - third.vx, first.pz - third.pz, 0.0, third.px - first.px],
          [0.0, second.vz - first.vz, first.vy - second.vy, 0.0, first.pz - second.pz, second.py - first.py],
          [0.0, third.vz - first.vz, first.vy - third.vy, 0.0, first.pz - third.pz, third.py - first.py],
      ]
  )

  b = [
      (first.py * first.vx - second.py * second.vx) - (first.px * first.vy - second.px * second.vy),
      (first.py * first.vx - third.py * third.vx) - (first.px * first.vy - third.px * third.vy),
      (first.pz * first.vx - second.pz * second.vx) - (first.px * first.vz - second.px * second.vz),
      (first.pz * first.vx - third.pz * third.vx) - (first.px * first.vz - third.px * third.vz),
      (first.pz * first.vy - second.pz * second.vy) - (first.py * first.vz - second.py * second.vz),
      (first.pz * first.vy - third.pz * third.vy) - (first.py * first.vz - third.py * third.vz),
  ]

  sol = np.linalg.solve(A, b)
  print(sol)
  print("p2: ", round(sol[0] + sol[1] + sol[2]))


def run(filename):
  hailstones = []
  i = 0
  with open(filename) as f:
    for line in f:
      pos, vel = line.strip().split('@')
      pos = pos.strip().split(', ')
      vel = vel.strip().split(', ')
      hailstones.append(Hailstone(i, int(pos[0]),int(pos[1]),int(pos[2]),
                                  int(vel[0]),int(vel[1]),int(vel[2])))
      i += 1
  
  # Make a cycle of hailstones based on which ones are close
  nearest = makeCycle(hailstones, hailstones[0])
  
  # find the largest negatives (they would collide off screen a long ways 
  # and start with one of them)
  nearest.sort(key=lambda x: x[2])
  nearest = makeCycle(hailstones, nearest[0][0])
  solveEquations(hailstones)
  
  
def main():
  run("day24-e.txt")
  run("day24.txt")


if __name__ == "__main__":
    main()