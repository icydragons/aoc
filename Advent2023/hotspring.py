import math
import re

class Puz:
  def __init__(self, springs, checks):
    self.springs = springs
    self.checks = checks

  def __repr__(self):
    return f"springs are {self.springs} and {self.checks}"
  
  def broke(self):
    check = 0
    contig = 0
    error = False
    uncertain = '?' in self.springs
    if uncertain:
      return False
    for i in range(len(self.springs)):
      char = self.springs[i]
      if char == '.':
        if error:
          return True
        contig = 0
        continue

      if char == '#':
        error = True  
      contig += 1
      if contig == self.checks[check]:
        check += 1
        i += 1
        if i < len(self.springs) and self.springs[i] == '#' and not uncertain:
          return True
        contig = 0
        error = False
      
      if check == len(self.checks):
        for j in range(i, len(self.springs)):
          char = self.springs[j]
          # Too many errors
          if char == '#' and not uncertain:
            return True
        #print(f'found a potential solution {self}')
        return False 
    return True
     
  
def countSol(puzzle):
  if puzzle.broke():
    return 0
  
  if '?' not in puzzle.springs:
    print(f'found solution {puzzle}')
    return 1
  
  count = 0
  s = puzzle.springs
  i = s.index('?')
  count += countSol(Puz('%s%s%s'%(s[:i],'#',s[i+1:]), puzzle.checks))
  count += countSol(Puz('%s%s%s'%(s[:i],'.',s[i+1:]), puzzle.checks))
  return count


def main():
  puzzles = [] 
  with open("hotspring.txt") as f:
    for line in f:
      l = line.strip().split(" ")
      print(l[1])
      springs = l[0]
      checks = l[1]
      puzzles.append(Puz(springs, [int(x) for x in checks.split(',')]))

  sols = 0
  for puzzle in puzzles:
    print(f'Solving {puzzle}')
    sol = countSol(puzzle)
    print(f'has {sol}')
    sols += sol

  # 7007
  print(f'totoal {sols}')  


if __name__ == "__main__":
    main()