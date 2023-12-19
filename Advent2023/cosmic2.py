import math
import re
import functools  


def main():
  visited = {}
  nodes = []
  map = []
  rowsToAdd = []
  with open("cosmic.txt") as f:
    row = 0
    for line in f:
      row += 1
      l = [x.strip() for x in line.strip()]
      # append all rows twice if no galaxy
      if '#' not in l:
        rowsToAdd.append(row)
      map.append(l)
  
  colsToAdd = []
  for j in range(len(map[0])):
    for i in range(len(map)):
      if map[i][j] == '#':
        break
      if i == len(map) - 1:
        colsToAdd.append(j)

  print(colsToAdd) 
  print(rowsToAdd) 

  extra = 999999
  galaxies = []
  for i in range(len(map)):
    for j in range(len(map[0])):
      if map[i][j] == '#':
        extraRows = functools.reduce(lambda a, b: a + 1 if b <= i else a, rowsToAdd, 0)
        extraCols = functools.reduce(lambda a, b: a + 1 if b <= j else a, colsToAdd, 0)
        galaxies.append([i + extra * extraRows, j + extra * extraCols])
        print(f'at {i},{j} extra rows {extraRows} and cols {extraCols} got {galaxies[-1]}')
  

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