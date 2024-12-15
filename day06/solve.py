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

directions = {1: {'y': -1, 'x': 0}, 2: {'y': 0, 'x': 1}, 4: {'y': 1, 'x': 0}, 8: {'y': 0, 'x': -1}}

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
                    moves[starty][startx] = Move.UP
                    guard_found = True
                else:
                    starty += 1
    return grid, moves, starty, startx

def find_distinct_positions(filename: str) -> int:
    grid, _, guardy, guardx = load_grid_and_start(filename)
    grid[guardy] = grid[guardy][:guardx] + 'X' + grid[guardy][guardx+1:]
    direction = Move.UP
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
                # a wall, turn and no move
                direction = direction.turn()
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

def is_loop(grid, moves, guardy: int, guardx: int, direction: Move) -> bool:
    # inserting fake wall in front of guard
    wally = guardy + directions[direction]['y']
    wallx = guardx + directions[direction]['x']
    if wally < 0 or wally >= len(grid) or wallx < 0 or wallx >= len(grid[0]):
        return False
    if grid[wally][wallx] == '#':
        return False
    new_grid = grid.copy()
    new_grid[wally] = new_grid[wally][:wallx] + '#' + new_grid[wally][wallx+1:]
    new_moves = copy_moves(moves)
    direction = direction.turn()
    
    while True:
        # try to move
        nexty = guardy + directions[direction]['y']
        nextx = guardx + directions[direction]['x']
        if nexty < 0 or nexty >= len(grid) or nextx < 0 or nextx >= len(grid[0]):
            # guard outbounds after this move
            return False
        if direction & new_moves[nexty][nextx]:
            # guard on his tracks
            return True
        next = grid[nexty][nextx]
        match next:
            case '#':
                # a wall, turn
                direction = direction.turn()
                new_moves[guardy][guardx] = new_moves[guardy][guardx] | direction
            case '.':
                # not a wall, move
                new_moves[nexty][nextx] = new_moves[nexty][nextx] | direction
                guardy, guardx = nexty, nextx

def find_loops(filename: str) -> int:
    grid, moves, guardy, guardx = load_grid_and_start(filename)
    grid[guardy] = grid[guardy][:guardx] + '.' + grid[guardy][guardx+1:]
    direction = Move.UP
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
                # a wall, turn
                direction = direction.turn()
                moves[guardy][guardx] = moves[guardy][guardx] | direction
                # check if it's possible to create a loop with a wall in front of guard
                if is_loop(grid, moves, guardy, guardx, direction):
                    nb += 1
            case '.':
                # not a wall, move
                guardy, guardx = nexty, nextx
                moves[guardy][guardx] = moves[guardy][guardx] | direction
                # check if it's possible to create a loop with a wall in front of guard
                if is_loop(grid, moves, guardy, guardx, direction):
                    nb += 1
    return nb
            
print("first part:")
print(find_distinct_positions('day06/sample'))
print(find_distinct_positions('day06/input'))

print("second part:")
print(find_loops('day06/sample'))
print(find_loops('day06/input'))
