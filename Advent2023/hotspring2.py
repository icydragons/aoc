import math
import re
from functools import cache

def possible_placements(condition, spring):
  for m in re.finditer(rf'(?=([^\.]{{{spring}}}[^#]))', condition):
    i = m.span(1)[0]
    if '#' in condition[:i]:
      break
    # print(f'original {condition} and {spring} test m is {m} i is {i} cond {condition}')
    yield condition[i + spring + 1:]

  
@cache
def countSol(condition, springs):
  if not springs:
    return '#' not in condition
  
  first, rest = springs[0], springs[1:]
  return sum(countSol(rest_condition, rest) for 
             rest_condition in possible_placements(condition, first))


def main():
  puzzles = [] 
  with open("hotspring.txt") as f:
    for line in f:
      l = line.strip().split(" ")
      print(l[1])
      springs = f'.{"?".join([l[0]]*5)}.'
      checks = ",".join([l[1]]*5)
      puzzles.append([springs, tuple([int(x) for x in checks.split(',')])])

  sols = 0
  for puzzle in puzzles:
    print(f'Solving {puzzle}')
    sol = countSol(puzzle[0], puzzle[1])
    print(f'has {sol}')
    sols += sol

  # 7007
  print(f'totoal {sols}')  


if __name__ == "__main__":
    main()