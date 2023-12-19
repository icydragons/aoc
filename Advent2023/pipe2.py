import math
import re

class Node:
  def __init__(self, i, j, prev):
    self.id = f'{i}_{j}'
    self.i = i
    self.j = j
    self.prev = prev
    self.depth = 0 if prev == None else prev.depth + 1

  def __repr__(self):
    return f"location is {self.i}, {self.j} and previous is \
    {self.prev.i}, {self.prev.j} with depth {self.depth}"
  


def main():
  visited = {}
  nodes = []
  map = []
  with open("pipe.txt") as f:
    for line in f:
      l = [x.strip() for x in line.strip()]
      map.append(l)
  
  print(map)
  for i in range(len(map)):
    for j in range(len(map[0])):
      c = map[i][j]
      if c == 'S':
        start = Node(i, j, None)
        nodes.append(
          #Node(i, j-1, start), Node(i, j+1, start),
                     Node(i+1, j, start))
       # nodes.append(Node(i-1, j, start))

  endNode = None     
  while len(nodes) > 0:
    node = nodes.pop(0)
    if node.id in visited:
      continue
    char = map[node.i][node.j]
    print(f'visiting {node} and {char}')
    if char == 'S':
      if node.depth > 2:
        endNode = node
        print(f'Made it! Total length {node.depth}')
        break
      else:
        continue
    visited[node.id] = True
    if char == '|':
      nodes.append(Node(node.i - 1, node.j, node))
      nodes.append( 
                   Node(node.i + 1, node.j, node))
    if char == '-':
      nodes.append(Node(node.i, node.j - 1, node))
      nodes.append( 
                   Node(node.i, node.j + 1, node))
    if char == 'L':
      nodes.append(Node(node.i - 1, node.j, node))
      nodes.append( 
                   Node(node.i, node.j + 1, node))
    if char == 'J':
      nodes.append(Node(node.i - 1, node.j, node))
      nodes.append( 
                   Node(node.i, node.j - 1, node))
    if char == '7':
      nodes.append(Node(node.i + 1, node.j, node))
      nodes.append( 
                   Node(node.i, node.j - 1, node))
    if char == 'F':
      nodes.append(Node(node.i + 1, node.j, node))
      nodes.append( 
                   Node(node.i, node.j + 1, node))


  node = endNode
  vertices = []
  boundaryPoints = 0
  while node.prev:
    char = map[node.i][node.j]
    if char in 'LJ7F':
      vertices.append([node.i, node.j])
    node = node.prev
    boundaryPoints += 1
  
  area = 0
  for i in range(len(vertices)):
    next = (i + 1) % len(vertices)
    vertex = vertices[i]
    nextV = vertices[next]
    area += vertex[0] * nextV[1] - vertex[1] * nextV[0]
  
  area = abs(area) / 2

  print(f'the area is {area}, the boundary is {boundaryPoints} and answer ' \
        f'{area - boundaryPoints / 2 + 1}')
  

      


    


if __name__ == "__main__":
    main()