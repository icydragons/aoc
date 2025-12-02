import math
import re


def main():
  l = []
  with open("Advent2025/1.txt") as f:
    for line in f:
      l.append(line)

    pos = 50
    count = 0
    for i in range(len(l)):
      dir = l[i][0]
      val = int(l[i][1:])
      if dir == 'R':
        pos = (pos - val) % 100
      else:
        pos = (pos + val) % 100
      
      if pos == 0:
        count+=1

    print(f'Part 1: {count}')

    pos = 50
    count = 0
    for i in range(len(l)):
  
      dir = l[i][0]
      oval = int(l[i][1:])
      count+=math.floor(oval/100)
      val = oval % 100

      if dir == 'R':
        np = pos - val  
        if np < 1:
          # was overcounting when it started on 0
          if pos > 0:
            count +=1
          pos = (100 + np) % 100
        else:  
          pos = np
      else:
        np = pos + val
        count += 1 if np > 99 else 0 
        pos = np % 100
      
      print(pos, dir, oval, val, count)

    print(f'Part 2: {count}')




    return 0
                


if __name__ == "__main__":
    main()