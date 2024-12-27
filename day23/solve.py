def load(filename: str) -> list[str]:
    connections = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            connections.append(line.strip())
    return connections

def find_connected(connections: list[str], computer: str) -> list[str]:
    connected = []
    for connection in connections:
        if computer in connection:
            connected.append(connection.replace(computer, '').replace('-', ''))
    return connected

def startswith(computers: list[str], prefix: str) -> bool:
    for computer in computers:
        if computer.startswith(prefix):
            return True
    return False

def connected(connections, computer1, computer2) -> bool:
    return f"{computer1}-{computer2}" in connections or f"{computer2}-{computer1}" in connections

def all_connected(connections: list[str], lan: set[str], computer: str) -> bool:
    for c in lan:
        if not connected(connections, c, computer):
            return False
    return True

def find_computers(filename: str, prefix: str) -> int:
    connections = load(filename)
    
    sets = set()
    for computer1, computer2 in [c.split('-') for c in connections]:
        for computer3 in find_connected(connections, computer1):
            if connected(connections, computer2, computer3):
                computers = [computer1, computer2, computer3]
                if startswith(computers, prefix):
                    computers.sort()
                    sets.add(",".join(computers))
        for computer3 in find_connected(connections, computer2):
            if connected(connections, computer1, computer3):
                computers = [computer1, computer2, computer3]
                if startswith(computers, prefix):
                    computers.sort()
                    sets.add(",".join(computers))
        
    return len(sets)

def find_lan_party(filename: str) -> str:
    connections = load(filename)

    networks = set()
    computers = [c.split('-') for c in connections]
    for n in range(0, len(computers) - 1):
        computer1, computer2 = computers[n]
        network = set([computer1, computer2])
        for computer3, computer4 in computers[n+1:]:
            if all_connected(connections, network, computer3):
                network.add(computer3)
            if all_connected(connections, network, computer4):
                network.add(computer4)
        lan = list(network)
        lan.sort()
        networks.add(','.join(lan))
    
    lans = list(networks)
    lans.sort(key=lambda l: len(l), reverse=True)
    return lans[0]

print("first part:")
print(find_computers('day23/sample', 't'))
print(find_computers('day23/input', 't'))

print("second part:")
print(find_lan_party('day23/sample'))
print(find_lan_party('day23/input'))