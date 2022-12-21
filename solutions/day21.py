import random
from dataclasses import dataclass
import re
from typing import List, Dict


# https://stackoverflow.com/questions/52390576/how-can-i-make-a-python-dataclass-hashable
@dataclass
class Node:
    name: str
    left_node_str: str
    right_node_str: str
    operation: str
    priority: int = None
    is_calculated: bool = False
    value: int = None


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    nodes_ = {}
    for line in lines:
        name_, command_ = line.split(':')
        # print(name_, command_)
        d = re.findall(r'\d+', command_)
        if d and d[0] == command_.strip():
            node_ = Node(name=name_,
                         left_node_str='',
                         right_node_str='',
                         operation='',
                         priority=0,
                         is_calculated=True,
                         value=int(d[0]))
            nodes_[name_] = node_
        else:
            op = re.findall(r'[\*/\+-]', command_)

            if op:
                # print(op[0])
                l, r = command_.split(op[0])
                node_ = Node(name=name_,
                             left_node_str=l.strip(),
                             right_node_str=r.strip(),
                             operation=op[0],
                             priority=-1,
                             is_calculated=False,
                             value=-1)
                nodes_[name_] = node_
            else:
                print('No operation found ((')

    return nodes_


def calculate_tree(t_: Dict[str, Node], is_part_2=False):
    cur_priority = 0
    undefined_priorities = [key for key in t_.keys() if
                            t_[key].priority == -1 and t_[key].is_calculated == False]
    # print(f'(cur_priority = {cur_priority}) Undefined priorities: {len(undefined_priorities)}')

    # define the priority of calculations (only for Part1, otherwise --> reuse that to calc
    if not is_part_2:
        while len(undefined_priorities) > 0:
            cur_priority += 1
            for key in undefined_priorities:
                left_node_str = t_[key].left_node_str
                right_node_str = t_[key].right_node_str
                # print(left_node_str, right_node_str)
                if t_[left_node_str].priority != -1 and t_[right_node_str].priority != -1:
                    t_[key].priority = cur_priority

            undefined_priorities = [key for key in t_.keys() if t_[key].priority == -1]
        # print(f'(cur_priority_defined = {cur_priority}) Undefined priorities: {len(undefined_priorities)}')

    max_priority = max([t_[key].priority for key in t_.keys()])
    # print(f'Max priority = {max_priority}')
    # print('========================')
    # print(f'Computing the tree:')

    # print(f'Current level (priority) = {0}')
    # for key in [key for key in t_.keys() if nodes[key].priority == 0]:
    # print(f'  This node is defined: {t_[key]}')

    cur_priority = 1
    while cur_priority < max_priority + 1:
        # print(f'Current level (priority) = {cur_priority}')
        to_be_computed = [key for key in t_.keys() if t_[key].priority == cur_priority]
        for k in to_be_computed:
            node = t_[k]
            if node.operation == '*':
                node.value = t_[node.left_node_str].value * t_[node.right_node_str].value
            elif node.operation == '/':
                node.value = t_[node.left_node_str].value / t_[node.right_node_str].value
            elif node.operation == '+':
                node.value = t_[node.left_node_str].value + t_[node.right_node_str].value
            elif node.operation == '-':
                node.value = t_[node.left_node_str].value - t_[node.right_node_str].value
            else:
                print(f'Wrong operation!!! for Node = {node}')
            node.is_calculated = True
            # print(f'  New node is computed: {node}')

        cur_priority += 1

    return t_


# FOR PART 2 : calc t_ tree for input_val, and find left-right value for root
# we need to find the value when f(t_, value) ==0
def f(t_: Dict[str, Node], input_val: float) -> float:
    t_['humn'].value = input_val
    # quick calculation with predefined priorities
    t_ = calculate_tree(t_, is_part_2=True)

    root_l_key = t_['root'].left_node_str
    root_r_key = t_['root'].right_node_str

    return t_[root_l_key].value - t_[root_r_key].value


# nodes = read_stats('../inputs/inputs_day21_test.txt', test_input=False)
nodes = read_stats('../inputs/inputs_day21.txt', test_input=False)
print(f'Inputs length = {len(nodes)}')

# PART1
tree = nodes

tree = calculate_tree(tree, is_part_2=False)
print(f'Part1 root value = {tree["root"]}')

# PART2
print('=============================')
print('Starting simulation for Part2')

left_boundary = -1e13
right_boundary = +1e13
steps = 10

part2_key = 0

iteration = 0
while iteration < 20:

    # print(f'Doing the interval [{left_boundary},{right_boundary}] within {2 * steps + 1} datapoints')

    # CALCULATE FUNC IN EVERY POINT
    values = []
    func_values = []
    for i in range(2 * steps + 1):
        value = left_boundary + i * (right_boundary - left_boundary) / steps
        f_ = f(tree, value)
        if f_ == 0:  # HERE IS THE SOLUTION!!!
            print('We found the solution!')
            part2_key = value
            break
        values.append(value)
        func_values.append(f_)
        # print(f' input_value = {value}, function f(value)={f_}')

    # no need to adjust the interval if we know the solution!
    if part2_key != 0:
        break

    # UPDATE THE RANGE FOR SEARCH (assume the function is monotonic)
    f_min_value = -1
    f_max_value = -1
    for i in range(len(values) - 1):
        if (func_values[i] > 0 and func_values[i + 1] < 0) or (func_values[i] < 0 and func_values[i + 1] > 0):
            left_boundary = min(values[i], values[i + 1])
            right_boundary = max(values[i], values[i + 1])
            f_min_value = min(func_values[i], func_values[i + 1])
            f_max_value = max(func_values[i], func_values[i + 1])
            break
    print(f'SELECTED THESE VALUES FOR THE NEXT INTERVAL {left_boundary} (f_={f_min_value}), and'
          f' {right_boundary} (f_={f_max_value})')
    iteration += 1

if part2_key != 0:
    print(f'RESULT FOR PART2 = {part2_key}')
