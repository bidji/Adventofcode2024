def load(filename: str):
    grid = []
    trail_heads = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            grid.append([])
            for num in line.strip():
                grid[-1].append(int(num))
                if int(num) == 0:
                    trail_heads.append({'y': len(grid) - 1, 'x': len(grid[-1]) - 1})
    return grid, trail_heads

def find_reachable_summits(grid, y: int, x: int):
    height = grid[y][x]
    if height == 9:
        # summit reached
        return [f"{y}/{x}"]
    else:
        summits = []
        if y-1 >= 0 and grid[y-1][x] == height+1:
            # going north
            summits.extend(find_reachable_summits(grid, y-1, x))
        if x+1 < len(grid[y]) and grid[y][x+1] == height+1:
            # going east
            summits.extend(find_reachable_summits(grid, y, x+1))
        if y+1 < len(grid) and grid[y+1][x] == height+1:
            # going south
            summits.extend(find_reachable_summits(grid, y+1, x))
        if x-1 >= 0 and grid[y][x-1] == height+1:
            # going west
            summits.extend(find_reachable_summits(grid, y, x-1))
        return summits

def sum_scores(filename: str) -> int:
    grid, trail_heads = load(filename)
    score = 0
    for head in trail_heads:
        score += len(set(find_reachable_summits(grid, head['y'], head['x'])))
    return score
                
print("first part:")
print(sum_scores('day10/sample'))
print(sum_scores('day10/input'))