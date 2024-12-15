import re

def first(filename: str) -> int:
    pattern_mul = re.compile('mul\([0-9]{1,3},[0-9]{1,3}\)')
    pattern_digits = re.compile('[0-9]{1,3}')
    result = 0
    with open(filename, 'r') as data:
        for line in data.readlines():
            for find in pattern_mul.findall(line.strip()):
                values = pattern_digits.findall(find)
                result += int(values[0]) * int(values[1])
    return result

def second(filename: str) -> int:
    pattern_mul = re.compile("mul\([0-9]{1,3},[0-9]{1,3}\)")
    pattern_do = re.compile("do\(\)")
    pattern_dont = re.compile("don't\(\)")
    full_pattern = re.compile("mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)")
    pattern_digits = re.compile('[0-9]{1,3}')
    result = 0
    multiply = True
    with open(filename, 'r') as data:
        for line in data.readlines():
            for find in full_pattern.findall(line.strip()):
                # print(find)
                if pattern_do.match(find):
                    # print("do")
                    multiply = True
                    continue
                if pattern_dont.match(find):
                    # print("dont")
                    multiply = False
                    continue
                if multiply:
                    values = pattern_digits.findall(find)
                    # print(f" add multiply {values[0]} * {values[1]} = {int(values[0]) * int(values[1])}")
                    result += int(values[0]) * int(values[1])
    return result

print("first part:")            
print(first('day03/sample1'))
print(first('day03/input'))

print("second part:")
print(second('day03/sample2'))
print(second('day03/input'))