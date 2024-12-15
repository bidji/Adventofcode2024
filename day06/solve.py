from enum import IntFlag, auto

class Move(IntFlag):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    
    def turn(self):
        match self:
            case Move.UP:
                return Move.RIGHT
            case Move.RIGHT:
                return Move.DOWN
            case Move.DOWN:
                return Move.LEFT
            case Move.LEFT:
                return Move.UP

directions = [{'y': -1, 'x': 0}, {'y': 0, 'x': 1}, {'y': 1, 'x': 0}, {'y': 0, 'x': -1}]

def load_grid_and_start(filename: str) -> tuple[list[str], list[list[Move]], int, int]:
    grid = []
    starty, startx = 0, 0
    guard_found = False
    moves = []
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            grid.append(line.strip())
            moves.append([])
            for x in range(0, len(line.strip())):
                moves[-1].append(0)
            if not guard_found:
                if '^' in line:
                    startx = line.index('^')
                    grid[starty] = grid[starty][:startx] + 'X' + grid[starty][startx+1:]
                    moves[starty][startx] = Move.UP
                    guard_found = True
                else:
                    starty += 1
    return grid, moves, starty, startx

def find_distinct_positions(filename: str) -> int:
    grid, _, guardy, guardx = load_grid_and_start(filename)
    direction = 0
    nb = 1
    while True:
        # try to move it
        nexty = guardy + directions[direction]['y']
        nextx = guardx + directions[direction]['x']
        if nexty < 0 or nexty >= len(grid) or nextx < 0 or nextx >= len(grid[0]):
            # guard outbounds after this move
            break
        next = grid[nexty][nextx]
        match next:
            case '#':
                # a wall, next direction or first direction if already last direction
                # and no move
                direction = (direction + 1) % len(directions)
            case '.':
                # a new position, add it and move
                nb += 1
                grid[nexty] = grid[nexty][:nextx] + 'X' + grid[nexty][nextx+1:]
                guardy, guardx = nexty, nextx
            case 'X':
                # already known position, just move
                guardy, guardx = nexty, nextx
    return nb

def copy_moves(original_moves):
    new_moves = []
    for raw in original_moves:
        new_moves.append(raw.copy())
    return new_moves

def is_loop(grid, moves, starty: int, startx: int, wally: int, wallx: int):
    new_moves = copy_moves(moves)
    while True:
        # try to move
        break

def find_loops(filename: str) -> int:
    grid, moves, guardy, guardx = load_grid_and_start(filename)
    direction = 0
    move = Move.UP
    nb = 0
    while True:
        # try to move it
        nexty = guardy + directions[direction]['y']
        nextx = guardx + directions[direction]['x']
        if nexty < 0 or nexty >= len(grid) or nextx < 0 or nextx >= len(grid[0]):
            # guard outbounds after this move
            break
        next = grid[nexty][nextx]
        match next:
            case '#':
                # a wall, next direction or first direction if already last direction
                # no move and no search for a loop with a new wall
                # we add a new direction in moves
                direction = (direction + 1) % len(directions)
                moves[guardy][guardx] = moves[guardy][guardx] | moves[guardy][guardx].turn()
            case '.':
                # a new position, add it and move
                nb += 1
                grid[nexty] = grid[nexty][:nextx] + 'X' + grid[nexty][nextx+1:]
                guardy, guardx = nexty, nextx
            case 'X':
                # already known position, just move
                guardy, guardx = nexty, nextx
    return nb
            
print("first part:")
print(find_distinct_positions('day06/sample'))
print(find_distinct_positions('day06/input'))

print("second part:")
#print(find_loops('day06/sample'))