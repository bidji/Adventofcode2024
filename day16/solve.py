# import logging
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
    return grid, (endy, endx), (starty, startx)

def solve_maze(filename: str):
    grid, end, start = load(filename)
    
    maze = Maze(grid=grid).solve(start=start, end=end)
    
    node = maze.walkthrough
    nb_nodes = 0
    while node:
        node = node.parent
        nb_nodes += 1
    return maze.walkthrough.g

# logger = logging.getLogger("day16")
# logging.basicConfig(filename="day16.log", encoding="utf-8", level=logging.DEBUG)

print("first part:")
print(solve_maze('day16/sample1'))
print(solve_maze('day16/sample2'))
print(solve_maze('day16/input'))