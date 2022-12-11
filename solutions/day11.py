import re
from typing import List
from copy import deepcopy


def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines

class Monkey:
    no:int
    items: List[int]
    num_items: int
    operation: str
    test_division: int
    true_test_pass: int
    false_test_pass: int
    inspected: int

    def __init__(self, list_input_lines: List[str]):
        self.no = int(re.findall(r'\d+',list_input_lines[0])[0])
        self.items = [int(x) for x in re.findall(r'\d+',list_input_lines[1])]
        # self.num_items = len(self.items)
        self.operation = list_input_lines[2].partition("=")[-1].strip()
        self.test_division = int(re.findall(r'\d+',list_input_lines[3])[0])
        self.true_test_pass = int(re.findall(r'\d+',list_input_lines[4])[0])
        self.false_test_pass = int(re.findall(r'\d+',list_input_lines[5])[0])
        self.inspected =0
    def __str__(self):
        return f'Monkey {self.no}, items={self.items}, op={self.operation}, div={self.test_division}, ' \
               f'true_div={self.true_test_pass}, false_div={self.false_test_pass}, inspected ={self.inspected}'
    def __repr__(self):
        return str(self)+'\n'

# Perform operations for monkey 'no' in the list of Monkeys, lcm = least common multiplier for ALL monkeys
def do_operations(monkeys_:List[Monkey], no:int, lcm:int=None, debug=False, part1=True):
    if debug:
        print(f'Monkey {no}:')
    m_ = monkeys_[no]

    for i_ in range(len(m_.items)):
        if not part1: # only for part2 -- store lower values
            m_.items[i_] = m_.items[i_] % lcm

        operation_ = m_.operation.replace('old',str(m_.items[i_]))
        if debug:
            print(operation_)
        worry_level = eval(operation_)
        if debug:
            print(worry_level)

        if part1: # only for part1 -- worry level is divided by 3
            worry_level = worry_level // 3

        if debug:
            print(worry_level)
        if worry_level % m_.test_division == 0:
            monkeys_[m_.true_test_pass].items.append(worry_level)
            if debug:
                print(f' (PASSED) Item with worry level {worry_level} is thrown to monkey {m_.true_test_pass}.')
        else:
            monkeys_[m_.false_test_pass].items.append(worry_level)
            if debug:
                print(f' (NOT PASSED) Item with worry level {worry_level} is thrown to monkey {m_.false_test_pass}.')

    if debug:
        print(f'==============')
    for _ in range(len(m_.items)):
        m_.items.pop(0)
        m_.inspected+=1
    return

# LEAST COMMON MULTIPLIER
# https://deepnote.com/@Python-Guides/Least-Common-Multiple-in-Python-deaa7c93-d6aa-404d-a70e-912e217dce2c
def lcm(x, y):
   if x > y:
       greater = x
   else:
       greater = y

   while True:
       if (greater % x == 0) and (greater % y == 0):
           lcm_ = greater
           break
       greater += 1

   return lcm_


# ------------------------
#         INPUTS
# input_stats = read_stats('../inputs/inputs_day11_test.txt', test_input=False)
input_stats = read_stats('../inputs/inputs_day11.txt', test_input=False)
print(input_stats)

# read monkeys input
monkeys : List[Monkey]=[]
m: Monkey

input_stats.insert(0,'') # slightly modify input to read all Monkeys info
for i in range(len(input_stats)):
    if input_stats[i]=='':
        m = Monkey(input_stats[(i+1):(i+7)])
        monkeys.append(m)

print(f'Initial state = {monkeys}')
monkeys_part2 = [deepcopy(m) for m in monkeys]

round_=0
for round_ in range(20):
    for i in range(len(monkeys)):
       do_operations(monkeys,i, part1=True)
    print(f' After round {round_+1} the state is:')
    print(monkeys)

inspected = [m.inspected for m in monkeys]
sorted_inspected= sorted(inspected)
print(f'TOP2 monkeys inspectors: {sorted_inspected[-1]}, {sorted_inspected[-2]}')
print(f'PART1 result: {sorted_inspected[-1]*sorted_inspected[-2]}')

print('---------------PART2-----------------')
print(f'Initial state = {monkeys_part2}')

lcm_all = 1
for i in range(len(monkeys_part2)):
    lcm_all = lcm(lcm_all,monkeys_part2[i].test_division)

print(f'LCM_ALL = {lcm_all}')

for round_ in range(10000):
    for i in range(len(monkeys_part2)):
       do_operations(monkeys_part2, i, lcm=lcm_all, part1=False)
    if (round_+1) %100 ==0 or (round_+1)==1 or (round_+1)==20:
        print(f' After round {round_+1} the state is:')
        print(monkeys_part2)

inspected_part2 = [m.inspected for m in monkeys_part2]
sorted_inspected_part2= sorted(inspected_part2)
print(f'TOP2 monkeys inspectors: {sorted_inspected_part2[-1]}, {sorted_inspected_part2[-2]}')
print(f'PART2 result: {sorted_inspected_part2[-1]*sorted_inspected_part2[-2]}')