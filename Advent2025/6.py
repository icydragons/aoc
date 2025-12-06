import math
import re

def part1():
  problems = []
  with open("Advent2025/6.txt") as f:
    for line in f:
       nums = re.split(r'\s+',line.strip())
       if len(problems) < 1:
          for num in nums: problems.append([])
       for i in range(len(nums)):
          problems[i].append(nums[i])

    s = 0
    for problem in problems:
       if problem[-1] == '+':
          s += sum(int(x) for x in problem[:-1])  
       else:
          s += math.prod(int(x) for x in problem[:-1]) 

    print(f'solution to 1: {s}')
   
def toVal(row):
   val = ''.join([str(x) for x in row if re.match(r'\d', x)])
   return int(val)

def main():
  part1()
  grid = []
  with open("Advent2025/6.txt") as f:
    for line in f:
       grid.append([x or ' ' for x in line])
    
    # Transpose the grid
    grid = list(map(list, zip(*grid)))
    print(grid)
    problems = []
    problem = []
    ops = []
    for row in grid:
       if (all(x == ' ' for x in row)):
          problems.append(problem)
          problem = []
       else:
          op = row[-1]
          if op in ('+','*'): ops.append(op) 
          problem.append(toVal(row))

    problems.append(problem)

    s = 0           
    for i in range(len(problems)):
      problem = problems[i]
      if ops[i] == '+':
          s += sum(int(x) for x in problem)  
      else:
          s += math.prod(int(x) for x in problem) 

    print(f'solution to 2: {s}')


    return 0
                


if __name__ == "__main__":
    main()