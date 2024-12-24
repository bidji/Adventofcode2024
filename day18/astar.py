from logging import Logger
from typing import Self


class MazeException(Exception):
    pass


class Node:
    parent: Self
    x: int
    y: int
    f: int
    g: int
    h: int
    
    def __init__(self, x: int, y: int, g: int=0, h: int=0, parent: Self=None):
        self.x, self.y = x, y
        self.f, self.g, self.h = g + h, g, h
        self.parent = parent
        
    @classmethod
    def build(cls, parent: Self, incr_x: int, incr_y: int) -> Self:
        return cls(x=parent.x + incr_x,
                   y=parent.y + incr_y,
                   g=parent.g + 1,
                   parent=parent)
    
    def compute(self, exit: Self) -> Self:
        # self.h = (exit.x - self.x) ** 2 + (exit.y - self.y) ** 2
        self.h = abs(exit.x - self.x) + abs(exit.y - self.y)
        self.f = self.g + self.h
        return self
        
    def __eq__(self, other: Self):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"{self.y}/{self.x} f:{self.f} g:{self.g}"


class Maze:
    grid: list[list[str]]
    wall: str
    path: str
    walkthrough: Node
    logger: Logger
    
    
    def __init__(self, grid: list[list[str]], wall: str='#', path: str='O', logger=None):
        # we want to be sure that grid will not be modified by our solver
        # just in case caller is expecting to be able to use it later
        self.wall = wall
        self.path = path
        self.logger = logger
        self.walkthrough = None
        
        self.grid = []
        for row in grid:
            self.grid.append(row.copy())
    
    def solve(self, start: tuple[int, int], end: tuple[int, int]) -> Self:
        """use A* algorithm to solve the maze"""
        opened = [Node(start[0], start[1])]
        closed = []
        exit = Node(end[0], end[1])
        
        while len(opened) > 0:
            # find the node with least f value
            opened.sort(key=lambda node: node.f, reverse=True)
            self.logger and self.logger.debug(f"opened: {' | '.join([str(n) for n in opened])}")
            current = opened.pop()
            self.logger and self.logger.debug(f"current: {current}")
            closed.append(current)
            
            if current == exit:
                self.logger and self.logger.debug(f"shortest path found: {current}")
                self.walkthrough = current
                return self

            # try to go up
            if current.y > 0 and self.grid[current.y - 1][current.x] != self.wall:
                up = Node.build(parent=current, incr_x=0, incr_y=-1)
                if up not in closed:
                    up.compute(exit)
                    if up not in opened:
                        opened.append(up)
                    elif up.g < opened[opened.index(up)].g:
                        if up in opened:
                            opened[opened.index(up)] = up
            # try to go down
            if current.y < len(self.grid) - 1 and self.grid[current.y + 1][current.x] != self.wall:
                down = Node.build(parent=current, incr_x=0, incr_y=1)
                if down not in closed:
                    down.compute(exit)
                    if down not in opened:
                        opened.append(down)
                    elif down.g < opened[opened.index(down)].g:
                        opened[opened.index(down)] = down
            # try to go left
            if current.x > 0 and self.grid[current.y][current.x - 1] != self.wall:
                left = Node.build(parent=current, incr_x=-1, incr_y=0)
                if left not in closed:
                    left.compute(exit)
                    if left not in opened:
                        opened.append(left)
                    elif left.g < opened[opened.index(left)].g:
                        opened[opened.index(left)] = left
            # try to go right
            if current.x < len(self.grid[current.y]) - 1 and self.grid[current.y][current.x + 1] != self.wall:
                right = Node.build(parent=current, incr_x=1, incr_y=0)
                if right not in closed:
                    right.compute(exit)
                    if right not in opened:
                        opened.append(right)
                    elif right.g < opened[opened.index(right)].g:
                        opened[opened.index(right)] = right
                    
        # didn't find exit
        raise MazeException()
    
    def __str__(self):
        string = "grid:\n"
        
        grid = []
        for row in self.grid:
            grid.append(row.copy())

        current = self.walkthrough
        while current:
            grid[current.y][current.x] = 'O'
            current = current.parent
        
        for j in range(0, len(grid)):
            string += "".join(grid[j])
            string += "\n"
        
        return string
