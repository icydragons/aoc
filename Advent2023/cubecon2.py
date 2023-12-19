import math
import re

class Game:
    def __init__(self, header, runs):
      id = header.split(' ')[-1]
      self.id = int(id)
      print(runs)
      self.greens = re.findall(r'([0-9]+)\s+(?:green)', runs)
      self.blues = re.findall(r'([0-9]+)\s+(?:blue)', runs)
      self.reds = re.findall(r'([0-9]+)\s+(?:red)', runs)
               
    def __repr__(self):
     return f"id is {self.id} greens are {self.greens}, blues are {self.blues}, reds are {self.reds}"
    
    def power(self):
       return max(int(green) for green in self.greens) * \
          max(int(blue) for blue in self.blues)  * \
          max(int(red) for red in self.reds) 

def main():
  f = open("cubecon.txt")
  lines = f.readlines()
  sum = 0
  cardarray = []
  for line in lines:
    game = re.split(':', line.strip())
    print(f"{game}")
    game = Game(game[0], game[1])
    pow = game.power()
    print(f"The power is {pow}")
    sum += pow
       
  print(f"final sum is {sum}")  


if __name__ == "__main__":
    main()