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
    if distance > 6500:
      print(f'Hit the end at {distance} and {len(visited.keys())}')
      print(sorted(visited.keys()))
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
  # To print label:
  # https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0A%0D%0A%220_1%22%20-%3E%20%2213_15%22%20%5Blabel%3D191%5D%0D%0A%2213_15%22%20-%3E%20%220_1%22%20%5Blabel%3D191%5D%0D%0A%2213_15%22%20-%3E%20%2237_19%22%20%5Blabel%3D228%5D%0D%0A%2213_15%22%20-%3E%20%2219_33%22%20%5Blabel%3D124%5D%0D%0A%2237_19%22%20-%3E%20%2213_15%22%20%5Blabel%3D228%5D%0D%0A%2237_19%22%20-%3E%20%2255_9%22%20%5Blabel%3D128%5D%0D%0A%2237_19%22%20-%3E%20%2243_39%22%20%5Blabel%3D74%5D%0D%0A%2219_33%22%20-%3E%20%2243_39%22%20%5Blabel%3D138%5D%0D%0A%2219_33%22%20-%3E%20%2213_15%22%20%5Blabel%3D124%5D%0D%0A%2219_33%22%20-%3E%20%229_57%22%20%5Blabel%3D262%5D%0D%0A%2255_9%22%20-%3E%20%2237_19%22%20%5Blabel%3D128%5D%0D%0A%2255_9%22%20-%3E%20%2289_19%22%20%5Blabel%3D372%5D%0D%0A%2255_9%22%20-%3E%20%2253_35%22%20%5Blabel%3D96%5D%0D%0A%2243_39%22%20-%3E%20%2219_33%22%20%5Blabel%3D138%5D%0D%0A%2243_39%22%20-%3E%20%2253_35%22%20%5Blabel%3D26%5D%0D%0A%2243_39%22%20-%3E%20%2237_19%22%20%5Blabel%3D74%5D%0D%0A%2243_39%22%20-%3E%20%2231_65%22%20%5Blabel%3D154%5D%0D%0A%229_57%22%20-%3E%20%2231_65%22%20%5Blabel%3D98%5D%0D%0A%229_57%22%20-%3E%20%2219_33%22%20%5Blabel%3D262%5D%0D%0A%229_57%22%20-%3E%20%2219_89%22%20%5Blabel%3D298%5D%0D%0A%2289_19%22%20-%3E%20%2255_9%22%20%5Blabel%3D372%5D%0D%0A%2289_19%22%20-%3E%20%22109_5%22%20%5Blabel%3D186%5D%0D%0A%2289_19%22%20-%3E%20%2283_35%22%20%5Blabel%3D74%5D%0D%0A%2253_35%22%20-%3E%20%2243_39%22%20%5Blabel%3D26%5D%0D%0A%2253_35%22%20-%3E%20%2283_35%22%20%5Blabel%3D198%5D%0D%0A%2253_35%22%20-%3E%20%2255_9%22%20%5Blabel%3D96%5D%0D%0A%2253_35%22%20-%3E%20%2261_55%22%20%5Blabel%3D100%5D%0D%0A%2231_65%22%20-%3E%20%229_57%22%20%5Blabel%3D98%5D%0D%0A%2231_65%22%20-%3E%20%2261_55%22%20%5Blabel%3D168%5D%0D%0A%2231_65%22%20-%3E%20%2243_39%22%20%5Blabel%3D154%5D%0D%0A%2231_65%22%20-%3E%20%2243_81%22%20%5Blabel%3D128%5D%0D%0A%2219_89%22%20-%3E%20%2243_81%22%20%5Blabel%3D124%5D%0D%0A%2219_89%22%20-%3E%20%229_57%22%20%5Blabel%3D298%5D%0D%0A%2219_89%22%20-%3E%20%2217_107%22%20%5Blabel%3D220%5D%0D%0A%22109_5%22%20-%3E%20%2289_19%22%20%5Blabel%3D186%5D%0D%0A%22109_5%22%20-%3E%20%22123_39%22%20%5Blabel%3D440%5D%0D%0A%22109_5%22%20-%3E%20%22105_41%22%20%5Blabel%3D220%5D%0D%0A%2283_35%22%20-%3E%20%2253_35%22%20%5Blabel%3D198%5D%0D%0A%2283_35%22%20-%3E%20%22105_41%22%20%5Blabel%3D120%5D%0D%0A%2283_35%22%20-%3E%20%2289_19%22%20%5Blabel%3D74%5D%0D%0A%2283_35%22%20-%3E%20%2287_53%22%20%5Blabel%3D86%5D%0D%0A%2261_55%22%20-%3E%20%2231_65%22%20%5Blabel%3D168%5D%0D%0A%2261_55%22%20-%3E%20%2287_53%22%20%5Blabel%3D184%5D%0D%0A%2261_55%22%20-%3E%20%2253_35%22%20%5Blabel%3D100%5D%0D%0A%2261_55%22%20-%3E%20%2259_85%22%20%5Blabel%3D176%5D%0D%0A%2243_81%22%20-%3E%20%2219_89%22%20%5Blabel%3D124%5D%0D%0A%2243_81%22%20-%3E%20%2259_85%22%20%5Blabel%3D52%5D%0D%0A%2243_81%22%20-%3E%20%2231_65%22%20%5Blabel%3D128%5D%0D%0A%2243_81%22%20-%3E%20%2231_109%22%20%5Blabel%3D160%5D%0D%0A%2217_107%22%20-%3E%20%2231_109%22%20%5Blabel%3D56%5D%0D%0A%2217_107%22%20-%3E%20%2219_89%22%20%5Blabel%3D220%5D%0D%0A%2217_107%22%20-%3E%20%2233_127%22%20%5Blabel%3D436%5D%0D%0A%22123_39%22%20-%3E%20%22105_41%22%20%5Blabel%3D80%5D%0D%0A%22123_39%22%20-%3E%20%22109_5%22%20%5Blabel%3D440%5D%0D%0A%22123_39%22%20-%3E%20%22129_53%22%20%5Blabel%3D116%5D%0D%0A%22105_41%22%20-%3E%20%2283_35%22%20%5Blabel%3D120%5D%0D%0A%22105_41%22%20-%3E%20%22123_39%22%20%5Blabel%3D80%5D%0D%0A%22105_41%22%20-%3E%20%22109_5%22%20%5Blabel%3D220%5D%0D%0A%22105_41%22%20-%3E%20%22107_57%22%20%5Blabel%3D62%5D%0D%0A%2287_53%22%20-%3E%20%2261_55%22%20%5Blabel%3D184%5D%0D%0A%2287_53%22%20-%3E%20%22107_57%22%20%5Blabel%3D64%5D%0D%0A%2287_53%22%20-%3E%20%2283_35%22%20%5Blabel%3D86%5D%0D%0A%2287_53%22%20-%3E%20%2277_79%22%20%5Blabel%3D172%5D%0D%0A%2259_85%22%20-%3E%20%2243_81%22%20%5Blabel%3D52%5D%0D%0A%2259_85%22%20-%3E%20%2277_79%22%20%5Blabel%3D88%5D%0D%0A%2259_85%22%20-%3E%20%2261_55%22%20%5Blabel%3D176%5D%0D%0A%2259_85%22%20-%3E%20%2261_101%22%20%5Blabel%3D114%5D%0D%0A%2231_109%22%20-%3E%20%2217_107%22%20%5Blabel%3D56%5D%0D%0A%2231_109%22%20-%3E%20%2261_101%22%20%5Blabel%3D110%5D%0D%0A%2231_109%22%20-%3E%20%2243_81%22%20%5Blabel%3D160%5D%0D%0A%2231_109%22%20-%3E%20%2233_127%22%20%5Blabel%3D120%5D%0D%0A%2233_127%22%20-%3E%20%2217_107%22%20%5Blabel%3D436%5D%0D%0A%2233_127%22%20-%3E%20%2261_127%22%20%5Blabel%3D216%5D%0D%0A%2233_127%22%20-%3E%20%2231_109%22%20%5Blabel%3D120%5D%0D%0A%22129_53%22%20-%3E%20%22107_57%22%20%5Blabel%3D114%5D%0D%0A%22129_53%22%20-%3E%20%22123_39%22%20%5Blabel%3D116%5D%0D%0A%22129_53%22%20-%3E%20%22127_75%22%20%5Blabel%3D212%5D%0D%0A%22107_57%22%20-%3E%20%2287_53%22%20%5Blabel%3D64%5D%0D%0A%22107_57%22%20-%3E%20%22129_53%22%20%5Blabel%3D114%5D%0D%0A%22107_57%22%20-%3E%20%22105_41%22%20%5Blabel%3D62%5D%0D%0A%22107_57%22%20-%3E%20%22105_79%22%20%5Blabel%3D108%5D%0D%0A%2277_79%22%20-%3E%20%2259_85%22%20%5Blabel%3D88%5D%0D%0A%2277_79%22%20-%3E%20%22105_79%22%20%5Blabel%3D136%5D%0D%0A%2277_79%22%20-%3E%20%2287_53%22%20%5Blabel%3D172%5D%0D%0A%2277_79%22%20-%3E%20%2279_113%22%20%5Blabel%3D248%5D%0D%0A%2261_101%22%20-%3E%20%2231_109%22%20%5Blabel%3D110%5D%0D%0A%2261_101%22%20-%3E%20%2279_113%22%20%5Blabel%3D74%5D%0D%0A%2261_101%22%20-%3E%20%2259_85%22%20%5Blabel%3D114%5D%0D%0A%2261_101%22%20-%3E%20%2261_127%22%20%5Blabel%3D210%5D%0D%0A%2261_127%22%20-%3E%20%2233_127%22%20%5Blabel%3D216%5D%0D%0A%2261_127%22%20-%3E%20%2289_129%22%20%5Blabel%3D218%5D%0D%0A%2261_127%22%20-%3E%20%2261_101%22%20%5Blabel%3D210%5D%0D%0A%22127_75%22%20-%3E%20%22105_79%22%20%5Blabel%3D122%5D%0D%0A%22127_75%22%20-%3E%20%22129_53%22%20%5Blabel%3D212%5D%0D%0A%22127_75%22%20-%3E%20%22123_103%22%20%5Blabel%3D284%5D%0D%0A%22105_79%22%20-%3E%20%2277_79%22%20%5Blabel%3D136%5D%0D%0A%22105_79%22%20-%3E%20%22127_75%22%20%5Blabel%3D122%5D%0D%0A%22105_79%22%20-%3E%20%22107_57%22%20%5Blabel%3D108%5D%0D%0A%22105_79%22%20-%3E%20%22105_113%22%20%5Blabel%3D262%5D%0D%0A%2279_113%22%20-%3E%20%2261_101%22%20%5Blabel%3D74%5D%0D%0A%2279_113%22%20-%3E%20%22105_113%22%20%5Blabel%3D118%5D%0D%0A%2279_113%22%20-%3E%20%2277_79%22%20%5Blabel%3D248%5D%0D%0A%2279_113%22%20-%3E%20%2289_129%22%20%5Blabel%3D102%5D%0D%0A%2289_129%22%20-%3E%20%2261_127%22%20%5Blabel%3D218%5D%0D%0A%2289_129%22%20-%3E%20%2299_133%22%20%5Blabel%3D66%5D%0D%0A%2289_129%22%20-%3E%20%2279_113%22%20%5Blabel%3D102%5D%0D%0A%22123_103%22%20-%3E%20%22105_113%22%20%5Blabel%3D132%5D%0D%0A%22123_103%22%20-%3E%20%22127_75%22%20%5Blabel%3D284%5D%0D%0A%22123_103%22%20-%3E%20%22133_127%22%20%5Blabel%3D166%5D%0D%0A%22105_113%22%20-%3E%20%2279_113%22%20%5Blabel%3D118%5D%0D%0A%22105_113%22%20-%3E%20%22123_103%22%20%5Blabel%3D132%5D%0D%0A%22105_113%22%20-%3E%20%22105_79%22%20%5Blabel%3D262%5D%0D%0A%22105_113%22%20-%3E%20%2299_133%22%20%5Blabel%3D74%5D%0D%0A%2299_133%22%20-%3E%20%2289_129%22%20%5Blabel%3D66%5D%0D%0A%2299_133%22%20-%3E%20%22133_127%22%20%5Blabel%3D260%5D%0D%0A%2299_133%22%20-%3E%20%22105_113%22%20%5Blabel%3D74%5D%0D%0A%22133_127%22%20-%3E%20%2299_133%22%20%5Blabel%3D260%5D%0D%0A%22133_127%22%20-%3E%20%22140_139%22%20%5Blabel%3D71%5D%0D%0A%22133_127%22%20-%3E%20%22123_103%22%20%5Blabel%3D166%5D%0D%0A%22140_139%22%20-%3E%20%22133_127%22%20%5Blabel%3D71%5D%0D%0A%7D
  #totalWeight = 0 
  #for node in intersections.values():
  #   for edge, d in node.edges.values():
  #     print(f'"{node.id}" -> "{edge.id}" [label={d}]')
  #     totalWeight += d
  #print(totalWeight/2)
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