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

class Node():
  def __init__(self, point):
    self.point = point
    self.edges = {}
    self.id = point.id
  
  def __repr__(self):
    return f'Node {self.id} edges: {[f"{n.id} {d}" for n,d in self.edges.values()]}'

  def addEdge(self, node, distance):
    self.edges[node.id] = (node, distance)
  
  def isEnd(self):
    return len(self.edges) < 1

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

def walkPath(node, distance, visited):
  if node.isEnd():
    # print(f'Hit the end at {distance} and {node}')
    return distance
  
  m = 0
  for edge, newDistance in node.edges.values():
    if edge.id in visited.keys():
      continue
    v = visited.copy()
    v[edge.id] = True
    m = max(m, walkPath(edge, distance + newDistance, v))
  return m

def makeGraph(map, start):
  distance = 0
  queue = [start]
  intersections = {}
  nodes = {}
  while len(queue) > 0:
    intersection = queue.pop(0)
    if intersection.id in intersections.keys():
      continue
    intersections[intersection.id] = intersection
    visited = {}
    innerQ = [intersection.point]
    while len(innerQ) > 0:
      node = innerQ.pop(0)
      if node.id in visited.keys():
        continue
      visited[node.id] = node.distance
      if node.i == (len(map) - 1) and node.j == (len(map[0]) - 2):
        newNode = Node(Point(node.i, node.j, 0))
        intersection.addEdge(newNode, node.distance)
        continue
      directions = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]
      paths = []
      for direction in directions:
        point = go(direction, node, map)
        if point and point.id not in visited.keys():
          paths.append(point)
      
      if len(paths) > 1 and intersection.id != node.id:
        newNode = None
        if node.id in nodes.keys():
          newNode = nodes[node.id]
        else:
          newNode = Node(Point(node.i, node.j, 0))
          nodes[newNode.id] = newNode
        intersection.addEdge(newNode, node.distance)
        queue.append(newNode)
        continue

      for path in paths:
        innerQ.append(path)
    
  pprint.pprint(intersections)
  return start


def run(filename):
  map = []
  with open(filename) as f:
    for line in f:
      map.append(line.strip())
  
  start = makeGraph(map, Node(Point(0, 1, 0)))
  distance = walkPath(start, 0, {})
  print(distance)
  
def main():
  run("day23.txt")


if __name__ == "__main__":
    main()