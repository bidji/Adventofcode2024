class Computer:
    def __init__(self, filename: str):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.program = []
        self.pointer = 0
        self.jump = False
        self.output = []
    
        with open(filename, 'r') as filedata:
            for line in filedata.readlines():
                if len(line.strip()) == 0:
                    continue
                
                data = line.strip().split(':')[1].strip()
                if line.startswith('Register A:'):
                    self.registerA = int(data)
                if line.startswith('Register B:'):
                    self.registerB = int(data)
                if line.startswith('Register C:'):
                    self.registerC = int(data)
                if line.startswith('Program:'):
                    self.program = [int(x) for x in data.split(',')]
                    
    def adv(self, value):
        """A / 2**value (opcode 0)"""
        self.registerA = int(self.registerA / (2 ** value))
    
    def bxl(self, literal):
        """B ^ literal value"""
        self.registerB = self.registerB ^ literal
        
    def bst(self, value):
        self.registerB = value % 8
        
    def jnz(self, value):
        if self.registerA != 0:
            self.pointer = value
            self.jump = True
        
    def bxc(self):
        self.registerB = self.registerB ^ self.registerC
        
    def out(self, value):
        self.output.append(value % 8)
        
    def bdv(self, value):
        self.registerB = int(self.registerA / (2 ** value))
        
    def cdv(self, value):
        self.registerC = int(self.registerA / (2 ** value))
        
    def run_instruction(self, instruction: int, operand: int):
        value = operand
        if operand == 4:
            value = self.registerA
        if operand == 5:
            value = self.registerB
        if operand == 6:
            value = self.registerC
            
        match instruction:
            case 0:
                self.adv(value)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(value)
            case 3:
                self.jnz(value)
            case 4:
                self.bxc()
            case 5:
                self.out(value)
            case 6:
                self.bdv(value)
            case 7:
                self.cdv(value)
    
    def run(self):
        while self.pointer < len(self.program):
            self.jump = False
            self.run_instruction(instruction=self.program[self.pointer], operand=self.program[self.pointer+1])
            if not self.jump:
                self.pointer += 2
        return ",".join([str(o) for o in self.output])

print("first part:")
print(Computer('day17/sample').run())
print(Computer('day17/input').run())

