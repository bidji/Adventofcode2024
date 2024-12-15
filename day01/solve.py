from collections import Counter

def get_list(filename: str) -> tuple[list[int], list[int]]:
    left = []
    right = []
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            data = line.strip().split(' ')
            left.append(int(data[0]))
            right.append(int(data[-1]))
    return left, right
    
def get_distance(filename: str) -> int:
    left, right = get_list(filename)
    left.sort()
    right.sort()
    distance = 0
    for i in range(0, len(left)):
        distance += abs(left[i] - right[i])
    return distance

def get_similarity(filename: str) -> int:
    left, right = get_list(filename)
    similarity = 0
    counter = Counter(right)
    for value in left:
        similarity += value * counter[value]
    return similarity
    
print("first part:")
print(get_distance('day01/sample'))
print(get_distance('day01/input'))
      
print("second part:")
print(get_similarity('day01/sample'))
print(get_similarity('day01/input'))