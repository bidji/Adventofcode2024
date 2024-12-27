class MissingInput(Exception):
    pass


class Gate:
    name_input1: str
    name_input2: str
    gate: str
    name_output: str
    
    def __init__(self, name_input1: str, gate: str, name_input2: str, name_output: str):
        self.name_input1 = name_input1
        self.name_input2 = name_input2
        self.gate = gate
        self.name_output = name_output
        
    def __str__(self):
        return f"{self.name_input1} {self.gate} {self.name_input2} -> {self.name_output}"
    
    def __copy__(self):
        return Gate(self.name_input1, self.gate, self.name_input2, self.name_output)
    
    def output(self, values: dict[str, bool]) -> bool:
        if self.name_input1 not in values or self.name_input2 not in values:
            raise MissingInput()
        
        match self.gate:
            case 'AND':
                return values[self.name_input1] and values[self.name_input2]
            case 'OR':
                return values[self.name_input1] or values[self.name_input2]
            case 'XOR':
                return values[self.name_input1] ^ values[self.name_input2]

class Monitor:
    initial_values: dict[str, bool]
    initial_gates: list[Gate]
    values: dict[str, bool]
    gates: list[Gate]
    
    def __init__(self, filename: str):
        self.initial_values = dict()
        self.initial_gates = []
        with open(filename, 'r') as filedata:
            for line in filedata.readlines():
                if len(line.strip()) == 0:
                    continue
                if ':' in line:
                    data = line.strip().split(':')
                    self.initial_values[data[0]] = int(data[1].strip()) == 1
                if '->' in line:
                    data = line.strip().split(' ')
                    self.initial_gates.append(Gate(name_input1=data[0], gate=data[1], name_input2=data[2], name_output=data[4]))
        self.values = self.initial_values.copy()
        self.gates = self.initial_gates.copy()
        
    def reset(self):
        self.values = self.initial_values.copy()
                    
    def produce(self):
        gates = self.gates.copy()
        while len(gates) > 0:
            gate = gates.pop(0)
            try:
                self.values[gate.name_output] = gate.output(self.values)
            except:
                gates.append(gate)
            
        znames = []
        for name in self.values:
            if name.startswith('z'):
                znames.append(name)
        znames.sort(reverse=True)
        output = ''
        for name in znames:
            output += '1' if self.values[name] else '0'
        return int(output, 2)
    
    def check(self):
        xnames = []
        ynames = []
        for name in self.values:
            if name.startswith('x'):
                xnames.append(name)
            if name.startswith('y'):
                ynames.append(name)
                
        xnames.sort(reverse=True)
        input = ''
        for name in xnames:
            input += '1' if self.values[name] else '0'
        x = int(input, 2)
        
        ynames.sort(reverse=True)
        input = ''
        for name in ynames:
            input += '1' if self.values[name] else '0'
        y = int(input, 2)
        
        z = self.produce()
        return x + y == z
    
    def repair(self) -> str:
        if self.check():
            return 'None'
        
        self.reset()
        #TODO: find fixes
        fixes = ['z00', 'z04', 'z01', 'z02']
        for gate in self.gates:
            if gate.name_output == fixes[0]:
                gate.name_output = fixes[1]
            elif gate.name_output == fixes[1]:
                gate.name_output = fixes[0]
            elif gate.name_output == fixes[2]:
                gate.name_output = fixes[3]
            elif gate.name_output == fixes[3]:
                gate.name_output = fixes[2]
        
        if self.check():
            fixes.sort()
            return ','.join(fixes)

print("first part:")
print(Monitor('day24/sample').produce())
print(Monitor('day24/sample2').produce())
print(Monitor('day24/input').produce())

print("second part:")
print(f"fixes: {Monitor('day24/sample3').repair()}")
print(f"fixes: {Monitor('day24/sample4').repair()}")