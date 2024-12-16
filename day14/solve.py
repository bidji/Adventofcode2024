def load(filename: str):
    robots = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            data = line.strip().split(' ')
            position = data[0].replace('p=', '').split(',')
            velocity = data[1].replace('v=', '').split(',')
            robots.append({'x': int(position[0]), 'y': int(position[1]), 'vx': int(velocity[0]), 'vy': int(velocity[1])})
    return robots

def move(robot, width: int, height: int, steps: int) -> tuple[int, int]:
    """return new position of given robot"""
    x = (robot['x'] + steps * robot['vx']) % width
    y = (robot['y'] + steps * robot['vy']) % height
    return x, y

def robots_by_quadrant(filename: str, width: int, height: int, steps: int):
    robots = load(filename)
    
    # initialise grid
    grid = []
    for _ in range(0, height):
        grid.append([0] * width)
        
    # place robots at last step on grid
    for robot in robots:
        x, y = move(robot, width=width, height=height, steps=steps)
        grid[y][x] += 1
        
    # first quadrant
    first = 0
    for j in range(0, int(height / 2)):
        first += sum(grid[j][0:int(width/2)])
    
    # second quadrant
    second = 0
    for j in range(0, int(height / 2)):
        second += sum(grid[j][int(width/2)+1:])
    
    # third quadrant
    third = 0
    for j in range(int(height / 2)+1, height):
        third += sum(grid[j][0:int(width/2)])
    
    # fourth quadrant
    fourth = 0
    for j in range(int(height / 2)+1, height):
        fourth += sum(grid[j][int(width/2)+1:])
    
    return first * second * third * fourth


print("part 1:")
print(robots_by_quadrant('day14/sample', width=11, height=7, steps=100))
print(robots_by_quadrant('day14/input', width=101, height=103, steps=100))