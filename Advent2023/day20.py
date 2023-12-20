import math
import re
import numpy as np
from functools import cache
from enum import Enum


LOW = np.array([1, 0])
HIGH = np.array([0, 1])

class Module():
   def __init__(self, id, dest):
      self.id = id
      self.dest = dest

   def __repr__(self):
      return f'{self.type} {self.id} -> {self.dest}'
  
   def handlePulse(self, pulse, queue, prevId):
      raise Exception('not implemented')

class Broadcaster(Module):
   type = 'broadcaster'

   def handlePulse(self, pulse, queue, prevId):
      # keeps the same pulse
      for dest in self.dest:
        queue.append([dest, pulse, self.id])

class Flip(Module):
   type = '%'
   isOn = False

   def handlePulse(self, pulse, queue, prevId):
      if (pulse == HIGH).all():
         return
      self.isOn = not self.isOn
      newPulse = HIGH if self.isOn else LOW
      for dest in self.dest:
        queue.append([dest, newPulse, self.id])

class Conj(Module):
   type = '&'
   
   def initializeMemory(self, modules):
      self.memory = {}
      for module in modules.values():
         if self.id in module.dest:
            self.memory[module.id] = LOW
      

   def handlePulse(self, pulse, queue, prevId):
      self.memory[prevId] = pulse
      newPulse = HIGH
      if all((x == HIGH).all() for x in self.memory.values()):
         newPulse = LOW
      for dest in self.dest:
        queue.append([dest, newPulse, self.id])

def pushButton(modules):
  queue = []
  counts = np.array([0, 0])
  queue.append(['broadcaster', LOW, ''])
  while len(queue) > 0:
     id, pulse, prevId = queue.pop(0)
     # print(f'{prevId} -{pulse} -> {id}')
     counts += pulse
     if id in modules:
      module = modules[id]
      module.handlePulse(pulse, queue, prevId)
  print(f'One cycle gives {counts} pulsese')
  return counts
   

def run(filename):
  modules = {}
  conjs = []
  with open(filename) as f:
    for line in f:
      module, dest = [x.strip() for x in line.strip().split("->")]
      id = module.replace('%', '').replace('&','')
      dest = [x.strip() for x in dest.split(',')]
      if 'broadcaster' in module:
         module = Broadcaster(id, dest)
      elif '%' in module:
         module = Flip(id, dest)
      elif '&' in module:
         module = Conj(id, dest)
         conjs.append(module)
      modules[id] = module 

  print(modules) 
  
  for conj in conjs:
     conj.initializeMemory(modules)

  print(modules)
     
  counts = np.array([0, 0])
  for i in range(1000):
    counts += pushButton(modules)
  print(counts)
  print(counts[0]*counts[1])


def main():
  run("day20.txt")


if __name__ == "__main__":
    main()