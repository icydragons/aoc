import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
import pprint

class Direction(Enum):
  UP = (-1, 0)
  DOWN = (1, 0)
  LEFT = (0, -1)
  RIGHT = (0, 1)

slopes = {
  'v': Direction.DOWN,
  '^': Direction.UP,
  '>': Direction.RIGHT,
  '<': Direction.LEFT
}

class Point():
  def __init__(self, i, j, distance):
    self.i = i
    self.j = j
    self.id = f'{i}_{j}'
    self.distance = distance
  
  def __repr__(self):
    return f'Point {self.id} {self.distance}'

def go(direction, node, map):
  i = node.i + direction.value[0]
  j = node.j + direction.value[1]
  if i >= 0 and i < len(map) and j >= 0 and j < len(map[0]):
    char = map[i][j]
    if char == '#':
      # Rock
      return
    return Point(i, j, node.distance + 1)

def walkPath(queue, visited, map, useSlopes):
  distance = 0
  while len(queue) > 0:
    node = queue.pop(0)
    if node.i == (len(map) - 1) and node.j == (len(map[0]) - 2):
      distance = max(distance, node.distance)
      print(f'Hit the end at {distance} and {node}')
    if node.id in visited.keys():
      continue
    visited[node.id] = node.distance
    char = map[node.i][node.j]
    directions = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]
    if char in slopes.keys() and useSlopes:
      directions = [slopes[char]]
    paths = []
    for direction in directions:
      point = go(direction, node, map)
      if point and point.id not in visited.keys():
        paths.append(point)
    
    for i,path in enumerate(paths):
      # Last one can just use the current things
      if i == len(paths) - 1:
        queue.append(path)
      else:
        newQueue = copy.deepcopy(queue)
        newVisited = copy.deepcopy(visited)
        newQueue.append(path)
        distance = max(distance, walkPath(newQueue, newVisited, map, useSlopes))
  
  
  print(f'I found a path of {distance}')
  return distance


def run(filename):
  map = []
  with open(filename) as f:
    for line in f:
      map.append(line.strip())
  
  start = Point(0, 1, 0)
  visited = {}
  queue = [start]
  distance = walkPath(queue, visited, map, False)
  print(distance)
  
def main():
  run("day23.txt")


if __name__ == "__main__":
    main()