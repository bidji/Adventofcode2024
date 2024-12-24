# import logging
from astar import Maze, MazeException

def load(filename: str) -> list[dict[str, int]]:
    coords = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            data = line.strip().split(',')
            coords.append({'x': int(data[0]), 'y': int(data[1])})
    return coords

def build_maze(coords: list[dict[str, int]], size: int, steps: int) -> list[list[str]]:
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

def search_impossible_maze(filename: str, size: str, steps: int):
    coords = load(filename)
    
    nb_steps = steps
    try:
        while nb_steps < len(coords):
            print(f"nb steps: {nb_steps}")
            Maze(build_maze(coords, size, nb_steps)).solve(start=(0, 0), end=(size - 1, size - 1))
            nb_steps += 1
    except MazeException:
        return coords[nb_steps - 1]

# logger = logging.getLogger("day18")
# logging.basicConfig(filename="day18.log", encoding="utf-8", level=logging.DEBUG)

print("first part:")
print(solve_maze(build_maze(load('day18/sample'), 7, 12)))
print(solve_maze(build_maze(load('day18/input'), 71, 1024)))

print("second part:")
print(search_impossible_maze('day18/sample', 7, 12))
print(search_impossible_maze('day18/input', 71, 2500))
