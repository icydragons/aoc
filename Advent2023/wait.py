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
  with open("wait3.txt") as f:
    # seeds
    time = [int(s) for s in 
             f.readline().strip().split(': ')[1].split(' ') if len(s) > 0]
    distance = [int(d) for d in 
             f.readline().strip().split(': ')[1].split(' ') if len(d) > 0]
    print(time)
    print(distance)
    total = 1
    for i in range(0, len(time)):
      far = howCanGo(time[i], distance[i])
      total *= far
      print(f'Found {far} ways for {total}')

    return total
                


if __name__ == "__main__":
    main()