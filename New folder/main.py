import sys

def power4(values, index, total):
    if index == len(values):
        return total

    value = int(values[index])

    if value <= 0:
        total = total + (value ** 4)

    return power4(values, index + 1, total)
        
def cases(lines, index, remaining, results):
    if remaining == 0:
        return results

    x = int(lines[index])
    numbers = lines[index + 1].split()

    if len(numbers) != x:
        results.append(-1)
    else:
        answer = power4(numbers, 0, 0)
        results.append(answer)

    return cases(lines, index + 2, remaining - 1, results)

def print_results(results, index):
    if index == len(results):
        return

    print(results[index])
    print_results(results, index + 1)
    
def main():
    lines = sys.stdin.readlines()
    n = int(lines[0])
    results = cases(lines, 1, n, [])
    print_results(results, 0)


if __name__ == "__main__":
    main()