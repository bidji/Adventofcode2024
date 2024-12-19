def load(filename: str):
    grid = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            grid.append(line.strip())
    return grid

def get_regions(grid):
    # regions initialisation
    regions = []
    for row in grid:
        regions.append([0] * len(row))
    
    num_region = 1
    for j in range(0, len(grid)):
        for i in range(0, len(grid[j])):
            if j > 0 and grid[j][i] == grid[j-1][i]:
                regions[j][i] = regions[j-1][i]
            elif i > 0 and grid[j][i] == grid[j][i-1]:
                regions[j][i] = regions[j][i-1]
            else:
                regions[j][i] = num_region
                num_region += 1
            
    areas = dict()
    for row in regions:
        for plot in set(row):
            if plot in areas:
                areas[plot] = areas[plot] + row.count(plot)
            else:
                areas[plot] = row.count(plot)
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
    regions, areas = get_regions(grid)
    display(regions, areas)
    
    # sum prices
    prices = 0
    for j in range(0, len(grid)):
        row_prices = []
        for i in range(0, len(grid[j])):
            row_prices.append(get_price(regions, areas, j, i))
        print(" ".join([str(p).zfill(2) for p in row_prices]))
        prices += sum(row_prices)
    return prices

print("first part:")
print(get_prices('day12/sample1'))
print(get_prices('day12/sample2'))
print(get_prices('day12/sample3'))