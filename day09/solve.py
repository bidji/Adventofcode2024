import math
import re

def load(filename: str):
    blocks = []
    
    with open(filename, 'r') as filedata:
        diskmap = filedata.read().strip()
        for id in range(0, math.ceil(len(diskmap) / 2)):
            blocks.extend([str(id)] * int(diskmap[id * 2]))
            if id * 2 + 1 < len(diskmap):
                blocks.extend(['.'] * int(diskmap[id * 2 + 1]))
                
    return blocks
            
def move_blocks(blocks: str):
    nb_empty = blocks.count('.')
    suffix = ['.'] * nb_empty

    while not blocks[-nb_empty:] == suffix:
        first_empty = -1
        for n in range(0, len(blocks)):
            if blocks[n] == '.':
                first_empty = n
                break
        last_used = -1
        for n in range(len(blocks) - 1, 0, -1):
            if blocks[n] != '.':
                last_used = n
                break
        blocks[first_empty], blocks[last_used] = blocks[last_used], blocks[first_empty]
    
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
print(checksum('day09/input'))