import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
import pprint


class Node():
  def __init__(self, point):
    self.point = point
    self.edges = {}
    self.id = point.id
  
  def __repr__(self):
    return f'Node {self.id} edges: {[f"{n.id} {d}" for n,d in self.edges.values()]}'

  def addEdge(self, node, distance):
    self.edges[node.id] = (node, distance)

class Point():
  def __init__(self, i, j):
    self.i = i
    self.j = j
    self.id = f'{i}_{j}'
  
  def __repr__(self):
    return f'Point {self.id}'
  
  def __eq__(self, other):
    return self.id == other.id

  def __sub__(self, other):
      return Point(self.i - other.i, self.j - other.j)

  def __add__(self, other):
      return Point(self.i + other.i, self.j + other.j)

class Direction(Enum):
  UP = Point(-1, 0)
  DOWN = Point(1, 0)
  LEFT = Point(0, -1)
  RIGHT = Point(0, 1)

def go(direction, node, map):
  p = direction.value + node
  if 0 <=  p.i < len(map) and 0 <= p.j < len(map[0]):
    char = map[p.i][p.j]
    if char == '#':
      # Rock
      return
    return p

def walkPath(node, distance, visited, end):
  if node.point == end:
    # print(f'Hit the end at {distance} and {node}')
    return distance
  
  m = 0
  for edge, newDistance in node.edges.values():
    if edge.id in visited.keys():
      continue
    v = visited.copy()
    v[edge.id] = True
    m = max(m, walkPath(edge, distance + newDistance, v, end))
  return m

def computeSegment(path, map):
  while True:
    end = path[-1]
    neighbors = [go(direction, end, map) for direction in Direction]
    neighbors = [n for n in neighbors if n and n not in path]
    match len(neighbors):
      case 1:
        path.append(neighbors[0])
      case _:
        return path


def makeGraph(map, start):
  queue = [start]
  intersections = {}
  intersections[start.id] = start
  while len(queue) > 0:
    intersection = queue.pop(0)
    neighbors = [go(direction, intersection.point, map) for direction in Direction]
    segments = [computeSegment([intersection.point, neighbor], map) for neighbor in neighbors if neighbor]
    for segment in segments:
      next = Node(segment[-1])
      if next.id in intersections.keys():
        next = intersections[next.id]
      else:
        queue.append(next)
        intersections[next.id] = next
      intersection.addEdge(next, len(segment) -1)
       
  pprint.pprint(intersections)
  return start


def run(filename):
  map = []
  with open(filename) as f:
    for line in f:
      map.append(line.strip())
  
  start = makeGraph(map, Node(Point(0, 1)))
  end = Node(Point(len(map) - 1, len(map[0]) - 2))
  distance = walkPath(start, 0, {}, end)
  print(distance)
  
def main():
  run("day23.txt")


if __name__ == "__main__":
    main()