def load(filename: str):
    towels = []
    patterns = []
    
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            if len(line.strip()) == 0:
                # skip blank lines
                continue
            
            if ',' in line:
                towels = line.strip().replace(' ', '').split(',')
            else:
                patterns.append(line.strip())
                
    towels.sort(key=lambda t: len(t), reverse=True)
    
    return towels, patterns

def is_pattern_buildable(pattern: str, towels: list[str], min: int, cache: set[str]) -> bool:
    if pattern in cache:
        return False
    if len(pattern) < min:
        cache.add(pattern)
        return False
    
    for towel in towels:
        if pattern == towel:
            return True
        if pattern.startswith(towel):
            if is_pattern_buildable(pattern.replace(towel, '', 1), towels, min, cache):
                return True
    cache.add(pattern)
    return False

def solve(filename: str):
    towels, patterns = load(filename)
    min = len(towels[-1])
    cache = set()
    
    nb = 0
    for pattern in patterns:
        if is_pattern_buildable(pattern, towels, min, cache):
            nb += 1
        
    return nb

print("first part:")
print(solve('day19/sample'))
print(solve('day19/input'))