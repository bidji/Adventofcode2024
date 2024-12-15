def check_safe(report: list[int]) -> int:
    """return 1 if this level is safe, else 0"""
    previous = report[0]
    direction = report[1] - previous
    for value in report[1:]:
        gap = value - previous
        if abs(gap) < 1 or abs(gap) > 3:
            return 0
        if gap * direction < 0:
            return 0
        previous = value
    return 1

def check_safe_with_dampener(report: list[int]) -> int:
    # print(f"Is report {report} safe ?")
    if check_safe(report) == 1:
        # print(f"{report} safe (without removing any level)")
        return 1
    if check_safe(report[1:]) == 1:
        # print(f"{report[1:]} safe (removing level {report[0]})")
        return 1
    for num in range(1, len(report) - 1):
        dampened_report = report[0:num]
        dampened_report.extend(report[num+1:])
        if check_safe(dampened_report) == 1:
            # print(f"{dampened_report} safe (removing level {report[num]})")
            return 1
    if check_safe(report[:-1]) == 1:
        # print(f"{report[:-1]} safe (removing level {report[-1]})")
        return 1
    # print("not safe")
    return 0

def get_safes(filename: str):
    nb_safes = 0
    with open(filename, 'r') as data:
        for line in data.readlines():
            nb_safes += check_safe([int(x) for x in line.strip().split(' ')])
    return nb_safes

def get_safes_with_dampener(filename: str):
    nb_safes = 0
    with open(filename, 'r') as data:
        for line in data.readlines():
            nb_safes += check_safe_with_dampener([int(x) for x in line.strip().split(' ')])
    return nb_safes             

print("first part:")
print(get_safes('day02/sample'))
print(get_safes('day02/input'))

print("second part:")
print(get_safes_with_dampener('day02/sample'))
print(get_safes_with_dampener('day02/input'))
