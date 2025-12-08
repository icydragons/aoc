import math
import re

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
   
class Distance():
   def __init__(self, d, a, b):
      self.d = d
      self.a = a
      self.b = b

   def __lt__(self, other):
        return self.d < other.d 
   
   def __repr__(self):
      return f'{self.d} -> {self.a}<->{self.b}'
   

def addDistance(distances, a, b):
   distance = Distance(a.distance(b), a, b)
   distances.add(distance)

def addCircuit(circuits, distance):
   a,b = distance.a,distance.b
   aCircuit = next((x for x in circuits if a.id in x), None)
   bCircuit = next((x for x in circuits if b.id in x), None)
   if not aCircuit and not bCircuit:
      circuits.append([a.id, b.id])
   elif aCircuit and bCircuit:
      if aCircuit != bCircuit:
         circuits.remove(aCircuit)
         circuits.remove(bCircuit)
         circuits.append(aCircuit + bCircuit) 
   elif not aCircuit:
      bCircuit.append(a.id) 
   elif not bCircuit:
      aCircuit.append(b.id)
   
def run(file, times): 
  boxes = []
  with open(f"Advent2025/{file}") as f:
    i = 0
    for line in f:
       x,y,z = line.strip().split(',')
       boxes.append(Junction(i, x, y, z))
       i+=1

    distances = sortedcontainers.SortedList()
    for i1 in range(len(boxes)):
       for i2 in range(i1+1, len(boxes)):
          addDistance(distances, boxes[i1], boxes[i2])

    # Part 1
    circuits = []
    if times:
      for i in range(times):
        addCircuit(circuits, distances[i])


      circuits.sort(key=lambda r: -len(r))
      s = 1
      for i in range(3):
        print(circuits[i])
        s *= len(circuits[i])

      print(f'Solution to 1: {s}')

      # Part 2 - keep going
      i = times
      while len(circuits[0]) < len(boxes):
        addCircuit(circuits, distances[i])
        i+=1
      
      lastD = distances[i - 1]
      print(lastD)
      print(f'Solution to 2: {lastD.a.x * lastD.b.x}')
     


def main():
    run('example.txt', 10)
    run('8.txt', 1000)    

    return 0
                


if __name__ == "__main__":
    main()