import math
import re
from functools import lru_cache, wraps
import numpy as np

def np_cache(*args, **kwargs):
    """LRU cache implementation for functions whose FIRST parameter is a numpy array
    >>> array = np.array([[1, 2, 3], [4, 5, 6]])
    >>> @np_cache(maxsize=256)
    ... def multiply(array, factor):
    ...     print("Calculating...")
    ...     return factor*array
    >>> multiply(array, 2)
    Calculating...
    array([[ 2,  4,  6],
           [ 8, 10, 12]])
    >>> multiply(array, 2)
    array([[ 2,  4,  6],
           [ 8, 10, 12]])
    >>> multiply.cache_info()
    CacheInfo(hits=1, misses=1, maxsize=256, currsize=1)
    
    """
    def decorator(function):
        @wraps(function)
        def wrapper(np_array, *args, **kwargs):
            hashable_array = tuple(map(tuple, np_array))
            return cached_wrapper(hashable_array, *args, **kwargs)

        @lru_cache(*args, **kwargs)
        def cached_wrapper(hashable_array, *args, **kwargs):
            array = np.array(hashable_array)
            return function(array, *args, **kwargs)

        # copy lru_cache attributes over too
        wrapper.cache_info = cached_wrapper.cache_info
        wrapper.cache_clear = cached_wrapper.cache_clear

        return wrapper

    return decorator

@np_cache()
def cycle(map):
  for x in range(4):
    #print(f'Map is {x} at \n{map}')
    for j in range(len(map[0])):
      val = 0
      for i in range(len(map)):
        if map[i][j] == '#':
          val = i+1
        if map[i][j] == 'O':
          map[i][j] = '.'
          map[val][j] = 'O'
          val += 1
    #print(f'Map after is \n{map}')
    map = np.transpose(map)
    for y in range(len(map)):
      map[y] = list(reversed(map[y]))
  
  return map

def calculateLoad(map, rows):
  sum = 0
  for j in range(len(map[0])):
    colSum = 0
    val = rows
    for i in range(len(map)):
      if map[i][j] == 'O':
        colSum += val - i
    # print(f'Column {j} has {colSum}')
    sum += colSum
  return sum

def main():
  map = []
  rows = 0
  with open("parabolic.txt") as f:
    for line in f:
      rows += 1
      l = [x for x in line.strip()]
      map.append(l)
  map = np.array(map)
  #cycle
  print(map)
  weights = []
  initialRuns = 300
  for i in range(initialRuns):
    original = map.copy()
    map = cycle(map) 
    if np.array_equal(original, map):
      print('done after {i} cycles')
    # print(f'cycle {i+1} has \n{map}')
    weights.append(calculateLoad(map, rows))   
  
  weights = list(reversed(weights))
  print(weights)
  cycle_len = 0
  for i in range(2, initialRuns):
    if cycle_len > 0:
      break
    for j in range(0, i):
      print(f'{weights[j]} and {weights[j+i]}')
      if (weights[j] != weights[(j+i)]):
        break
      if j == i - 1:
        cycle_len = i
  print(f'Cycle length is {cycle_len}')
  # calculate load
  sum = calculateLoad(map, rows)
  index = (1000000000 - initialRuns) % cycle_len
  print(f'{weights} and {index} and {weights[index]}')






    


if __name__ == "__main__":
    main()