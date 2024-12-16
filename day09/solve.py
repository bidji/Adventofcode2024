def load(filename: str):
    blocks = []
    files = dict()
    empties = []
    
    with open(filename, 'r') as filedata:
        diskmap = filedata.read().strip()
        for id in range(0, int(len(diskmap) / 2) + 1):
            files[id] = {'start': len(blocks), 'size': int(diskmap[id * 2])}
            blocks.extend([str(id)] * int(diskmap[id * 2]))
            if id * 2 + 1 < len(diskmap):
                empties.append({'start': len(blocks), 'size': int(diskmap[id * 2 + 1])})
                blocks.extend(['.'] * int(diskmap[id * 2 + 1]))
                
    return blocks, files, empties
            
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

def move_files(blocks: str, files, empties):
    # starting by last file, first file never move
    for id in range(len(files) - 1, 0, -1):
        for empty in empties:
            if files[id]['start'] < empty['start']:
                # gone too far, stop searching
                break
            if empty['size'] >= files[id]['size']:
                # found a suitable empty space
                # moving file in blocks
                for n in range(0, files[id]['size']):
                    pos_empty = empty['start'] + n
                    pos_block = files[id]['start'] + n
                    blocks[pos_empty], blocks[pos_block] = blocks[pos_block], blocks[pos_empty]
                # adjusting empty space used
                if empty['size'] == files[id]['size']:
                    empties.remove(empty)
                else:
                    empty['start'] = empty['start'] + files[id]['size']
                    empty['size'] -= files[id]['size']
                # add new empty space or increasing empty space just before file moved
                contiguous_empty = False
                for e in empties:
                    if e['start'] + e['size'] + 1 == files[id]['start']:
                        contiguous_empty = True
                        e['size'] += files[id]['size']
                        break
                if not contiguous_empty:
                    empties.append({'start': files[id]['start'], 'size': files[id]['size']})
                # going to next file
                break
    return blocks

def checksum(filename: str, whole_files: bool):
    blocks, files, empties = load(filename)
    if whole_files:
        blocks = move_files(blocks, files, empties)
    else:
        blocks = move_blocks(blocks)
    checksum = 0
    for n in range(0, len(blocks)):
        if blocks[n] == '.':
            continue
        checksum += n * int(blocks[n])
    return checksum
        
print("first part:")
print(checksum('day09/sample2', whole_files=False))
print(checksum('day09/input', whole_files=False))

print("second part:")
print(checksum('day09/sample2', whole_files=True))
print(checksum('day09/input', whole_files=True))