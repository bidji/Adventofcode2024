class MissingInput(Exception):
    pass


class Gate:
    wire1: str
    wire2: str
    gate: str
    name: str
    
    def __init__(self, wire1: str, gate: str, wire2: str, name: str):
        self.wire1 = wire1
        self.wire2 = wire2
        self.gate = gate
        self.name = name
        
    def __str__(self):
        return f"{self.wire1} {self.gate} {self.wire2} -> {self.name}"
    
    def output(self, values: dict[str, bool]) -> bool:
        if self.wire1 not in values or self.wire2 not in values:
            raise MissingInput()
        
        match self.gate:
            case 'AND':
                return values[self.wire1] and values[self.wire2]
            case 'OR':
                return values[self.wire1] or values[self.wire2]
            case 'XOR':
                return values[self.wire1] ^ values[self.wire2]

class Monitor:
    values: dict[str, bool]
    gates: list[Gate]
    
    def __init__(self, filename: str):
        self.values = dict()
        self.gates = []
        with open(filename, 'r') as filedata:
            for line in filedata.readlines():
                if len(line.strip()) == 0:
                    continue
                if ':' in line:
                    data = line.strip().split(':')
                    self.values[data[0]] = int(data[1].strip()) == 1
                if '->' in line:
                    data = line.strip().split(' ')
                    self.gates.append(Gate(wire1=data[0], gate=data[1], wire2=data[2], name=data[4]))
                    
    def produce(self):
        gates = self.gates.copy()
        while len(gates) > 0:
            gate = gates.pop(0)
            try:
                self.values[gate.name] = gate.output(self.values)
            except:
                gates.append(gate)
            
        names = []
        for name in self.values:
            if name.startswith('z'):
                names.append(name)
        names.sort(reverse=True)
        output = ''
        for name in names:
            output += '1' if self.values[name] else '0'
        return int(output, 2)

print("first part:")
print(Monitor('day24/sample').produce())
print(Monitor('day24/sample2').produce())
print(Monitor('day24/input').produce())