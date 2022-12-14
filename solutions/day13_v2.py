
# from aocd import data
import logging
from functools import cmp_to_key
from ast import literal_eval

#
# logging.basicConfig(filename='aoc.log', level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)
# logging.info('Start of program')

def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read()
        # .splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines


def parse(puzzle_input):
    # ast.literal_eval() is "more safe", but eval is ok for aoc
    return [[literal_eval(line) for line in pair.splitlines()]
            for pair in puzzle_input.split('\n\n')]

# can't just use bool because there is third option (equals)
def order(left, right):
    for i in range(len(left)):
        if i > len(right) - 1:
            return 1
        elif type(left[i]) == int:
            if type(right[i]) == int:
                if left[i] > right[i]:
                    logging.debug(f"Not in order: {left[i]}, {right[i]}")
                    return 1
                elif left[i] < right[i]:
                    return - 1
                else:
                    continue
            else:
                #convert int to list if necessary
                lr_order = order([left[i]], right[i])
                if lr_order == 0:
                    continue
                else:
                    return lr_order
        elif type(left[i]) == list:
            #convert int to list if necessary
            right_val = ([right[i]] if type(right[i]) == int
                         else right[i])
            lr_order = order(left[i], right_val)
            if lr_order == 0:
                continue
            else:
                return lr_order
    if len(left) < len(right):
        logging.debug(f'Finished looping through left {left}, right has more {right}')
        return -1
    # if the left & right were same length, 0 == continue
    return 0

def part1(parsed_data):
    sum_of_indices = 0
    logging.debug(f'There are {len(parsed_data)} pairs')
    for i in range(len(parsed_data)):
        left, right = parsed_data[i]
        logging.debug(f'In pair: {i + 1}')
        if order(left, right) < 1:
            logging.debug(f'Pair: {i + 1} is in order')
            sum_of_indices += i + 1
    return sum_of_indices


def part2(parsed_data):
    flattened = [message for pair in parsed_data for message in pair]
    flattened.extend([[[2]],[[6]]])
    flattened.sort(key=cmp_to_key(order))
    return (flattened.index([[2]])+1) * (flattened.index([[6]])+1)

def solve(data):
    """Solve the puzzle for the given input."""
    parsed_data = parse(data)
    solution1 = part1(parsed_data)
    solution2 = part2(parsed_data)

    return solution1, solution2

if __name__ == "__main__":
    # inputs = read_stats('../inputs/inputs_day13_test.txt', test_input=True)
    inputs = read_stats('../inputs/inputs_day13.txt', test_input=False)
    solutions = solve(inputs)
    print("\n".join(str(solution) for solution in solutions))