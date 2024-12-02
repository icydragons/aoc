import math
import re


def howCanGo(time, distance):
  for i in range(0,time):
    far = i * (time - i)
    if far > distance:
      first = i
      last = time - i
      total = last - first + 1
      return total


def main():
  l1 = []
  l2 = []
  with open("Advent2024/1.txt") as f:
    for line in f:
      l = line.strip().split('   ')
      print(l)
      l1.append(int(l[0]))
      l2.append(int(l[1]))

    l1.sort()
    l2.sort()
    l2b = l2[::-1]
    sum = 0
    for i in range(len(l1)):
      sum += abs(l1[i] - l2[i])

    print(sum)

    sum = 0
    for i in range(len(l1)):
      val = l1[i]
      try:
        index = l2.index(val)
        end = len(l2) - l2b.index(val)
        sum += val * (end - index)

      except:
        continue

    print(sum)




    return 0
                


if __name__ == "__main__":
    main()