import math
import re


def main():
  reg = re.compile('^(\d+)\\1$')
  reg2 = re.compile('^(\d+)\\1+$')
  ranges = []
  with open("Advent2025/2.txt") as f:
    for line in f:
      ranges = line.split(',')
  
    print(ranges)

    s = 0
    for i in range(len(ranges)):
      start,end = [int(x) for x in ranges[i].split('-')]
      sols = []
      while start <= end:
        sols.extend(int(x+x) for x in reg.findall(str(start)))
        start+=1
      print(sols)
      s += sum(sols)

    print(f'Part 1: {s}')

    s = 0
    for i in range(len(ranges)):
      start,end = [int(x) for x in ranges[i].split('-')]
      print(start, end)
      sols = []
      while start <= end:
        if reg2.match(str(start)):
          sols.append(start)
        start+=1
      print(sols)
      s += sum(sols)

    print(f'Part 2: {s}')



    return 0
                


if __name__ == "__main__":
    main()