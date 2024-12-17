def load(filename: str):
    grid = []
    movements = ""
    startx, starty = 0, 0
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            if len(line.strip()) == 0:
                continue
            if line.startswith("#"):
                if '@' in line:
                    starty = len(grid)
                    startx = line.find('@')
                grid.append([])
                for char in line.strip():
                    grid[-1].append(char)
            else:
                movements += line.strip()
    return grid, movements, startx, starty

def get_direction(movement: str):
    match movement:
        case '<':
            return -1, 0
        case '^':
            return 0, -1
        case '>':
            return 1, 0
        case 'v':
            return 0, 1
        
def push_box(grid, x: int, y: int, directionx: int, directiony: int) -> bool:
    nextx = x + directionx
    nexty = y + directiony
    if grid[nexty][nextx] == '#':
        # no push
        return False
    if grid[nexty][nextx] == '.':
        # push
        grid[y][x], grid[nexty][nextx] = grid[nexty][nextx], grid[y][x]
        return True
    if grid[nexty][nextx] == 'O':
        # box, trying to push it
        if push_box(grid, nextx, nexty, directionx, directiony):
            grid[y][x], grid[nexty][nextx] = grid[nexty][nextx], grid[y][x]
            return True
        else:
            return False

def move_robot(grid, startx: int, starty: int, directionx: int, directiony: int) -> tuple[int, int]:
    robotx, roboty = startx, starty
    nextx = robotx + directionx
    nexty = roboty + directiony
    
    if grid[nexty][nextx] == '#':
        # a wall, no move
        return robotx, roboty
    if grid[nexty][nextx] == '.':
        # empty place, just move
        grid[roboty][robotx], grid[nexty][nextx] = grid[nexty][nextx], grid[roboty][robotx]
        return nextx, nexty
    if grid[nexty][nextx] == 'O':
        # a box, trying to push it
        if push_box(grid, nextx, nexty, directionx, directiony):
            # box pushed, take its position
            grid[roboty][robotx], grid[nexty][nextx] = grid[nexty][nextx], grid[roboty][robotx]
            return nextx, nexty
        else:
            # box stuck, no move
            return robotx, roboty

def sum_gps(filename: str):
    grid, movements, robotx, roboty = load(filename)
    
    # print("initial state")
    # display(grid)
    
    # move robot
    for n in range(0, len(movements)):
        dx, dy = get_direction(movements[n])
        robotx, roboty = move_robot(grid, robotx, roboty, dx, dy)
        # print(f"after movement {movements[n]}")
        # display(grid)
    
    # sum gps
    gps = 0
    for j in range(0, len(grid)):
        for i in range(0, len(grid[j])):
            if grid[j][i] == 'O':
                gps += 100 * j + i
    return gps

def display(grid):
    for j in range(0, len(grid)):
        row = ""
        for i in range(0, len(grid[j])):
            row += grid[j][i]
        print(row)

print("part 1:")
print(sum_gps('day15/sample1'))
print(sum_gps('day15/sample2'))
print(sum_gps('day15/input'))