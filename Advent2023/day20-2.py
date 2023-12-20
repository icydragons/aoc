import math
import re
import numpy as np
from functools import cache
from enum import Enum
import pprint

LOW = np.array([1, 0])
HIGH = np.array([0, 1])

class Module():
   def __init__(self, id, dest):
      self.id = id
      self.dest = dest
      self.pulses = np.array([0,0])
      self.runs = []
      self.inputs = []
      self.rememberPulse = None
      self.rememberPulses = []

   def __repr__(self):
      return f'{self.type} {self.id} -> {self.dest} with history: {self.runs}'
    
   def handleEnd(self):
      self.runs.append(self.pulses)
      if (self.rememberPulse == LOW).all() and self.pulses[0] > 0:
        self.rememberPulses.append(len(self.runs))
      self.pulses = np.array([0,0])
    
   def initialize(self, modules):
      for module in modules.values():
         if self.id in module.dest:
            self.inputs.append(module.id)
      

class Broadcaster(Module):
   type = 'broadcaster'

   def handlePulse(self, pulse, queue, prevId):
      # keeps the same pulse
      self.pulses += pulse
      for dest in self.dest:
        queue.append([dest, pulse, self.id])
  
   def isDefault(self):
      return True

class Flip(Module):
   type = '%'
   isOn = False

   def handlePulse(self, pulse, queue, prevId):
      if (pulse == HIGH).all():
         return
      self.isOn = not self.isOn
      newPulse = HIGH if self.isOn else LOW
      self.pulses += newPulse
      for dest in self.dest:
        queue.append([dest, newPulse, self.id])
  
   def isDefault(self):
      return not self.isOn

class Conj(Module):
   type = '&'
   
   def initialize(self, modules):
      super().initialize(modules)
      self.memory = {}
      for id in self.inputs:
        self.memory[id] = LOW
      
   def handlePulse(self, pulse, queue, prevId):
      self.memory[prevId] = pulse
      newPulse = HIGH
      if all((x == HIGH).all() for x in self.memory.values()):
         newPulse = LOW
      self.pulses += newPulse
         
      for dest in self.dest:
        queue.append([dest, newPulse, self.id])
   
   def isDefault(self):
      return all((x == LOW).all() for x in self.memory.values())
   
   def solve(self, pulse):
      self.rememberPulse = pulse
         

def pushButton(modules):
  queue = []
  counts = np.array([0, 0])
  count = 0
  queue.append(['broadcaster', LOW, ''])
  while len(queue) > 0:
     id, pulse, prevId = queue.pop(0)
     # print(f'{prevId} -{pulse} -> {id}')
     counts += pulse
     if id in modules:
      module = modules[id]
      module.handlePulse(pulse, queue, prevId)
     if id == 'rx' and (pulse == LOW).all():
      count+=1
  # print(f'One cycle gives {counts} pulsese and {count}')
  return count
   

def run(filename):
  modules = {}
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
      modules[id] = module 

  for module in modules.values():
     module.initialize(modules)
     
  # initialize data
  key = ['dj', 'nl', 'pb', 'rr']
  for id in key:
     modules[id].solve(LOW)
     
  for i in range(5000):
    count = pushButton(modules)
    for module in modules.values():
       module.handleEnd()
  
  # pprint.pprint(modules)
  pprint.pprint(modules['dj'].rememberPulses)
  pprint.pprint(modules['nl'].rememberPulses)
  pprint.pprint(modules['pb'].rememberPulses)
  pprint.pprint(modules['rr'].rememberPulses)
 
  lcm = 1
  for id in key:
      i = modules[id].rememberPulses[0]
      lcm = lcm*i//math.gcd(lcm, i)
  print(lcm)
  


def main():
  run("day20.txt")


if __name__ == "__main__":
    main()