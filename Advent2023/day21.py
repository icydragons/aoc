import math
import re
import numpy as np
from functools import cache
from enum import Enum
import pprint


class Direction(Enum):
  UP = (-1, 0)
  DOWN = (1, 0)
  LEFT = (0, -1)
  RIGHT = (0, 1)

class Point():
  def __init__(self, i, j, distance):
    self.i = i
    self.j = j
    self.id = f'{i}_{j}'
    self.distance = distance

def go(direction, node, queue, map):
  i = node.i + direction.value[0]
  j = node.j + direction.value[1]
  if i >= 0 and i < len(map) and j >= 0 and j < len(map[0]):
    char = map[i][j]
    if char == '#':
      # Rock
      return
    queue.append(Point(i, j, node.distance + 1))


def run(filename, steps):
  map = []
  visited = {}
  start = [0,0]
  queue = []
  with open(filename) as f:
    for line in f:
      row = [x for x in line.strip()]
      map.append(row)
      if 'S' in row:
        start = Point(len(map) - 1, row.index('S'), 0)
        queue.append(start)
  
  start = Point(int((len(map)-1)/2), int((len(map[0])-1)/2), 0)
  queue.append(start)

  directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
  while (len(queue) > 0):
    node = queue.pop(0)
    if node.id in visited.keys():
      continue
    visited[node.id] = node.distance
    if node.distance > steps:
      continue

    for direction in directions:
      go(direction, node, queue, map)

  print(visited)
  count = 0
  for val in visited.values():
    if val % 2 == 0:
      count += 1

  print(count)
  
def main():
  run("day21.txt", 64)


if __name__ == "__main__":
    main()