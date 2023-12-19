import math


def calculate(line):
  line = line.strip()
  print(line)
  line = line.replace('one','one1one').replace('two','two2two').replace('three','three3three'). \
      replace('four','four4four').replace('five','five5five').replace('six','six6six').\
        replace('seven','seven7seven'). \
      replace('eight','eight8eight').replace('nine','nine9nine')
  print(line)
  val = [i for i in line if i.isdigit()]
  val = [val[0],val[-1]]
  print(val)
  num = int(''.join(val))
  print(num)
  return num
  

def main():
  f = open("trebuchet.txt")
  lines = f.readlines()
  sum = 0
  for line in lines:
    sum += calculate(line)
    
  print(f"final sum is {sum}")  


if __name__ == "__main__":
    main()