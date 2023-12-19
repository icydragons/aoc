import math
import re



class Node:
    def __init__(self, id, children):
      self.id = id
      self.left = children[2:5]  
      self.right = children[7:10]
       
    def __repr__(self):
     return f"cards is {self.id} and {self.left}, {self.right}"


def main():
  nodes = {}
  with open("haunted.txt") as f:
    instructions = f.readline().strip()
    f.readline()

    
    allstart = {}
    for line in f:
      l = line.strip().split('=')
      node = Node(l[0].strip(), l[1])
      print(node)
      nodes[node.id] = node
      if node.id[-1:] == 'A':
        allstart[node.id] = 0
    
    print(allstart)

    for start in allstart.keys():
      next = nodes[start]
      steps = 0
      while next.id[-1:] != 'Z':
        for i in range(len(instructions)):
          char = instructions[i]
          if char == 'L':
            next = nodes[next.left]
          if char == 'R':
            next = nodes[next.right]
          steps+=1
          if i == len(instructions) - 1:
            i = 0
      allstart[start] = steps
    
    print(allstart)
    lcm = 1
    for i in allstart.values():
        lcm = lcm*i//math.gcd(lcm, i)
    print(lcm)


    


if __name__ == "__main__":
    main()