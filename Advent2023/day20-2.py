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
  
# Graph viz link
# https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%20%20vh%20-%3E%20qc%2C%20rr%0Apb%20-%3E%20gf%2C%20gv%2C%20vp%2C%20qb%2C%20vr%2C%20hq%2C%20zj%0Azj%20-%3E%20kn%2C%20pb%0Amm%20-%3E%20dj%0Agp%20-%3E%20cp%0Adc%20-%3E%20ns%0Aqc%20-%3E%20gp%0Adx%20-%3E%20fq%2C%20dj%0Atg%20-%3E%20nl%2C%20ks%0Apr%20-%3E%20nl%0Agx%20-%3E%20xf%0Ahd%20-%3E%20lt%2C%20nl%0Adq%20-%3E%20dj%2C%20jc%0Aht%20-%3E%20jv%0Abs%20-%3E%20pb%2C%20rd%0Anl%20-%3E%20ks%2C%20cq%2C%20tc%2C%20xf%2C%20gx%2C%20hd%2C%20lt%0Adj%20-%3E%20dc%2C%20fq%2C%20jz%2C%20ht%2C%20zs%2C%20jc%0Arr%20-%3E%20gp%2C%20rv%2C%20jt%2C%20qc%2C%20sq%0Avr%20-%3E%20qb%0Ajz%20-%3E%20dj%2C%20ht%0Ahq%20-%3E%20nx%0Acf%20-%3E%20jg%2C%20rr%0Ahj%20-%3E%20cf%2C%20rr%0Amt%20-%3E%20rr%0Asq%20-%3E%20rr%2C%20vh%0Ajg%20-%3E%20rr%2C%20pd%0Agf%20-%3E%20gv%0Axv%20-%3E%20dj%2C%20dx%0Arh%20-%3E%20nl%2C%20gx%0Abroadcaster%20-%3E%20hd%2C%20zj%2C%20sq%2C%20jz%0Ajv%20-%3E%20dj%2C%20zs%0Ard%20-%3E%20vs%2C%20pb%0Apd%20-%3E%20rr%2C%20mt%0Arv%20-%3E%20ns%0Avp%20-%3E%20ns%0Avs%20-%3E%20pb%0Anx%20-%3E%20pb%2C%20bs%0Azp%20-%3E%20mm%2C%20dj%0Ans%20-%3E%20rx%0Alt%20-%3E%20rh%0Apf%20-%3E%20pr%2C%20nl%0Atc%20-%3E%20qz%0Axz%20-%3E%20dj%2C%20zp%0Aqb%20-%3E%20hq%0Arl%20-%3E%20pf%2C%20nl%0Afq%20-%3E%20xz%0Akn%20-%3E%20pb%2C%20xn%0Axf%20-%3E%20tg%0Aqz%20-%3E%20nl%2C%20rl%0Aks%20-%3E%20tc%0Ajt%20-%3E%20kb%0Ajc%20-%3E%20xv%0Akb%20-%3E%20hj%2C%20rr%0Azs%20-%3E%20dq%0Agv%20-%3E%20vr%0Acq%20-%3E%20ns%0Acp%20-%3E%20rr%2C%20jt%0Axn%20-%3E%20pb%2C%20gf%0A%7D

def main():
  run("day20.txt")


if __name__ == "__main__":
    main()