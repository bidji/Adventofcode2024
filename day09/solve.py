import math
import re

def load(filename: str):
    blocks = ""
    
    with open(filename, 'r') as filedata:
        diskmap = filedata.read().strip()
        for id in range(0, math.ceil(len(diskmap) / 2)):
            blocks += str(id) * int(diskmap[id * 2])
            if id * 2 + 1 < len(diskmap):
                blocks += '.' * int(diskmap[id * 2 + 1])
                
    return blocks
            
def move_blocks(blocks: str):
    suffix = '.' * blocks.count('.')

    while not blocks.endswith(suffix):
        first_empty = blocks.find('.')
        for n in range(len(blocks) - 1, 0, -1):
            if blocks[n] != '.':
                blocks = blocks[0:first_empty] + blocks[n] + blocks[first_empty+1:n] + '.' + blocks[n+1:]
                break
    
    return blocks

def checksum(filename: str):
    blocks = move_blocks(load(filename))
    checksum = 0
    for n in range(0, len(blocks)):
        if blocks[n] == '.':
            break
        checksum += n * int(blocks[n])
    return checksum
        
print("first part:")
print(checksum('day09/sample2'))
#print(checksum('day09/input'))