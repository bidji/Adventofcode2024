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

def findall_builds(pattern: str, towels: list[str], min: int, not_buildables: set[str], buildables: dict[str, int]) -> int:
    if pattern in not_buildables:
        return 0
    if len(pattern) < min:
        not_buildables.add(pattern)
        return 0
    if pattern in buildables:
        return buildables[pattern]
    
    nb_builds = 0
    for towel in towels:
        if pattern == towel:
            nb_builds += 1
        elif pattern.startswith(towel):
            nb_builds += findall_builds(pattern.replace(towel, '', 1), towels, min, not_buildables, buildables)
            
    if nb_builds == 0:
        not_buildables.add(pattern)
    else:
        buildables[pattern] = nb_builds
    return nb_builds

def solve(filename: str, findall: bool) -> int:
    towels, patterns = load(filename)
    min = len(towels[-1])
    not_buildables = set()
    buildables = dict()
    
    nb = 0
    for pattern in patterns:
        nb_builds = findall_builds(pattern, towels, min, not_buildables, buildables)
        if nb_builds > 0:
            nb += 1 if not findall else nb_builds
            
    return nb

print("first part:")
print(solve('day19/sample', findall=False))
print(solve('day19/input', findall=False))

print("second part:")
print(solve('day19/sample', findall=True))
print(solve('day19/input', findall=True))
