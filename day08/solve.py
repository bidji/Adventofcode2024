import re
def load_map(filename: str, with_harmonics: bool):
    grid = []
    frequencies = dict()
    pattern = re.compile('[^.]')
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            grid.append([0 for i in range(0, len(line.strip()))])
            for frequency in pattern.findall(line.strip()):
                antennas = [{'y': len(grid) - 1, 'x': occurence.start()} for occurence in re.finditer(frequency, line.strip())]
                if with_harmonics:
                    for antenna in antennas:
                        grid[antenna['y']][antenna['x']] = 1
                if frequency in frequencies:
                    frequencies[frequency].extend(antennas)
                else:
                    frequencies[frequency] = antennas
    return grid, frequencies

def get_antinodes(grid, antenna_a, antenna_b):
    diffy = antenna_a['y'] - antenna_b['y']
    diffx = antenna_a['x'] - antenna_b['x']
    
    ay = antenna_a['y'] + diffy
    ax = antenna_a['x'] + diffx
    if ay >= 0 and ay < len(grid) and ax >= 0 and ax < len(grid[0]):
        grid[ay][ax] = 1
    by = antenna_b['y'] - diffy
    bx = antenna_b['x'] - diffx
    if by >= 0 and by < len(grid) and bx >= 0 and bx < len(grid[0]):
        grid[by][bx] = 1
        
def get_antinodes_with_harmonics(grid, antenna_a, antenna_b):
    diffy = antenna_a['y'] - antenna_b['y']
    diffx = antenna_a['x'] - antenna_b['x']
    
    ay = antenna_a['y'] + diffy
    ax = antenna_a['x'] + diffx
    while ay >= 0 and ay < len(grid) and ax >= 0 and ax < len(grid[0]):
        grid[ay][ax] = 1
        ay += diffy
        ax += diffx
        
    by = antenna_b['y'] - diffy
    bx = antenna_b['x'] - diffx
    while by >= 0 and by < len(grid) and bx >= 0 and bx < len(grid[0]):
        grid[by][bx] = 1
        by -= diffy
        bx -= diffx

def get_nb_antinodes(filename, with_harmonics: bool):
    grid, frequencies = load_map(filename, with_harmonics)
    
    for frequency in frequencies:
        antennas = frequencies[frequency]
        if len(antennas) > 1:
            # at least 2 antennas, we have to search for antinodes
            for a in range(0, len(antennas) - 1):
                for b in range(a + 1, len(antennas)):
                    if with_harmonics:
                        get_antinodes_with_harmonics(grid, antennas[a], antennas[b])
                    else:
                        get_antinodes(grid, antennas[a], antennas[b])
    
    nb_antinodes = 0
    for line in grid:
        nb_antinodes += line.count(1)
    return nb_antinodes

print("first part:")
print(get_nb_antinodes('day08/sample', with_harmonics=False))
print(get_nb_antinodes('day08/input', with_harmonics=False))

print("second part:")
print(get_nb_antinodes('day08/sample', with_harmonics=True))
print(get_nb_antinodes('day08/input', with_harmonics=True))