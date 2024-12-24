# import logging
from astar import Maze

def load(filename: str):
    coords = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            data = line.strip().split(',')
            coords.append({'x': int(data[0]), 'y': int(data[1])})
    return coords

def build_maze(filename: str, size: int, steps) -> list[list[str]]:
    coords = load(filename)
    
    maze = []
    for _ in range(0, size):
        maze.append(['_'] * size)
    
    for n in range(0, steps):
        maze[coords[n]['y']][coords[n]['x']] = '#'
    
    return maze

def solve_maze(grid: list[list[str]], logger=None) -> int:
    maze = Maze(grid, logger=logger)
    logger and logger.info(str(maze))
    maze.solve(start=(0, 0), end=(len(grid) - 1, len(grid) - 1))
    logger and logger.info(str(maze))
    return maze.walkthrough.g

# logger = logging.getLogger("day18")
# logging.basicConfig(filename="day18.log", encoding="utf-8", level=logging.DEBUG)

print("first step:")
print(solve_maze(build_maze('day18/sample', 7, 12)))
print(solve_maze(build_maze('day18/input', 71, 1024)))
