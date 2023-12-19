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
  for i in range(0, len(grid)):
    row = grid[i]
    num = ''
    isPart = False
    for j in range(0, len(row)):
      char = row[j]
      if char.isnumeric():
        num += char
        for ii in range(max(0, i-1), min(len(grid), i+2)):
          for ji in range(max(0, j-1), min(len(row), j+2)):
            if not pattern.search(grid[ii][ji]):
              print(f'ispart {num} and {char}')
              isPart = True
      
      if not char.isnumeric() or j == len(row) - 1:
        if len(num) > 0:
          if isPart:
            n = int(num)
            sum += n
            print(f'Found a part {n} adding to sum to make {sum}')
            isPart = False
          num = ''
  
  print(f'done {sum}')
        
      
                


if __name__ == "__main__":
    main()