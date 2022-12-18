import numpy as np

from dataclasses import dataclass
from typing import List


@dataclass
class Cube:
    """Class to store cube coords x,y,z"""
    x: int
    y: int
    z: int


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    cubes_ = []

    for line in lines:
        x_, y_, z_ = line.split(',')
        c = Cube(int(x_), int(y_), int(z_))
        cubes_.append(c)

    return cubes_


def test_connection(c1: Cube, c2: Cube):
    if abs(c1.x - c2.x) == 1 and c1.y == c2.y and c1.z == c2.z:
        return True
    elif abs(c1.y - c2.y) == 1 and c1.x == c2.x and c1.z == c2.z:
        return True
    elif abs(c1.z - c2.z) == 1 and c1.x == c2.x and c1.y == c2.y:
        return True

    return False


def find_min_max_coords(cubes_: List[Cube]):
    x = [c.x for c in cubes_]
    y = [c.y for c in cubes_]
    z = [c.z for c in cubes_]

    print(f'Coord x is between {min(x)} and {max(x)}')
    print(f'Coord y is between {min(y)} and {max(y)}')
    print(f'Coord z is between {min(z)} and {max(z)}')

    return


def solve_part1(cubes_: List[Cube]):
    connected_sides = 0
    for i in range(len(cubes_)):
        j = i + 1
        while j < len(cubes_):
            is_conn = test_connection(cubes_[i], cubes_[j])
            if is_conn:
                connected_sides += 1
            j += 1
    return len(cubes) * 6 - 2 * connected_sides


def try_inner_border(matrix_: np.ndarray, cx: int, cy: int):
    if cx == 0 or cy == 0 or cx == len(matrix_) - 1 or cy == len(matrix_[cx]) - 1:
        return False

    found_up = False
    found_down = False
    found_left = False
    found_right = False

    for cur in range(cx):
        if matrix_[cx - cur - 1, cy] == 'X':
            found_up = True
            break

    for cur in range(len(matrix_) - cx - 1):
        if matrix_[cx + cur + 1, cy] == 'X':
            found_down = True
            break

    for cur in range(cy):
        if matrix_[cx, cy - cur - 1] == 'X':
            found_left = True
            break

    for cur in range(len(matrix_[cx]) - cy - 1):
        if matrix_[cx, cy + cur + 1] == 'X':
            found_right = True
            break

    if found_up and found_down and found_right and found_left:
        return True
    else:
        return False


def remove_bad_inner_borders(matrix_: np.ndarray):
    for i in range(len(matrix_)):
        for j in range(len(matrix_[i])):
            if matrix_[i, j] == 'O':
                if matrix_[i - 1, j] == '.' or matrix_[i + 1, j] == '.' or matrix_[i, j - 1] == '.' or matrix_[
                    i, j + 1] == '.':
                    matrix_[i, j] = '.'
                    return True

    return False


def gen_slice_x(cubes_: List[Cube], fixed_x, generate_inner_border=True):
    subset_cubes = [cube for cube in cubes_ if cube.x == fixed_x]

    y = [c.y for c in cubes_]
    z = [c.z for c in cubes_]

    range_y = max(y) - min(y) + 1
    range_z = max(z) - min(z) + 1

    matrix_ = np.zeros((range_y, range_z), dtype='str')

    for i_ in range(len(matrix_)):
        for j_ in range(len(matrix_[i_])):
            matrix_[i_, j_] = '.'

    for c in subset_cubes:
        matrix_[c.y - 1, c.z - 1] = 'X'

    if generate_inner_border:
        for i_ in range(len(matrix_)):
            for j_ in range(len(matrix_[i_])):
                if matrix_[i_, j_] == '.' and try_inner_border(matrix_, i_, j_):
                    matrix_[i_, j_] = 'O'

    # iteratively remove 'bad' borders ==> All 'O' should be surrounded only by X
    removed_border = True
    while removed_border:
        removed_border = remove_bad_inner_borders(matrix_)

    return matrix_


def gen_slice_y(cubes_: List[Cube], fixed_y, generate_inner_border=True):
    subset_cubes = [cube for cube in cubes_ if cube.y == fixed_y]

    x_ = [c.x for c in cubes_]
    z_ = [c.z for c in cubes_]

    range_x = max(x_) - min(x_) + 1
    range_z = max(z_) - min(z_) + 1

    matrix_ = np.zeros((range_x, range_z), dtype='str')

    for i_ in range(len(matrix_)):
        for j_ in range(len(matrix_[i_])):
            matrix_[i_, j_] = '.'

    for c in subset_cubes:
        matrix_[c.x - 1, c.z - 1] = 'X'

    if generate_inner_border:
        for i_ in range(len(matrix_)):
            for j_ in range(len(matrix_[i])):
                if matrix_[i_, j_] == '.' and try_inner_border(matrix_, i_, j_):
                    matrix_[i_, j_] = 'O'

    # iteratively remove 'bad' borders ==> All 'O' should be surrounded only by X
    removed_border = True
    while removed_border:
        removed_border = remove_bad_inner_borders(matrix_)

    return matrix_


# cubes = read_stats('../inputs/inputs_day18_test.txt', test_input=False)
cubes = read_stats('../inputs/inputs_day18.txt', test_input=False)

find_min_max_coords(cubes)

all_x = [c.x for c in cubes]
min_x, max_x = min(all_x), max(all_x)

potential_blocked = {}

for x in range(max_x - min_x + 1):
    print(f'Fixing x== {min_x + x}')
    slice_x = gen_slice_x(cubes, fixed_x=min_x + x)

    for i in range(len(slice_x)):
        for j in range(len(slice_x[i])):
            if slice_x[i, j] == 'O':
                potential_blocked[(min_x + x, i + 1, j + 1)] = 1
    print(slice_x)
    print('=================')

print(f' Potentially blocked cells: {len(potential_blocked)}')

print(' NOW MOVING TO  SLICING Y')

all_y = [c.y for c in cubes]
min_y, max_y = min(all_y), max(all_y)

for y in range(max_y - min_y + 1):
    print(f'Fixing y== {min_y + y}')
    slice_y = gen_slice_y(cubes, fixed_y=min_y + y)

    for i in range(len(slice_y)):
        for j in range(len(slice_y[i])):
            if slice_y[i, j] == 'O' and (i + 1, min_y + y, j + 1) in potential_blocked.keys():
                potential_blocked[(i + 1, min_y + y, j + 1)] = 2
    print(slice_y)
    print('=================')

double_blocked = {}

for key in potential_blocked:
    if potential_blocked[key] == 2:
        double_blocked[key] = 2

print(f' DOUBLE blocked cells: {len(double_blocked)}')

part1 = solve_part1(cubes)

print(f'Part1 res: {part1}')

removed_inner_connections = 0
for elem in double_blocked:
    for c in cubes:
        e_x, e_y, e_z = elem
        if test_connection(c, Cube(e_x, e_y, e_z)):
            removed_inner_connections += 1

print(f' Found these connections to remove = {removed_inner_connections}')

print(f'Part2 res: {part1 - removed_inner_connections}')
