import math
import re
import numpy as np
from functools import cache
from enum import Enum

index = {
  'x': 0,
  'm': 1,
  'a': 2,
  's': 3
}

def test(part, work):
  char = work[0]
  comparison = work[1]
  val = int(work[2:])
  partVal = part[index[char]]
  if comparison == '<':
     return partVal < val
  else:
     return partVal > val


def handlePart(part, workflows, id):
  workflow = workflows[id]
  for work in workflow:
    if ':' in work:
      comp, inst = work.split(':')
      print(comp, inst)
      if test(part, comp):
         if inst in 'RA':
            return inst
         else:
            return handlePart(part, workflows, inst)
      else:
         continue
    if work in 'RA':
       return work
    else:
       return handlePart(part, workflows, work)
       

def main():
  workflows = {}
  parts = []
  with open("day19.txt") as f:
    for line in f:
      if len(line) > 5:
        l = [x.strip() for x in line.strip().split("{")]
        id = l[0]
        instruction = l[1][:-1].split(',')
        workflows[id] = instruction    
      else:
        break

    for line in f:
          part = line.strip()[1:-1].split(',')
          part = [int(x.split('=')[1]) for x in part]
          parts.append(part)
      
  
  print(workflows)
  print(parts)

  s = 0
  for part in parts:
    end = handlePart(part, workflows, 'in')
    val = sum(part)
    print(f'Handle part {part} got to {end} with {val}')
    if end == 'A':
       s += val

  print(s)


if __name__ == "__main__":
    main()