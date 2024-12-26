import logging
from astar import Maze

def load(filename: str) -> list[list[str]]:
    grid = []
    starty, startx = 0, 0
    endy, endx = 0, 0
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            if 'S' in line:
                starty, startx = len(grid), line.find('S')
            if 'E' in line:
                endy, endx = len(grid), line.find('E')
            grid.append([cell for cell in line.strip()])
    return grid, (endx, endy), (startx, starty)

def solve_maze(filename: str, logger: logging.Logger=None):
    grid, end, start = load(filename)
    
    maze = Maze(grid=grid, logger=logger).solve(start=start, end=end)
    
    return maze.walkthrough.g

def findall_solutions(filename: str, logger: logging.Logger=None):
    grid, end, start = load(filename)
    
    maze = Maze(grid=grid, logger=logger).solve(start=start, end=end, findall=True)
    
    # logger.debug(f"walkthroughs:{' '.join([str(node) for node in maze.walkthroughs])}")
    logger.debug(str(maze))
    
    nodes = []
    for node in maze.walkthroughs:
        current = node
        while current:
            pos = (current.x, current.y)
            if pos not in nodes:
                nodes.append(pos)
            current = current.parent
    return len(nodes)

logger = logging.getLogger("day16")
logging.basicConfig(filename="day16.log", encoding="utf-8", level=logging.DEBUG)

print("first part:")
print(solve_maze('day16/sample1'))
print(solve_maze('day16/sample2'))
print(solve_maze('day16/input'))

print("second part:")
print(findall_solutions('day16/sample1', logger))
# print(findall_solutions('day16/sample2'))
# print(findall_solutions('day16/input'))

