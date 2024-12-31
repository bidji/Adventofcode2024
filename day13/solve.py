class NoExistingSolution(Exception):
    pass


class NoIntegerSolution(Exception):
    pass


class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int
    
    def __init__(self, ax: int, ay: int, bx: int, by: int, px: int, py: int):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py
        
    def solve(self) -> tuple[int, int]:
        """solving with Cramer theorem
        ax * a + bx * b = px
        ay * a + by * b = py
        a = ((px * by) - (bx * py)) / ((ax * by) - (bx * ay))
        b = ((ax * py) - (px * ay)) / ((ax * by) - (bx * ay))
        """
        detA = (self.ax * self.by) - (self.bx * self.ay)
        if detA == 0:
            raise NoExistingSolution()
        a = int(((self.px * self.by) - (self.bx * self.py)) / detA)
        b = int(((self.ax * self.py) - (self.px * self.ay)) / detA)
        if self.ax * a + self.bx * b != self.px or self.ay * a + self.by * b != self.py:
            raise NoIntegerSolution()
        return a, b

class Solver:
    filename: str
    machines: list[Machine]
    
    def __init__(self, filename):
        self.filename = filename
        self.machines = []

    def load(self, offset: int=0):
        with open(self.filename, 'r') as filedata:
            machine = dict()
            for line in filedata.readlines():
                if len(line.strip()) == 0:
                    continue
                
                data = line.strip().split(':')[1]
                if line.startswith('Button A:'):
                    machine['ax'] = int(data.split(',')[0].replace('X+', '').strip())
                    machine['ay'] = int(data.split(',')[1].replace('Y+', '').strip())
                if line.startswith('Button B:'):
                    machine['bx'] = int(data.split(',')[0].replace('X+', '').strip())
                    machine['by'] = int(data.split(',')[1].replace('Y+', '').strip())
                if line.startswith('Prize:'):
                    machine['px'] = int(data.split(',')[0].replace('X=', '').strip()) + offset
                    machine['py'] = int(data.split(',')[1].replace('Y=', '').strip()) + offset
                    self.machines.append(Machine(machine['ax'], machine['ay'],
                                                 machine['bx'], machine['by'],
                                                 machine['px'], machine['py']))
                    machine = dict()
                
        
    def count_needed_tokens(self, with_limit: bool=True) -> int:
        needed_tokens = 0
        
        for machine in self.machines:
            try:
                a, b = machine.solve()
                if a < 0 or b < 0:
                    continue
                if with_limit and (a > 100 or b > 100):
                    continue
                needed_tokens += 3 * a + b
            except NoExistingSolution:
                pass
            except NoIntegerSolution:
                pass
        
        return needed_tokens


print("part 1:")
solver = Solver('day13/sample')
solver.load(offset=0)
print(solver.count_needed_tokens())
solver = Solver('day13/input')
solver.load(offset=0)
print(solver.count_needed_tokens())

print("part 2:")
solver = Solver('day13/input')
solver.load(offset=10000000000000)
print(solver.count_needed_tokens(with_limit=False))