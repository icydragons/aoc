import math


def calculate(line):
  (input,sol) = line.strip().split(':')[1].split('|')
  print(input)
  print(sol)
  sols = sol.split(' ')
  vals = input.split(' ')
  sols.sort()
  vals.sort()
  print(f"{sols} and  {vals}")
  sum = 1
  for val in vals:
     if val is "":
       continue
     if val in sols:
        sum = sum*2
  print(f"returning {math.floor(sum/2)}")
  return math.floor(sum/2)
  

def main():
  f = open("scratchpad-data.txt")
  lines = f.readlines()
  sum = 0
  for line in lines:
    sum += calculate(line)
    
  print(f"final sum is {sum}")  


if __name__ == "__main__":
    main()