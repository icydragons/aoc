import math
import re
import copy
import numpy as np
from functools import cache, reduce
from enum import Enum
from typing import NamedTuple
import pprint

def countConnections(start, components):
  visited = {}
  visited[start] = True
  queue = components[start]
  while len(queue) > 0:
    component = queue.pop()
    if component in visited.keys():
      continue
    visited[component] = True
    queue.extend(components[component])
  
  print(len(visited.keys()))
  return len(visited.keys())


def run(filename):
  components = {}
  i = 0
  with open(filename) as f:
    for line in f:
      component, connections = line.strip().split(':')
      connections = connections.strip().split(' ')
      components[component.strip()] = connections

  for component in components:
    connections = components[component]
    print(f'{component} -> {",".join(connections)}')
  
  # Put the printed values into graphviz and.... Connections to break from graphviz
  # brd -> clb
  # mxd -> glz 
  # jxd -> bbz
  components['brd'].remove('clb')
  components['mxd'].remove('glz')
  components['jxd'].remove('bbz')

  # Add the two way connections
  fullComponents = components.copy()
  for component in components:
    for connection in components[component]:
      if connection in components.keys():
        fullComponents[connection].append(component)
      else:
        fullComponents[connection] = [component]

  one = countConnections('brd', fullComponents)
  two = countConnections('jxd', fullComponents)
  print(one * two)
  
  
def main():
  # run("day25-e.txt")
  run("day25.txt")


if __name__ == "__main__":
    main()