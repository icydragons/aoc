import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
import pprint

### THIS DOES NOT WORK!!!!!!!!!!!!!!!!!!!!!!!!!

PPlates = {}

class Direction(Enum):
  UP = (-1, 0)
  DOWN = (1, 0)
  LEFT = (0, -1)
  RIGHT = (0, 1)

directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

class Tile():
  def __init__(self, i, j, distance, plate):
    self.id = f'{i}_{j}'
    self.i = i
    self.j = j
    self.distance = distance
    self.plate = plate
  
  def __repr__(self):
    return f'Tile {self.id} and {self.distance} and {self.plate.id}'


class Point():
  def __init__(self, i, j, distance):
    self.i = i
    self.j = j
    self.id = f'{i}_{j}'
    self.distance = distance
  
  def __repr__(self):
    return f'Point {self.id}'

class Edge():
  def __init__(self, direction, line):
    self.direction = direction
    self.line = np.array(line)
    # print(direction, line)
    self.min = min([int(x) for x in line if isinstance(x, int)])
    self.max = max([int(x) for x in line if isinstance(x, int)])
    self.exits = [i for i,d in enumerate(line) if d==self.min]
  
  def getNewEntrances(self, map):
    entrances = []
    for exit in self.exits:
      match self.direction:
        case Direction.UP:
          entrances.append(Point(len(map) - 1, exit, 0))
        case Direction.DOWN:
          entrances.append(Point(0, exit, 0))
        case Direction.LEFT:
          entrances.append(Point(exit, len(map[0]) - 1, 0))
        case Direction.RIGHT:
          entrances.append(Point(exit, 0, 0))
    return entrances


  def __repr__(self):
    return f'{self.direction}, {self.line}, {self.min}, {self.max}, {self.exits}'


def makePlateId(entrances):
  return ";".join(entrance.id for entrance in entrances)

class PPlate():
  def __init__(self, entrances, map, steps):
    self.id = makePlateId(entrances)
    self.entrances = entrances
    self.map = copy.deepcopy(map)
    self.initialize(steps)

  def __repr__(self):
    return f'Map {self.id} has {self.count} and between {self.min} and {self.max} steps'

  def initialize(self, steps):
    entrances = []
    for entrance in self.entrances:
      entrances.append(Point(entrance.i, entrance.j, 0))
    self.map, self.visited = makeMap(entrances, self.map)
    
    count = 0
    for val in self.visited.values():
      if val % 2 == steps % 2:
        count += 1
    self.count = count
    np.set_printoptions(threshold=10000000,linewidth=1000000)
    # print(np.array(self.map))
    edges = {}
    edges[Direction.UP] = Edge(Direction.UP, self.map[0])
    edges[Direction.DOWN] = Edge(Direction.DOWN, self.map[len(self.map) - 1]) 
    left = []
    right = []  
    for i in range(len(self.map)):
      left.append(self.map[i][0])
      right.append(self.map[i][len(self.map[0]) - 1])
    edges[Direction.LEFT] = Edge(Direction.LEFT, left)
    edges[Direction.RIGHT] = Edge(Direction.RIGHT, right)
    self.edges = edges
    self.max = max([edge.max for edge in self.edges.values()])
    self.min = min([edge.min for edge in self.edges.values()])
  
  def calculateCount(self, totalSteps, stepsRemaining):
    if stepsRemaining >= self.max:
      return self.count
    return len([x for x in self.visited.values() if
                x <= stepsRemaining and x % 2 == totalSteps % 2])


def makeMap(starts, map): 
  queue = starts
  visited = {}

  while (len(queue) > 0):
    node = queue.pop(0)
    if node.id in visited.keys():
      continue
    visited[node.id] = node.distance
    map[node.i][node.j] = node.distance

    for direction in directions:
      go(direction, node, queue, map)

  return map, visited

def go(direction, node, queue, map):
  i = node.i + direction.value[0]
  j = node.j + direction.value[1]
  if i >= 0 and i < len(map) and j >= 0 and j < len(map[0]):
    char = map[i][j]
    if char == '#':
      # Rock
      return
    queue.append(Point(i, j, node.distance + 1))


def runMap(baseMap, steps, plateCache):
  print(f'starting {len(baseMap)}')
  
  # print(baseMap)
  startPoints = [Point(int((len(baseMap)-1)/2), int((len(baseMap[0])-1)/2), 0)]
  start = Tile(0, 0, 0, PPlate(startPoints, baseMap, steps))
  print(start)
  count = 0
  tileCount = 0
  plateCache[makePlateId(startPoints)] = start
  visited = {}
  queue = [start]
  fullTileDistance = 67433
  while len(queue) > 0:
    tile = queue.pop(0)
    if tile.id in visited.keys():
      continue
    visited[tile.id] = tile.distance
    if tile.distance > steps:
      continue
    tileCount += 1
    stepsToGo = steps - tile.distance
    tcount = tile.plate.calculateCount(steps, stepsToGo)
    print(f'Plate {tile.plate} is adding {tcount} at {tileCount} and {tile.distance} and {stepsToGo} more steps')
    count += tcount

    # UP = 4435994471, 392, 588, 195 
    # DOWN = 4435994476, 195
    # LEFT = 4435994457
    # RIGHT = 4435994490
    # 67434
    # Up example:
    #       195 -  392  - 195
    # 195 - 558 -  Full - 558 - 195
    dirs = [Direction.LEFT]
    if tileCount > 67432:
      dirs = directions

    distanceAway = abs(tile.i) + abs(tile.j)
    for direction in directions:
      edge = tile.plate.edges[direction]
      entrances = edge.getNewEntrances(baseMap)
      entranceDistance = tile.distance + edge.min + 1
      if entranceDistance > steps:
        continue
      i = tile.i + direction.value[0]
      j = tile.j + direction.value[1]
      newDistanceAway = abs(i) + abs(j)
      if distanceAway >= newDistanceAway:
        continue
      plateId = makePlateId(entrances)
      plate = None
      if plateId in plateCache.keys():
        # print(f'Found plate {plateId}')
        plate = plateCache[plateId]
      else:
        # print(f'New plate {plateId}')
        plate = PPlate(entrances, baseMap, steps)
        plateCache[plateId] = plate
      queue.append(Tile(i, j, entranceDistance, plate))   

  # pprint.pprint(plateCache)
  print(count)
  return(count)


def doMath(steps): 
  # UP = 4435994471, 392, 588, 195 
  # DOWN = 4435994476, 195
  # LEFT = 4435994457
  # RIGHT = 4435994490
  # 67434
  # Full ones extend up for 67433 in a triangle pattern
  # Up example, steps left:
  #       195 -  392  - 195
  # 195 - 588 -  Full - 588 - 195
  # This means there are 67432 of the each of the 558 steps corners
  # One of each of the 392 ends
  # 67433 of each of the 195 corners
  # (1 + 3 + ... + 134863)*2 + 134865 = 134864*134864/2 + 134865 times 65783
  fullMapCount = 65783 
  SW195 = 8178
  NW195 = 8153
  NE195 = 8167
  SE195 = 8192
  SW588 = 57591
  NW588 = 57610
  NE588 = 57629
  SE588 = 57605
  N = 49432
  S = 49437
  E = 49451
  W = 49418
  total = 0
  total += (SW195 + SE195 + NW195 + NE195)*67433
  total += (SW588 + SE588 + NW588 + NE588)*67432
  total += N + S + E + W
  total += int(134864 * 134864/2 + 134865)*fullMapCount
  # 149582284215763
  # 598267035015124
  # 598267035080907 is wrong
  print(total)
  # 594606492802848 another answer
  # is wrong 592519386562691
  # 581387762708291 is wrong
  # 598044246091813
  # 598044246091826
  print(int(14613*steps*steps/17161 + 32167*steps/17161 - 111106/17161))
  # 139744678793741
  

  

def run(filename, steps):
  baseMap = []
  threeMap = []
  nineMap = []
  twentySevenMap = []
  eightyOneMap = []
  with open(filename) as f:
    for line in f:
      row = [x for x in line.strip()]
      baseMap.append(row)
      threeMap.append(row.copy()*3)
      nineMap.append(row.copy()*9)
      twentySevenMap.append(row.copy()*27)
      eightyOneMap.append(row.copy()*81)
  
  rows = len(threeMap)
  for i in range(rows*2):
    threeMap.append(threeMap[i].copy())
  for i in range(rows*8):
    nineMap.append(nineMap[i].copy())
  for i in range(rows*26):
    twentySevenMap.append(twentySevenMap[i].copy())
  for i in range(rows*80):
    eightyOneMap.append(eightyOneMap[i].copy())
  
  plateCache = {}
  # runMap(baseMap, steps, plateCache)
  #runMap(threeMap, steps, plateCache)
  # runMap(nineMap, steps, plateCache)
  # runMap(twentySevenMap, steps, plateCache)
  # runMap(eightyOneMap, steps, plateCache)
  doMath(steps)
  # return

  stepsArray = []
  formulas = []
  for i in [65, 196, 327]:
    count = runMap(twentySevenMap, i, plateCache)
    stepsArray.append(count)
    formulas.append(count / i)

  # [3591, 33086, 91537]
  # [3591, 33086, 90993]
  # [3591, 33086, 90993]
  # Now with odds!
  # [3726, 33086, 90932]
  # [3726, 33086, 91128]
  # [3726, 33086, 91672]
  # [3726, 33086, 91672]
  doMath(steps)

  # [8739, 1031926, 3767420, 8211806, 14355016, 22214756, 31792413, 43063392, 56057597, 70732998]
  # quadratic fit {100, 8739}, {1100,1031926}, {2100,3767420}, {3100,8211806}, {4100,14355016}, {5100,22214756}, {6100,31792413}, {7100,43063392}, {8100,56057597}, {9100,70732998}
  # [853345, 103090801, 375660517, 818645902, 1431998179, 2215651583, 3169770018, 4294156984, 5588970236, 7054228447]
  # quadratic fit {1000, 853345}, {11000,103090801}, {21000,375660517}, {31000,818645902}, {41000,1431998179}, {51000,2215651583}, {61000,3169770018}, {71000,4294156984}, {81000,5588970236}, {91000,7054228447}
  print(stepsArray)
  print(formulas) 
    

  
def main():
  run("day21.txt", 26501365) # 26501365)


if __name__ == "__main__":
    main()