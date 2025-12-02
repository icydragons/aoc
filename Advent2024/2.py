# Playing around with copilot rather then solving it myself

def is_safe(levels):
    # Check if all increasing or all decreasing (strictly monotonic)
    diffs = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
    if all(d > 0 for d in diffs):
        direction = 1
    elif all(d < 0 for d in diffs):
        direction = -1
    else:
        return False

    # Check if all diffs are between 1 and 3 (absolute value)
    if all(1 <= abs(d) <= 3 for d in diffs):
        return True
    return False

def main():
    safe_count = 0
    with open("aoc/Advent2024/2.txt") as f:
        for line in f:
            levels = list(map(int, line.strip().split()))
            if len(levels) < 2:
                continue
            if is_safe(levels):
                safe_count += 1
    print(safe_count)


    safe_count = 0
    with open("aoc/Advent2024/2.txt") as f:
        for line in f:
            levels = list(map(int, line.strip().split()))
            if len(levels) < 2:
                continue
            if is_safe(levels):
                safe_count += 1
            else:
                # Try removing each level once
                for i in range(len(levels)):
                    new_levels = levels[:i] + levels[i+1:]
                    if len(new_levels) >= 2 and is_safe(new_levels):
                        safe_count += 1
                        break
    print(safe_count)

if __name__ == "__main__":
    main()