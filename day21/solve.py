def load(filename: str):
    codes = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            codes.append(line.strip())
            
    numerical = {'7': (0,0), '8': (0,1), '9': (0,2), '4': (1,0), '5': (1,1), '6': (1,2), '1': (2,0), '2': (2,1), '3': (2,2), '/': (3,0), '0': (3,1), 'A': (3,2)}
    directional = {'/': (0,0), '^': (0,1), 'A': (0,2), '<': (1,0), 'v': (1,1), '>': (1,2)}
    
    return codes, numerical, directional

def horizontal_first_blocked(position, target, pad_map) -> bool:
    if (position[0],target[1]) == pad_map['/']:
        return True
    return False

def vertical_first_blocked(position, target, pad_map) -> bool:
    if (target[0],position[1]) == pad_map['/']:
        return True
    return False

def get_vertical_sequence(position: tuple[int, int], target: tuple[int, int]) -> str:
    if target[0] > position[0]:
        return 'v' * (target[0] - position[0])
    else:
        return '^' * (position[0] - target[0])

def get_horizontal_sequence(position: tuple[int, int], target: tuple[int, int]) -> str:
    if target[1] > position[1]:
        return '>' * (target[1] - position[1])
    else:
        return '<' * (position[1] - target[1])
    
def get_sequences(position: tuple[int, int], target: tuple[int, int],
                  pad_map: dict[str, tuple[int, int]]) -> list[str]:
    sequences = []
    if not horizontal_first_blocked(position, target, pad_map):
        sequence = get_horizontal_sequence(position, target)
        sequence += get_vertical_sequence(position, target)
        sequences.append(sequence)
    if not vertical_first_blocked(position, target, pad_map):
        sequence = get_vertical_sequence(position, target)
        sequence += get_horizontal_sequence(position, target)
        sequences.append(sequence)
    return sequences

def converts(code: str, pad_map: dict[str, tuple[int, int]]) -> list[str]:
    position = pad_map['A']
    sequences = set([''])
    for c in code:
        target = pad_map[c]
        new_seq = set()
        next_sequences = get_sequences(position, target, pad_map)
        for s in sequences:
            for ns in next_sequences:
                new_seq.add(s + ns + 'A')
        sequences = new_seq
        position = target
    return sequences

def get_complexity(filename: str) -> int:
    codes, numerical, directional = load(filename)
    complexity = 0
    
    for code in codes:
        firsts = converts(code, numerical)
        seconds = []
        for first in firsts:
            seconds.extend(converts(first, directional))
        thirds = []
        for second in seconds:
            thirds.extend(converts(second, directional))
        thirds.sort(key=lambda t: len(t))
        
        complexity += len(thirds[0].replace(' ', '')) * int(code.replace('A',''))
    
    return complexity

print("first part:")
print(get_complexity('day21/sample'))
print(get_complexity('day21/input'))