import math
import re
import numpy as np
from functools import cache
from enum import Enum

class DIR(Enum):
   UP = 'up'
   DOWN =  'down'
   LEFT = 'left'
   RIGHT = 'right'


class Node:
  def __init__(self, x, y, dir, steps, prev):
    self.id = f'{x}_{y}_{dir}_{steps}'
    self.x = x
    self.y = y
    self.loss = int(grid[x][y])
    self.dir = dir
    self.steps = steps
    self.prev = prev
    self.totalLoss = self._totalLoss()
       
  def __repr__(self):
    return f'cards is {self.id} with steps {self.steps}'\
      f' and loss {self.loss} {self.totalLoss} and previous {self.prev.id}'

  def _totalLoss(self):
    loss = self.loss
    node = self
    while node.prev:
      node = node.prev
      loss += node.loss
    return loss

grid = []                   

def goDir(x, y, dir, steps, node, nodes):
  if steps > 10:
    return None
  match dir:
    case DIR.RIGHT:
      if y < len(grid[0]) - 1:
        nodes.append(Node(x, y+1, DIR.RIGHT, steps, node))
    case DIR.LEFT:
      if y > 0:
        nodes.append(Node(x, y-1, DIR.LEFT, steps, node))
    case DIR.UP:
      if x > 0:
        nodes.append(Node(x -1, y, DIR.UP, steps, node))
    case DIR.DOWN:
      if x < len(grid) - 1:
        nodes.append(Node(x + 1, y, DIR.DOWN, steps, node))
  return None


def main():
  with open("day17.txt") as f:
    for line in f:
      grid.append([x for x in line.strip()])

  bestPath = 0
  visited = {}
  nodes = []
  allLeafs = []
  maxLoss = 1000000000000000000000000000000
  bestNode = None
  start = Node(0, 0, DIR.DOWN, 0, None)
  visited[start.id] = start
  nodes.append(Node(0, 1, DIR.RIGHT, 1, start))
  nodes.append(Node(1, 0, DIR.DOWN, 1, start))
  while len(nodes) > 0:
    node = nodes.pop(0)
    loss = int(node.totalLoss)


    if loss >= maxLoss:
      continue
    if node.id in visited.keys():
      old = visited[node.id]
      if old.totalLoss <= node.totalLoss:
        continue
      # print(f'update node {node} with {old.totalLoss}')
    else:
      prune = node
      shouldPrune = False
      # Is there another earlier path that's better
      while prune.prev:
        prune = prune.prev
        if visited[prune.id].totalLoss < prune.totalLoss:
          shouldPrune = True
          break
      if shouldPrune:
        print(f'prune {len(nodes)}')
        continue


    visited[node.id] = node
    x = node.x
    y = node.y
    dir = node.dir
    steps = node.steps
    rows = len(grid) - 1
    cols = len(grid[0]) - 1

    cur = grid[x][y]
    if x == rows and y == cols:
     print(f'Found an end at {node} and {loss} and {len(nodes)}')
     if loss < maxLoss:
      bestNode = node
      maxLoss = loss
      continue
    
    path = 0
    match dir:
      case DIR.UP:
        goDir(x, y, DIR.UP, steps+1, node, nodes)
        if steps >= 4:
          goDir(x, y, DIR.LEFT, 1, node, nodes)
          goDir(x, y, DIR.RIGHT, 1, node, nodes)
      case DIR.DOWN:
        goDir(x, y, DIR.DOWN, steps+1, node, nodes)
        if steps >= 4:
          goDir(x, y, DIR.LEFT, 1, node, nodes)
          goDir(x, y, DIR.RIGHT, 1, node, nodes)
      case DIR.RIGHT:
        goDir(x, y, DIR.RIGHT, steps+1, node, nodes)
        if steps >= 4:
          goDir(x, y, DIR.UP, 1, node, nodes)
          goDir(x, y, DIR.DOWN, 1, node, nodes)
      case DIR.LEFT:
        goDir(x, y, DIR.LEFT, steps+1, node, nodes)
        if steps >= 4:
          goDir(x, y, DIR.UP, 1, node, nodes)
          goDir(x, y, DIR.DOWN, 1, node, nodes)
    
    # print(f'Found the best path is {path} and {cur} at {x} and {y}')
    
  print(np.array(grid))
  print(f'Found {bestNode} with {bestNode.totalLoss}')
  #1194 is too low...? Found a path with 1200 which is too high
  node = bestNode
  grid[node.x][node.y] = '*'
  while node.prev:
    node = visited[node.prev.id]
    grid[node.x][node.y] = '*'
  
  print(np.array(grid))
 
          
if __name__ == "__main__":
    main()
