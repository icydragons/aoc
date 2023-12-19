import math
import re
import numpy as np
from functools import cache
from enum import Enum
from sortedcontainers import SortedList

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
    self.totalLoss = (prev.totalLoss if prev else 0) + self.loss
       
  def __repr__(self):
    prev = self.prev.id if self.prev else None
    return f'cards is {self.id} with steps {self.steps}'\
      f' and loss {self.loss} {self.totalLoss} and previous {prev}'

grid = []                   

def goDir(x, y, dir, steps, node, nodes):
  if steps > 10:
    return None
  newNode = None
  match dir:
    case DIR.RIGHT:
      if y < len(grid[0]) - 1:
        newNode = Node(x, y+1, DIR.RIGHT, steps, node)
    case DIR.LEFT:
      if y > 0:
        newNode = Node(x, y-1, DIR.LEFT, steps, node)
    case DIR.UP:
      if x > 0:
        newNode = Node(x -1, y, DIR.UP, steps, node)
    case DIR.DOWN:
      if x < len(grid) - 1:
        newNode = Node(x + 1, y, DIR.DOWN, steps, node)
  if newNode:
    if nodes[newNode.totalLoss]:
      nodes[newNode.totalLoss].append(newNode)
    else:
      nodes[newNode.totalLoss] = [newNode]
  return None


def main():
  with open("day17.txt") as f:
    for line in f:
      grid.append([x for x in line.strip()])

  visited = {}
  maxTime = 10000000
  nodes = [None] * maxTime
  bestNode = None
  nodes[0] = [Node(0, 1, DIR.RIGHT, 1, None), Node(1, 0, DIR.DOWN, 1, None)]
  rows = len(grid) - 1
  cols = len(grid[0]) - 1
  for i in range(maxTime):
    tic = nodes[i]
    if bestNode:
      break
    if not tic:
      continue
    for node in tic:
      loss = int(node.totalLoss)
      if node.id in visited.keys():
        continue

      visited[node.id] = node
      x = node.x
      y = node.y
      dir = node.dir
      steps = node.steps
      if x == rows and y == cols:
        print(f'Found an end at {node} and {loss} and {len(nodes)}')
        bestNode = node
        break
      
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
  node = bestNode
  grid[node.x][node.y] = '*'
  while node.prev:
    node = visited[node.prev.id]
    grid[node.x][node.y] = '*'
  
  print(np.array(grid))
 
          
if __name__ == "__main__":
    main()
