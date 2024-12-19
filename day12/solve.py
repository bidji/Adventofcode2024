def load(filename: str):
    grid = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            grid.append(line.strip())
    return grid


def next_region(areas: dict[int, int]) -> int:
    if len(areas) == 0:
        return 1
    else:
        return max(areas.keys()) + 1

def set_region(grid: list[list[int]], regions: list[list[int]],
               areas: dict[int, int], j: int, i: int):
    # check if region already set
    if regions[j][i] > 0:
        return
    
    plot = grid[j][i]
    
    # check if there is a plot connected with a region already set
    region = 0
    if j > 0 and grid[j-1][i] == plot and regions[j-1][i] > 0:
        region = regions[j-1][i]
    if i > 0 and grid[j][i-1] == plot and regions[j][i-1] > 0:
        region = regions[j][i-1]
    if j < len(grid) - 1 and grid[j+1][i] == plot and regions[j+1][i] > 0:
        region = regions[j+1][i]
    if i < len(grid[j]) - 1 and grid[j][i+1] == plot and regions[j][i+1] > 0:
        region = regions[j][i+1]
        
    if region > 0:
        areas[region] += 1
    else:
        region = next_region(areas)
        areas[region] = 1
    regions[j][i] = region
    
    # set region for connected plots without a region set
    if j > 0 and grid[j-1][i] == plot and regions[j-1][i] == 0:
        set_region(grid, regions, areas, j-1, i)
    if i > 0 and grid[j][i-1] == plot and regions[j][i-1] == 0:
        set_region(grid, regions, areas, j, i-1)
    if j < len(grid) - 1 and grid[j+1][i] == plot and regions[j+1][i] == 0:
        set_region(grid, regions, areas, j+1, i)
    if i < len(grid[j]) - 1 and grid[j][i+1] == plot and regions[j][i+1] == 0:
        set_region(grid, regions, areas, j, i+1)

def get_regions_areas(grid):
    # regions and mapped initialisation
    regions = []
    for row in grid:
        regions.append([0] * len(row))
    
    areas = dict()
    for j in range(0, len(grid)):
        for i in range(0, len(grid[j])):
            set_region(grid, regions, areas, j, i)
    
    return regions, areas

def get_price(regions, areas, j: int, i: int) -> int:
    price = 0
    area = areas[regions[j][i]]
    if j == 0 or regions[j][i] != regions[j-1][i]:
        price += 1 * area
    if i == 0 or regions[j][i] != regions[j][i-1]:
        price += 1 * area
    if j == len(regions)-1 or regions[j][i] != regions[j+1][i]:
        price += 1 * area
    if i == len(regions[j])-1 or regions[j][i] != regions[j][i+1]:
        price += 1 * area
    return price

def display(regions: list[list[int]], areas: dict):
    print("regions:")
    nb_regions = max(areas.keys())
    for row in regions:
        if nb_regions < 10:
            print("".join([str(p) for p in row]))
        else:
            print(" ".join([str(p).zfill(2) for p in row]))
    
    print("areas:")
    print(areas)
            
def get_prices(filename: str):
    grid = load(filename)
    
    # define regions in mapped
    regions, areas = get_regions_areas(grid)
    
    # sum prices
    prices = 0
    for j in range(0, len(grid)):
        row_prices = []
        for i in range(0, len(grid[j])):
            row_prices.append(get_price(regions, areas, j, i))
        # print(" ".join([str(p).zfill(2) for p in row_prices]))
        prices += sum(row_prices)
    return prices

print("first part:")
print(get_prices('day12/sample1'))
print(get_prices('day12/sample2'))
print(get_prices('day12/sample3'))
print(get_prices('day12/input'))