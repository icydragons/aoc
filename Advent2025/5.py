
  

def main():
  ranges = []
  ingredients = []
  with open("Advent2025/5.txt") as f:
    for line in f:
      if "-" in line:
       a,b = line.strip().split('-')
       ranges.append(range(int(a),int(b)+1))
      elif line.strip():
         ingredients.append(int(line.strip()))

    s = sum(1 for i in ingredients if any(i in r for r in ranges))
    print(f'Part 1: {s}')

    ranges = sorted(ranges, key=lambda r: r.start)
    newRanges = []
    cur = ranges[0]
    for r1 in ranges[1:]:
       if cur.stop <= r1.start:
          newRanges.append(cur)
          cur = r1
       else:
          cur = range(min(r1.start, cur.start), max(r1.stop, cur.stop))
    newRanges.append(cur)

    print(f'Part 2: {sum(len(r) for r in newRanges)}')
       
       

       


    return 0
                


if __name__ == "__main__":
    main()