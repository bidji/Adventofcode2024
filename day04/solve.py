def read_data(filename: str) -> list[str]:
    data = []
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            data.append(line.strip())
    return data

def find_in_direction(data: list[str], j: int, i: int, j_direction: int, i_direction: int) -> int:
    if j_direction == -1 and j < 3:
        return 0
    if j_direction == 1 and j > len(data) - 4:
        return 0
    if i_direction == -1 and i < 3:
        return 0
    if i_direction == 1 and i > len(data[j]) - 4:
        return 0
    if data[j + 1 * j_direction][i + 1 * i_direction] == 'M' \
        and data[j + 2 * j_direction][i + 2 * i_direction] == 'A' \
        and data[j + 3 * j_direction][i + 3 * i_direction] == 'S':
        return 1
    return 0

def check_x_mas(data: list[str], j: int, i: int) -> int:
    if j == 0 or j == len(data) - 1 or i == 0 or i == len(data[j]) - 1:
        return 0
    diags = [data[j-1][i-1], data[j-1][i+1], data[j+1][i+1], data[j+1][i-1]]
    if diags.count('M') != 2 or diags.count('S') != 2:
        return 0
    if diags == ['M', 'S', 'M', 'S'] or diags == ['S', 'M', 'S', 'M']:
        return 0
    return 1

def find_xmas(filename: str) -> int:
    data = read_data(filename)
    finds = 0
    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            if data[j][i] != 'X':
                continue
            finds += find_in_direction(data, j, i, 0, 1)
            finds += find_in_direction(data, j, i, 1, 1)
            finds += find_in_direction(data, j, i, 1, 0)
            finds += find_in_direction(data, j, i, 1, -1)
            finds += find_in_direction(data, j, i, 0, -1)
            finds += find_in_direction(data, j, i, -1, -1)
            finds += find_in_direction(data, j, i, -1, 0)
            finds += find_in_direction(data, j, i, -1, 1)
    return finds

def find_x_mas(filename: str) -> int:
    data = read_data(filename)
    finds = 0
    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            if data[j][i] != 'A':
                continue
            finds += check_x_mas(data, j, i)
    return finds

print("first part:")
print(find_xmas('day04/sample'))
print(find_xmas('day04/input'))

print("second part:")
print(find_x_mas('day04/sample'))
print(find_x_mas('day04/input'))