import math
import re
  


def main():
  visited = {}
  nodes = []
  map = []
  with open("cosmic.txt") as f:
    for line in f:
      l = [x.strip() for x in line.strip()]
      # append all rows twice if no galaxy
      if '#' not in l:
        map.append(l)
      map.append(l)
  
  colsToAdd = []
  for j in range(len(map[0])):
    for i in range(len(map)):
      if map[i][j] == '#':
        break
      if i == len(map) - 1:
        colsToAdd.append(j)

  print(colsToAdd)

  for row in map:
    for loc in reversed(colsToAdd):
      row.insert(loc, '.')  

  galaxies = []
  for i in range(len(map)):
    for j in range(len(map[0])):
      if map[i][j] == '#':
        galaxies.append([i, j])
  

  print(galaxies)
  sum = 0
  for i in range(len(galaxies)- 1):
    for j in range(i + 1, len(galaxies)):
      x1 = galaxies[i][0]
      y1 = galaxies[i][1]
      x2 = galaxies[j][0]
      y2 = galaxies[j][1]
      distance = abs(x1-x2) + abs(y1-y2)
      print(f'Found the distance between {i} {galaxies[i]} and {j} {galaxies[j]} as {distance}')
      sum += distance


  print(sum)  


    


if __name__ == "__main__":
    main()