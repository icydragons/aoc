import math
import re
import numpy as np
from functools import cache
from enum import Enum

class Part:
  def __init__(self, x1, x2, m1, m2, a1, a2, s1, s2):
    self.x = range(x1,x2+1)
    self.m = range(m1,m2+1)
    self.a = range(a1,a2+1)
    self.s = range(s1,s2+1)

  def __repr__(self):
    return f'x={self.x[0],self.x[-1]}, m={self.m[0],self.m[-1]}, a={self.a[0],self.a[-1]}, s={self.s[0],self.s[-1]}'

  def count(self):
    return len(self.x) * len(self.m) * len(self.a) * len(self.s)

def newPart(part):
  return Part(part.x[0], part.x[-1], part.m[0], part.m[-1], part.a[0], part.a[-1], part.s[0], part.s[-1])


def split(work, part):
  char = work[0]
  comparison = work[1]
  val = int(work[2:])
  partA = newPart(part)
  partB = newPart(part)
  index = getattr(part, char).index(val) 
  if comparison == '<':
     setattr(partA, char, getattr(partA, char)[:index])
     setattr(partB, char, getattr(partB, char)[index:])
     return partA, partB
  else:
     setattr(partA, char, getattr(partA, char)[index+1:])
     setattr(partB, char, getattr(partB, char)[:index+1])
     return partA, partB


def countAccept(part, workflows, id):
  workflow = workflows[id]
  sum = 0
  for work in workflow:
    if ':' in work:
      comp, inst = work.split(':')
      partA, partB = split(comp, part)
      print(f'Split {part} with {comp} into {partA} and {partB}')
      if inst == 'A':
        sum += partA.count()
      elif inst != 'R':
        sum += countAccept(partA, workflows, inst)
      part = partB
    elif work == 'A':
       sum += part.count()
    elif work != 'R':
       sum += countAccept(part, workflows, work)
  return sum
       

def main():
  workflows = {}
  with open("day19.txt") as f:
    for line in f:
      if len(line) > 5:
        l = [x.strip() for x in line.strip().split("{")]
        id = l[0]
        instruction = l[1][:-1].split(',')
        workflows[id] = instruction    
      else:
        break
    

  end = countAccept(Part(1,4000,1,4000,1,4000,1,4000), workflows, 'in')
  print(end)


if __name__ == "__main__":
    main()