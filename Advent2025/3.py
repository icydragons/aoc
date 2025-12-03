import math
import re

def maxBank(bank, num):
  curIndex = 0
  sum = 0
  for i in range(1, num):
    mv = max(bank[curIndex:-num + i])
    curIndex = bank[curIndex:].index(mv) + curIndex + 1
    sum += int(mv*10**(num - i))
  # last one needs no end index...
  mv = max(bank[curIndex:]) 
  return sum + mv


def main():
  banks = []
  with open("Advent2025/3.txt") as f:
    for line in f:
      banks.append([int(x) for x in line.strip()])

    s = 0
    for bank in banks:
       max = maxBank(bank, 2)
       s+=max    

    print(f'Part 1: {s}')

    s = 0
    for bank in banks:
       max = maxBank(bank, 12)
       s+=max
    

    print(f'Part 2: {s}')
    return 0
                


if __name__ == "__main__":
    main()