import logging
from astar import Maze, Node

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

def find_currents_and_nexts(grid: list[list[str]], holex: int, holey: int):
    currents_and_nexts = []
    # starting from up
    if holey > 0 and grid[holey - 1][holex] != '#' and holey < len(grid) - 1 and grid[holey+1][holex] != '#':
            currents_and_nexts.append({'currentx': holex, 'currenty': holey - 1, 'nextx': holex, 'nexty': holey+1})
    # starting from right
    if holex < len(grid[holey]) - 1 and grid[holey][holex+1] != '#' and holex > 1 and grid[holey][holex-1] != '#':
            currents_and_nexts.append({'currentx': holex+1, 'currenty': holey, 'nextx': holex-1, 'nexty': holey})
    # starting from down
    if holey < len(grid) - 1 and grid[holey+1][holex] != '#' and holey > 0 and grid[holey - 1][holex] != '#':
            currents_and_nexts.append({'currentx': holex, 'currenty': holey+1, 'nextx': holex, 'nexty': holey-1})
    # starting from left
    if holex > 1 and grid[holey][holex-1] != '#' and holex < len(grid[holey]) - 1 and grid[holey][holex+1] != '#':
            currents_and_nexts.append({'currentx': holex-1, 'currenty': holey, 'nextx': holex+1, 'nexty': holey})
    return currents_and_nexts

def find_saving(walkthrough: Node, currentx: int, currenty: int, nextx: int, nexty: int) -> int:
    node = walkthrough
    current_node = next_node = None
    while node:
        if node.x == nextx and node.y == nexty:
            next_node = node
        if node.x == currentx and node.y == currenty:
            if not next_node:
                # we don't want to get back
                return 0
            current_node = node
        node = node.parent
    if current_node and next_node:
        return next_node.g - current_node.g
    return 0

def find_valuable_cheats(filename: str, logger: logging.Logger, threshold: int) -> int:
    grid, end, start = load(filename)
    
    maze = Maze(grid=grid, logger=logger).solve(start=start, end=end)
    logger.info(str(maze))
    
    cheats = dict()
    for j in range(1, len(grid) - 1):
        for i in range(1, len(grid[j]) - 1):
            if grid[j][i] == '#':
                for elem in find_currents_and_nexts(grid, i, j):
                    saving = find_saving(maze.walkthrough,
                                         elem['currentx'], elem['currenty'],
                                         elem['nextx'], elem['nexty'])
                    logger.debug(f"hole: {j}/{i} current: {elem['currenty']}/{elem['currentx']} next: {elem['nexty']}/{elem['nextx']} -> saving: {saving}")
                    if saving > threshold:
                        if saving in cheats:
                            cheats[saving] += 1
                        else:
                            cheats[saving] = 1
    
    logger.info(f"cheats: {cheats}")
    nb = 0
    for saving in cheats:
        if saving > threshold:
            nb += cheats[saving]
    return nb

logger = logging.getLogger("day20")
logging.basicConfig(filename="day20.log", encoding="utf-8", level=logging.ERROR)

print("first part:")
print(find_valuable_cheats('day20/sample', logger, 0))
print(find_valuable_cheats('day20/input', logger, 100))