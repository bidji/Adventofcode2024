def load(filename: str) -> list[dict]:
    data = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            parts = line.strip().split(':')
            data.append({'result': int(parts[0]), 'values': [int(x) for x in parts[1].strip().split(' ')]})
    return data

def first_total_calibration(filename: str):
    data = load(filename)
    calibration = 0
    
    for line in data:
        result, values = line['result'], line['values']
        totals = [values[0]]
        for value in values[1:]:
            new_totals = []
            for total in totals:
                new_totals.append(total + value)
                new_totals.append(total * value)
            totals = new_totals
        if result in totals:
            calibration += result
        
    return calibration

def second_total_calibration(filename: str):
    data = load(filename)
    calibration = 0
    
    for line in data:
        result, values = line['result'], line['values']
        totals = [values[0]]
        for value in values[1:]:
            new_totals = []
            for total in totals:
                new_totals.append(total + value)
                new_totals.append(total * value)
                new_totals.append(int(str(total) + str(value)))
            totals = new_totals
        if result in totals:
            calibration += result
        
    return calibration
            
print("first part:")
print(first_total_calibration('day07/sample'))
print(first_total_calibration('day07/input'))

print("second part:")
print(second_total_calibration('day07/sample'))
print(second_total_calibration('day07/input'))