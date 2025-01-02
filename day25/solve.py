import logging
from typing import Self

class KeyLock:
    schema: list[str]
    heights: list[int]
    
    def __init__(self, schema: list[str]):
        self.schema = schema
        self.heights = []
        for i in range(0, len(schema[0])):
            self.heights.append([line[i] for line in self.schema].count('#'))
        
    def __str__(self):
        return str(self.heights) + '\n' + '\n'.join(self.schema)
    
    def __eq__(self, other: Self):
        return self.heights == other.heights
    
    def __hash__(self):
        value = 0
        width = len(self.heights)
        for i in range(0, width):
            value += self.heights[i] * (10 ** (width - i - 1))
        return hash(value)
    
    def overlap(self, other: Self) -> bool:
        if len(self.heights) != len(other.heights):
            return True
        for i in range(0, len(self.heights)):
            if self.heights[i] + other.heights[i] > 5:
                return True
        return False
    

def load(filename: str) -> tuple[list[KeyLock], list[KeyLock]]:
    locks: list[KeyLock] = []
    keys: list[KeyLock] = []
    
    with open(filename, 'r') as filedata:
        lines = filedata.readlines()
        ptr = 0
        while ptr < len(lines):
            schema = []
            for line in lines[ptr + 1:ptr + 6]:
                schema.append(line.strip())
            if lines[ptr + 0].strip() == '#' * len(lines[ptr + 0].strip()):
                locks.append(KeyLock(schema))
            if lines[ptr + 0].strip() == '.' * len(lines[ptr + 0].strip()):
                keys.append(KeyLock(schema))
            ptr += 8

    return set(locks), set(keys)
    
def count_pairs(filename: str) -> int:
    locks, keys = load(filename)
    
    pairs = 0
    for lock in locks:
        for key in keys:
            if not key.overlap(lock):
                pairs += 1
    
    return pairs

print("first part:")
print(count_pairs('day25/sample'))
print(count_pairs('day25/input'))