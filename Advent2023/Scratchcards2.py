import math
import re


class Card:
    def __init__(self, header, numbers, sol):
      id = header.split(' ')[-1]
      self.id = int(id)
      self.sols = sol.split(' ')
      self.vals = numbers.split(' ')
      self.calculated = -1
      self.sols.sort()
      self.vals.sort()      
       
    def __repr__(self):
     return f"id is {self.id} sols are {self.sols} vals are {self.vals}"

    def calculate(self, cardarray):
      if self.calculated > -1:
        return self.calculated

      matches = 0
      for val in self.vals:
        if val is "":
          continue
        if val in self.sols:
          matches += 1
      print(f"found {matches} matches")
      cards = 1
      for j in range(matches):
       newcard = cardarray[self.id + j]
       count = newcard.calculate(cardarray)
       print(f"Adding another card {newcard.id} with {count}")
       cards += count

      print(f"total cards created for {self.id} is {cards}")
      self.calculated = cards
      return cards

def main():
  f = open("scratchpad-data.txt")
  lines = f.readlines()
  sum = 0
  cardarray = []
  for line in lines:
    cards = re.split(':|\|', line.strip())
    print(f"{cards}")
    card = Card(cards[0], cards[1], cards[2])
    # will be at id - 1
    cardarray.append(card)

  total = 0
  for card in cardarray:
    total += card.calculate(cardarray)
       
  print(f"final sum is {total}")  


if __name__ == "__main__":
    main()