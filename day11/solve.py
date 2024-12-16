def load(filename: str):
    with open(filename, 'r') as filedata:
        return [int(x) for x in filedata.read().strip().split(' ')]
    
def apply_rules(filename: str, steps: int):
    stones = load(filename)
    
    step = 0
    while step < steps:
        nb_stones = len(stones)
        n = 0
        while n < nb_stones:
            stone = stones[n]
            length = len(str(stone))
            if stone == 0:
                stones[n] = 1
            elif length % 2 == 0:
                stones[n] = int(stone / (10 ** (length/2)))
                stones.insert(n+1, int(stone - stones[n] * (10 ** (length/2))))
                n += 1
                nb_stones += 1
            else:
                stones[n] = stone * 2024
            n += 1
        step += 1
    return len(stones)

print("first part:")
print(apply_rules('day11/sample', 25))
print(apply_rules('day11/input', 25))