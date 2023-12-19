import math
import re
    
def nextVal(seq):
  next = []
  if all(x == 0 for x in seq):
    return 0
  for i in range(len(seq) - 1):
    next.append(seq[i+1] - seq[i])
  
  val = nextVal(next)
  r = seq[-1] + val
  print(f'found the next level of {seq} is {val} and return {r}')
  return r


def main():
  nodes = {}
  with open("mirage.txt") as f:

    sum = 0
    for line in f:
      l = [int(x.strip()) for x in line.strip().split(' ')]
      sum += nextVal(l)

    print(sum)


      


    


if __name__ == "__main__":
    main()