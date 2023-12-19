import math
import re


pattern = re.compile('[0-9.]')

def main():
  with open("gear.txt") as f:
    grid = []
    for line in f:
      row = []
      for char in line.strip():
        row.append(char)
      grid.append(row)
  
  sum = 0
  gears = {}
  for i in range(0, len(grid)):
    row = grid[i]
    num = ''
    gearsToAdd = []
    for j in range(0, len(row)):
      char = row[j]
      if char.isnumeric():
        num += char
        for ii in range(max(0, i-1), min(len(grid), i+2)):
          for ji in range(max(0, j-1), min(len(row), j+2)):
            if grid[ii][ji] == '*':
              print(f'ispart {num} and {char}')
              gearsToAdd.append(f'{ii}_{ji}')
      
      if not char.isnumeric() or j == len(row) - 1:
        if len(num) > 0:
          if gearsToAdd:
            print(f'gears to add are {gearsToAdd} and num is {num}')
            n = int(num)
            for gear in gearsToAdd:
              print(gears)
              parts = gears[gear] if gear in gears else []
              parts.append(n)
              print(parts)
              gears[gear] = parts

              print(f'Found a gear {gear} with {n} now have {gears[gear]}')
            gearsToAdd = []
          num = ''
  sum = 0
  for key in gears:
    parts = list(set(gears[key]))
    print(f'found {parts} in gears {key}')
    if len(parts) == 2:
      sum += parts[0]*parts[1]

  
  print(f'done {sum}')
        
      
                


if __name__ == "__main__":
    main()