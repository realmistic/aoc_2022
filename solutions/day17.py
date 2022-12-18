import numpy as np
from typing import List
from dataclasses import dataclass


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines


class Rock:
    x: int
    y: int
    type: str
    cells: List[List[str]]

    def try_left(self):
        pass

    def try_right(self):
        pass

    def try_down(self):
        pass

    def __str__(self):
        return f'type {self.type} at pos ({self.x, self.y})'

    def __repr__(self):
        return str(self) + '\n'


@dataclass
class HLineRock(Rock):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = 'hline'
        self.cells = [['#', '#', '#', '#']]


@dataclass
class CrossRock(Rock):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = 'cross'
        self.cells = [['.', '#', ','], ['#', '#', '#'], ['.', '#', '.']]


@dataclass
class CornerRock(Rock):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = 'corner'
        self.cells = [['.', '.', '#'], ['.', '.', '#'], ['#', '#', '#']]


@dataclass
class VLineRock(Rock):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = 'vline'
        self.cells = [['#'], ['#'], ['#'], ['#']]


@dataclass
class SquareRock(Rock):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.type = 'square'
        self.cells = [['#', '#'], ['#', '#']]


class Field:
    width: int
    height: int
    gas_pattern: str
    gas_pointer: int
    cells: np.ndarray
    rocks: List[Rock]
    tallest_elem: int

    def emulate_rock(self, rockType: str):

        if rockType == 'hline':
            if self.tallest_elem - 3 - 1 < 0:
                return False
            r = HLineRock(self.tallest_elem - 3 - 1, 2)
        elif rockType == 'cross':  # 2 additional lines needed
            if self.tallest_elem - 3 - 3 < 0:
                return False
            r = CrossRock(self.tallest_elem - 3 - 3, 2)
        elif rockType == 'corner':  # 2 additional lines needed
            if self.tallest_elem - 3 - 3 < 0:
                return False
            r = CornerRock(self.tallest_elem - 3 - 3, 2)
        elif rockType == 'vline':  # 3 additional lines needed
            if self.tallest_elem - 3 - 4 < 0:
                return False
            r = VLineRock(self.tallest_elem - 3 - 4, 2)
        elif rockType == 'square':  # 1 additional lines needed
            if self.tallest_elem - 3 - 2 < 0:
                return False
            r = SquareRock(self.tallest_elem - 3 - 2, 2)

        # print(
        #     f'Created rock {r}, current gas pointer = {self.gas_pointer} (out of {len(self.gas_pattern)}), tallest elem = {self.tallest_elem}')

        steps = 0
        while steps < self.height:
            if self.gas_pattern[self.gas_pointer] == '>':
                # print('Gas tries to push right')
                self.try_move_right(r)
                self.gas_pointer = (self.gas_pointer + 1) % (len(self.gas_pattern))
            elif self.gas_pattern[self.gas_pointer] == '<':
                # print('Gas tries to push left')
                self.try_move_left(r)
                self.gas_pointer = (self.gas_pointer + 1) % (len(self.gas_pattern))

            move = self.try_move_down(r)
            if not move:
                # print(f'Can\'t move down')
                self.rocks.append(r)
                self.add_rock(r)
                if r.x < self.tallest_elem:
                    self.tallest_elem = r.x
                break

            steps += 1

        return True  # added a rock

    def try_move_right(self, r: Rock):
        if self.can_add_rock(r, r.x, r.y + 1):
            r.y += 1
            # print('Moved right')
            return True
        else:
            return False

    def try_move_left(self, r: Rock):
        if self.can_add_rock(r, r.x, r.y - 1):
            r.y -= 1
            # print('Moved left')
            return True
        else:
            return False

    def try_move_down(self, r: Rock):
        if self.can_add_rock(r, r.x + 1, r.y):
            r.x += 1
            # print('Moved down')
            return True
        else:
            return False

    def can_add_rock(self, r: Rock, x: int, y: int):
        if x < 0 or y < 0 or x >= len(self.cells) or y >= len(self.cells[0]):
            return False

        for i in range(len(r.cells)):
            for j in range(len(r.cells[i])):
                if x + i >= len(self.cells) or y + j >= len(self.cells[i]):
                    return False
                if r.cells[i][j] == '#' and self.cells[x + i, y + j] != '.':
                    return False
        return True

    def add_rock(self, r: Rock):
        for i in range(len(r.cells)):
            for j in range(len(r.cells[i])):
                if r.cells[i][j] == '#':
                    self.cells[r.x + i, r.y + j] = '#'
        return

    def erase_rock(self, r: Rock):
        for i in range(len(r.cells)):
            for j in range(len(r.cells[i])):
                if self.cells[r.x + i, r.y + j] == '#':
                    self.cells[r.x + i, r.y + j] = '.'
        return

    def __init__(self, height: int, width: int, gas_pattern_: str):
        self.width = width
        self.height = height
        self.cells = np.zeros((height, width), dtype='str')
        self.rocks = []
        self.gas_pattern = gas_pattern_
        self.gas_pointer = 0
        self.tallest_elem = height  # nothing at the bottom

        for i in range(height):
            for j in range(width):
                self.cells[i][j] = '.'

    def __str__(self):
        return str(self.cells)

    def __repr__(self):
        return str(self) + '\n'


def compare_two_lines(f_: Field, i_: int, j_: int):
    line_i = f_.cells[i_]
    line_j = f_.cells[j_]
    for x in range(len(line_i)):
        if line_i[x] != line_j[x]:
            return False
    return True


def find_cycle(f_: Field):
    cycle_len = 1

    while cycle_len <= f_.tallest_elem // 2:
        found_pattern = True
        for i in range(cycle_len):
            rez = compare_two_lines(f_, f_.height - 1 - i, f_.height - 1 - i - cycle_len)
            if not rez:
                found_pattern = False
                break

        if found_pattern:
            return cycle_len
        cycle_len += 1

    return -1


# gas_pattern = read_stats('../inputs/inputs_day17_test.txt', test_input=False)
gas_pattern = read_stats('../inputs/inputs_day17.txt', test_input=False)

FIELD_WIDTH = 7
FIELD_HEIGHT = 4000000

field = Field(FIELD_HEIGHT, FIELD_WIDTH, gas_pattern[0])

cnt = 0
order_rocks = ['hline', 'cross', 'corner', 'vline', 'square']
while cnt < 2022000:
    new_rock = field.emulate_rock(order_rocks[cnt % 5])
    if not new_rock:
        break
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt)
    # print(field)

print(f'Added {cnt} rocks ')
print(f'Height of the structure {field.height - field.tallest_elem}')

print(find_cycle(field))
