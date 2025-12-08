import heapq
import math
import re
import time

import sortedcontainers

class Junction():
   def __init__(self, id, x, y, z):
      self.id = id
      self.x = int(x)
      self.y = int(y)
      self.z = int(z)

   def __repr__(self):
      return f'({self.x}, {self.y}, {self.z})'
   
   def distance(self, o):
      return (self.x-o.x)**2 + (self.y - o.y)**2 + (self.z - o.z)**2
   

def addCircuit(circuits, distance):
   a,b = distance[0],distance[1]
   aCircuit = next((x for x in circuits if a.id in x), None)
   bCircuit = next((x for x in circuits if b.id in x), None)
   if not aCircuit and not bCircuit:
      circuits.append([a.id, b.id])
   elif aCircuit and bCircuit:
      if aCircuit != bCircuit:
         circuits.remove(aCircuit)
         bCircuit.extend(aCircuit) 
   elif not aCircuit:
      bCircuit.append(a.id) 
   elif not bCircuit:
      aCircuit.append(b.id)
   
def run(file, times): 
  
  before = time.perf_counter_ns()
  boxes = []
  with open(f"Advent2025/{file}") as f:
    i = 0
    for line in f:
       x,y,z = line.strip().split(',')
       boxes.append(Junction(i, x, y, z))
       i+=1
    elapsed = time.perf_counter_ns() - before
    print(f'Parsing done in ({elapsed//1_000_000} ms)')

    distances = []
    for i1 in range(len(boxes)):
       for i2 in range(i1+1, len(boxes)):
         d = boxes[i1].distance(boxes[i2])   
         heapq.heappush(distances, (d, [boxes[i1], boxes[i2]]))
    
    
    elapsed = time.perf_counter_ns() - before
    print(f'Distances done in ({elapsed//1_000_000} ms)')

    # Part 1
    circuits = []
    if times:
      for i in range(times):
        addCircuit(circuits, heapq.heappop(distances)[1])

      circuits.sort(key=lambda r: -len(r))
      s = 1
      for i in range(3):
        s *= len(circuits[i])
        
      elapsed = time.perf_counter_ns() - before
      print(f'Solution to 1: {s} in ({elapsed//1_000_000} ms)')
      

      # Part 2 - keep going
      while len(circuits[0]) < len(boxes):
        d = heapq.heappop(distances)
        addCircuit(circuits, d[1])
      
      elapsed = time.perf_counter_ns() - before
      print(f'Solution to 2: {d[1][0].x * d[1][1].x} in ({elapsed//1_000_000} ms)')
     


def main():
    run('example.txt', 10)
    run('8.txt', 1000)    

    return 0
                


if __name__ == "__main__":
    main()