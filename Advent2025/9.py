import enum
from functools import lru_cache
import time

class DIR(enum.Enum):
   LESS = 'l'
   MORE =  'm'
   HORIZ = 'h'
   VERT = 'v'


class Line():
   def __init__(self, fixed, a, b, dir):
      self.fixed = fixed
      self.start = min(a, b)
      self.end = max(a, b)
      self.dir = dir
  
   def crossVal(self, val):
      return self.start <= val and self.end >= val
   
   def __repr__(self):
      return f'({self.fixed}: {self.start} -> {self.end} {self.dir})'
   


def area(a, b):
   return (abs(a[0]-b[0]) + 1) * (abs(a[1]-b[1]) + 1)

def checkCrossings(cols, rows, a, b):
   # print(f'CHECKING from {a} to {b}')
   ax,bx = a[0],b[0]
   ay,by = a[1],b[1]
   return (checkCrossing(cols, Line(ay, ax, bx, DIR.HORIZ)) 
           and checkCrossing(cols, Line(by, ax, bx, DIR.HORIZ)) 
           and checkCrossing(rows, Line(ax, ay, by, DIR.VERT)) 
           and checkCrossing(rows, Line(bx, ay, by, DIR.VERT)))

@lru_cache(maxsize=None)
def computeRanges(lines, fixed):
  insideLoop = False
  dir = None
  insideRange = []
  start = 0
  #print(lines)
  for line in lines:
      if (line.crossVal(fixed)):
        # print(f'crossing line {line} at {fixed}')
        if not start:
            start = line.fixed
        if line.start == fixed or line.end == fixed:
            newDir = DIR.MORE if line.start == fixed else DIR.LESS
            if dir == None:
              dir = newDir
            elif dir != newDir:
              dir = None
              insideLoop = not insideLoop
              if not insideLoop: 
                  insideRange.append((start, line.fixed))
                  start = 0
            elif dir == newDir:
              dir = None
              if not insideLoop:
                # print(f'not inside {dir}, {start}, {line.fixed}')
                insideRange.append((start, line.fixed))
                start = 0
        else:
            insideLoop = not insideLoop
            if not insideLoop: 
              insideRange.append((start, line.fixed))
              start = 0
  ranges = tuple(insideRange)
  # print(ranges)
                                  
     
  return ranges
   
      
def checkCrossing(lines, target):
      # print(f'Checking target {target}')
      # ray trace at the line from the edge
      insideRange = computeRanges(lines, target.fixed)

      # print(f'ranges: {insideRange}')
      for range in insideRange:
         if target.start >= range[0]:
              return target.end <= range[1]

      return False     
               
         
   
def main():
  
  before = time.perf_counter_ns()
  reds = []
  with open(f"Advent2025/9.txt") as f:
    for line in f:
       x,y = line.strip().split(',')
       reds.append([int(x), int(y)])

    m =  0
    for i1 in range(len(reds)):
       for i2 in range(i1+1, len(reds)):
         a = area(reds[i1], reds[i2])
         m = max(a, m)
        
    elapsed = time.perf_counter_ns() - before
    print(f'Solution to 1: {m} in ({elapsed//1_000_000} ms)')
    
    cols = []
    rows = []
    for i in range(0, len(reds)):
       ax,ay = reds[i-1] if i != 0 else reds[len(reds) - 1]
       bx,by = reds[i]
       if (ax == bx):
          cols.append(Line(ax, ay, by, DIR.VERT)) 
       else:
          rows.append(Line(ay, ax, bx, DIR.HORIZ)) 
   
    rows.sort(key=lambda r: r.fixed)
    cols.sort(key=lambda r: r.fixed)
    rows = tuple(rows)
    cols = tuple(cols)

    m =  0
    for i1 in range(len(reds)):
       for i2 in range(i1+1, len(reds)):
         a,b = reds[i1],reds[i2]
         size = area(a, b)
         if size < m:
            continue
         if checkCrossings(cols, rows, a, b):
           m = max(size, m)
        
    elapsed = time.perf_counter_ns() - before
    print(f'Solution to 1: {m} in ({elapsed//1_000_000} ms)')
    # 4660195710 is too high, 1393287318 is too low
                
    return 0
                


if __name__ == "__main__":
    main()