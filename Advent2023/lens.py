import math
import re
import numpy as np
from functools import cache

@cache
def compute(instruction):
   val = 0
   for char in instruction:
     ascii = ord(char) 
     val += ascii
     val *= 17
     val = val % 256
   return val



def main():
  instructions = []
  with open("lens.txt") as f:
    for line in f:
      instructions = [x for x in line.strip().split(',')]
      
  sum = 0
  boxes = {}
  for instruction in instructions:
    labels= re.split(r'(=|-)', instruction)
    label = labels[0]
    op = labels[1]
    val = compute(label)
    print(f'The value of {instruction} is {val} with {op}')
    box = boxes[val] if val in boxes.keys() else []
    if op == '=':
        focal = labels[2]
        found = False
        for lens in box:
           if lens[0] == label:
              lens[1] = focal
              found = True   
        if not found:
           box.append([label, focal])
        boxes[val] = box
        print(box)
    if op == '-':
        for lens in box:
           if lens[0] == label:
              box.remove(lens)
              break

  print(boxes)
  sum = 0 
  for i in boxes.keys():
      box = boxes[i]
      for j in range(len(box)):
        sum+= (i+1) * (j+1) * int(box[j][1])
        print(sum)

        
  
  print(sum)




        
      
                


if __name__ == "__main__":
    main()
