import copy

def countPaper(grid, r, c):
  return sum(hasPaper(grid, i, j) for i in (r-1,r,r+1) for j in (c-1,c,c+1) if i != r or j != c)

def hasPaper(grid, r, c):
      return grid[r][c] in ('@','x') if r in range(len(grid)) and c in range(len(grid[0])) else 0

def runSim(grid, keep):
  s = 0

  for row in range(len(grid)):
      for col in range(len(grid[row])):
        if grid[row][col] in ('@','x') and countPaper(grid, row, col) < 4:
          s+=1
          grid[row][col] = 'x' if keep else '.'

  return s
  

def main():
  grid = []
  with open("Advent2025/4.txt") as f:
    for line in f:
      grid.append([x for x in line.strip()])

    s = runSim(copy.deepcopy(grid), True)
    print(f'Part 1: {s}')

    s = 0
    while r := runSim(grid, False): s += r  
    print(f'Part 2: {s}')

    return 0
                


if __name__ == "__main__":
    main()