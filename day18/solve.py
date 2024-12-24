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

def search_impossible_maze(filename: str, size: str):
    coords = load(filename)
    
    # starting by the maximum steps as most constrained mazes are faster to solve
    nb_steps = len(coords)
    while True:
        try:
            Maze(build_maze(coords, size, nb_steps)).solve(start=(0, 0), end=(size - 1, size - 1))
            # no exception raised, we found the last solvable maze
            return coords[nb_steps]
        except MazeException:
            nb_steps -= 1

# logger = logging.getLogger("day18")
# logging.basicConfig(filename="day18.log", encoding="utf-8", level=logging.DEBUG)

print("first part:")
print(solve_maze(build_maze(load('day18/sample'), 7, 12)))
print(solve_maze(build_maze(load('day18/input'), 71, 1024)))

print("second part:")
print(search_impossible_maze('day18/sample', 7))
print(search_impossible_maze('day18/input', 71))
