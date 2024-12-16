def load(filename: str):
    machines = []
    with open(filename, 'r') as filedata:
        machine = dict()
        for line in filedata.readlines():
            if len(line.strip()) == 0:
                continue
            
            data = line.strip().split(':')[1]
            if line.startswith('Button A:'):
                machine['A X+'] = int(data.split(',')[0].replace('X+', '').strip())
                machine['A Y+'] = int(data.split(',')[1].replace('Y+', '').strip())
            if line.startswith('Button B:'):
                machine['B X+'] = int(data.split(',')[0].replace('X+', '').strip())
                machine['B Y+'] = int(data.split(',')[1].replace('Y+', '').strip())
            if line.startswith('Prize:'):
                machine['Prize X'] = int(data.split(',')[0].replace('X=', '').strip())
                machine['Prize Y'] = int(data.split(',')[1].replace('Y=', '').strip())
                machines.append(machine)
                machine = dict()
    return machines

def count_needed_tokens(filename: str) -> int:
    machines = load(filename)
    
    needed_tokens = 0
    nb_prizes = 0
    for machine in machines:
        nb_tokens = 0
        max_a = min(int(machine['Prize X']/machine['A X+']), int(machine['Prize Y']/machine['A Y+']), 100)
        for a in range(0, max_a + 1):
            if (machine['Prize X'] - (a * machine['A X+'])) % machine['B X+'] == 0 and (machine['Prize Y'] - (a * machine['A Y+'])) % machine['B Y+'] == 0:
                # found a solution, check if b is pressed more than 100 times
                b = int((machine['Prize X'] - (a * machine['A X+'])) / machine['B X+'])
                if b >= 0 and b <= 100 and a * machine['A Y+'] + b * machine['B Y+'] == machine['Prize Y']:
                    if nb_tokens == 0:
                        nb_tokens = a * 3 + b
                    else:
                        nb_tokens = min(a * 3 + b, nb_tokens)
        
        if nb_tokens > 0:
            needed_tokens += nb_tokens
            nb_prizes += 1
            
    return nb_prizes, needed_tokens
            
                
print("part 1:")
print(count_needed_tokens('day13/sample'))
print(count_needed_tokens('day13/input'))
