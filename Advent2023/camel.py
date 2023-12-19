import math
import re
import numpy

RANK = {
  'five': 10,
  'four': 9,
  'full': 8,
  'three': 7,
  'twop': 6,
  'pair': 5,
  'high': 4
}

def computeRank(cards):
    hist = {card: cards.count(card) for card in cards}
    keys = hist.keys()
    vals = sorted(hist.values(), reverse=True)
    print(vals)
    if vals == [5]:
       return RANK['five']
    if vals == [4,1]:
       return RANK['four']
    if vals == [3,2]:
       return RANK['full']
    if vals == [3,1,1]:
       return RANK['three']
    if vals == [2,2,1]:
       return RANK['twop']
    if vals == [2,1,1,1]:
       return RANK['pair']
    return RANK['high']


ORDER = 'AKQJT98765432'  

class Card:
    def __init__(self, cards, bid):
      self.cards = cards
      self.bid = int(bid)  
      self.rank = computeRank(cards)
       
    def __repr__(self):
     return f"cards is {self.cards} bid are {self.bid} rank is {self.rank}"
    
    def __lt__(self, other):
       if self.rank != other.rank:
          return self.rank < other.rank
       
       for i in range(len(self.cards)):
          s = self.cards[i]
          o = other.cards[i]
          if s == o:
             continue
          return ORDER.index(s) > ORDER.index(o)



def main():
  cards = []
  with open("camel.txt") as f:
    for line in f:
      l = line.strip().split(' ')
      card = Card(l[0], l[1])
      print(card)
      cards.append(card)
  
  cards.sort()

  sum = 0
  for i in range(len(cards)):
      card = cards[i]
      rank = i + 1
      print(f'{card} is position {rank}')
      sum += rank * card.bid
     
           
  print(f"final sum is {sum}")  


if __name__ == "__main__":
    main()