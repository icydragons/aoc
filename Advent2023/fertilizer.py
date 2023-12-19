import math
import re

class Map:
   def __init__(self, id, elements):
      self.id = id
      self.elements = [[int(e) for e in element.split(' ')] for element in elements]
      self.elements = sorted(self.elements, key=lambda x: x[1])
               
   def __repr__(self):
      return f"id is {self.id} elements are {self.elements}"
   
   def findNext(self, source, count):
      values = []
      for elem in self.elements:
        sourceE = elem[1]
        destE = elem[0]
        countE = elem[2]
        print(f'{self.id} elem {elem} and id {id}')
        # Have some before this element
        if (sourceE > source):
          # Have all before this element. DONE
          if sourceE > source + count:
             values.extend([source, count])
             print(f'Found {values} before a map')
             return values
          # Some before...
          dif = sourceE - source
          values.extend([source, dif])
          count = count - dif
          source = sourceE
          # Keep going
        
        # SourceE is <= source now. so if we have some in the count
        if sourceE + countE > source:
          newDest = source - sourceE + destE
          # is it all ?
          if sourceE + countE >= source + count:
            values.extend([newDest, count])
            print(f'Found {values} inside a map')
            return values
          # Must only have found some...
          
          newCount = (source + count) - (sourceE + countE)
          values.extend([newDest, count - newCount])
          count = newCount
          source = (sourceE + countE)

      # Out of the for loop, but still have some left
      values.extend([source, count])
      print(f'Found {values} at the end')
      return values
        
        
                  
def runMap(map, values):
  newVals = []
  for i in range(0, len(values), 2):
    start = values[i]
    length = values[i+1]
    newVals.extend(map.findNext(start, length))
    
  print(f'{map.id}: Started with {values} and ended with {newVals}')
  return newVals



def main():
  with open("fertilizer.txt") as f:
    # seeds
    seeds = [int(seed) for seed in 
             f.readline().strip().split(': ')[1].split(' ')]
    print(seeds)
    maps = {}
    for line in f:
       if ':' in line:
          id = line.split(' map')[0]
          elements = []
          for l in f:
             if len(l) > 1:
                elements.append(l.strip())
             else:
                break         
          m = Map(id, elements)
          maps[id] = m
          print(m)
       
    locations = []
    values = seeds
    values = runMap(maps['seed-to-soil'], values)
    values = runMap(maps['soil-to-fertilizer'], values)
    values = runMap(maps['fertilizer-to-water'], values)
    values = runMap(maps['water-to-light'], values)
    values = runMap(maps['light-to-temperature'], values)
    values = runMap(maps['temperature-to-humidity'], values)
    values = runMap(maps['humidity-to-location'], values)
    locations = values[0::2]
    locations.append(min(locations))
    locations.sort()
    print(f'full locations {locations} and the min is {locations[0]}')
           
           
        
      


if __name__ == "__main__":
    main()