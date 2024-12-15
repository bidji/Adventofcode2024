def get_rules_and_updates(filename: str):
    rules = dict()
    inv_rules = dict()
    updates = []
    with open(filename, 'r') as datafile:
        for line in datafile.readlines():
            if '|' in line:
                # dealing with rules
                data = line.strip().split('|')
                if data[0] in rules:
                    rules[data[0]].append(data[1])
                else:
                    rules[data[0]] = [data[1]]
                if data[1] in inv_rules:
                    inv_rules[data[1]].append(data[0])
                else:
                    inv_rules[data[1]] = [data[0]]
            if ',' in line:
                # dealing with reports
                updates.append(line.strip().split(','))
    return rules, updates

def check_update(update, rules):
    for num in range(1, len(update)):
        if update[num] in rules:
            for rule in rules[update[num]]:
                if rule in update[0:num]:
                    return False
    return True

def fix_update(update, rules):
    for num in range(1, len(update)):
        if update[num] in rules:
            for rule in rules[update[num]]:
                if rule in update[0:num]:
                    pos = update[0:num].index(rule)
                    update[pos], update[num] = update[num], update[pos]
                    return

def find_right_ordered_updates(filename: str):
    rules, updates = get_rules_and_updates(filename)
    result = 0
    for update in updates:
        if check_update(update, rules):
            result += int(update[int(len(update)/2)])
    return result

def fix_wrong_ordered_updates(filename: str):
    rules, updates = get_rules_and_updates(filename)
    result = 0
    for update in updates:
        if not check_update(update, rules):
            while not check_update(update, rules):
                fix_update(update, rules)
            result += int(update[int(len(update)/2)])
    return result

print("first part:")
print(find_right_ordered_updates('day05/sample'))
print(find_right_ordered_updates('day05/input'))

print("second part:")
print(fix_wrong_ordered_updates('day05/sample'))
print(fix_wrong_ordered_updates('day05/input'))
