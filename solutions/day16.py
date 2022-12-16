import re
import copy
import numpy as np
from typing import List

def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')


    names_ = []
    flows_ = []
    connections_ = []

    for line_ in lines:
        splitted_line_ = line_.split(' ')
        names_.append(splitted_line_[1])
        flows_.append(int(re.findall(r'\d+', splitted_line_[4])[0]))

        pos_to_valve = line_.find('to valves')
        if pos_to_valve==-1:
            pos_to_valve = line_.find('to valve')
            connections_.append([x.strip() for x in line_[line_.find('to valve') + 9:].split(',')])
        else:
            connections_.append([x.strip() for x in line_[line_.find('to valves') + 10:].split(',')])

    print('========== INPUTS ==========')
    print(f'NAMES: {names_}')
    print(f'FLOWS: {flows_}')
    print(f'CONNECTIONS: {connections_}')
    print('========== ========= ==========')

    return names_, flows_, connections_


class State:
    min_passed:int
    cur_valve:str
    valves_state:List[int]
    total_pressure_released: int
    last_step_pressure_released: int

    def __init__(self, min_passed:int, cur_valve:str, valves_state:List[int], total_pressure_released:int):
        self.min_passed = min_passed
        self.cur_valve = cur_valve
        self.valves_state = valves_state
        self.total_pressure_released = total_pressure_released
        self.last_step_pressure_released = get_released_pressure(self.valves_state)

    def __str__(self):
        return f'min_passed = {self.min_passed}, cur_valve={self.cur_valve}, valves_state={self.valves_state}, total_pressure_released={self.total_pressure_released}, last_step_pressure_released = {self.last_step_pressure_released} '

    def __repr__(self):
        return str(self) + '\n'


class StateTwoPlayers:
    min_passed: int
    cur_valve1: str
    cur_valve2: str
    valves_state: List[int]
    valves_open: int
    total_pressure_released: int
    last_step_pressure_released: int

    def __init__(self, min_passed: int, cur_valve1: str, cur_valve2:str, valves_state: List[int], total_pressure_released: int):
        self.min_passed = min_passed
        self.cur_valve1 = cur_valve1
        self.cur_valve2 = cur_valve2
        self.valves_state = valves_state
        self.valves_open = sum(valves_state)

        self.total_pressure_released = total_pressure_released
        self.last_step_pressure_released = get_released_pressure(self.valves_state)

    def __str__(self):
        return f'min_passed = {self.min_passed}, your_position={self.cur_valve1}, Elephants_pos={self.cur_valve2}, valves_state={self.valves_state}, total_pressure_released={self.total_pressure_released}, last_step_pressure_released = {self.last_step_pressure_released} '

    def __repr__(self):
        return str(self) + '\n'

def get_released_pressure(valves_state_):
    return sum([i1 * i2 for i1, i2 in zip(valves_state_,flows)])



def solve_part1(max_steps_:int):
    state_zero = State(min_passed=0,
                       cur_valve='AA',
                       valves_state=valves_state_0,
                       total_pressure_released=0)

    MAX_STEPS = max_steps_
    states = [state_zero]
    max_valves_to_open = sum([1 for x in flows if x > 0])

    step = 0
    while step < MAX_STEPS:
        step += 1
        print(f'Step = {step}, possible previous states = {len(states)}')
        cur_states = []
        have_states_all_valves_open = False

        for prev_state in states:
            valves_open = sum(prev_state.valves_state)
            released = prev_state.last_step_pressure_released

            # 1) move only iff don't need to open (flow[cur_valve]==0 or flow[cur_valve]>0 and cur_valve is open already)
            if valves_open < max_valves_to_open and (
                    prev_state.valves_state[names_to_int[prev_state.cur_valve]] == 1 or flows[
                names_to_int[prev_state.cur_valve]] == 0):
                for next_valve in connections[names_to_int[prev_state.cur_valve]]:
                    cur_state = State(min_passed=step,
                                      cur_valve=next_valve,
                                      valves_state=prev_state.valves_state,
                                      total_pressure_released=prev_state.total_pressure_released + released)
                    cur_states.append(cur_state)

            # 2) open valve -- if makes sense (FLOWS[cur_valve]>0 and cur_valve is CLOSED)
            if flows[names_to_int[prev_state.cur_valve]] > 0 and prev_state.valves_state[
                names_to_int[prev_state.cur_valve]] == 0:
                new_valves = copy.deepcopy(prev_state.valves_state)
                new_valves[names_to_int[prev_state.cur_valve]] = 1
                cur_state = State(min_passed=step,
                                  cur_valve=prev_state.cur_valve,
                                  valves_state=new_valves,
                                  total_pressure_released=prev_state.total_pressure_released + released)
                cur_states.append(cur_state)

            # 3) do nothing
            if valves_open == max_valves_to_open:
                have_states_all_valves_open = True
                cur_state = State(min_passed=step,
                                  cur_valve=prev_state.cur_valve,
                                  valves_state=prev_state.valves_state,
                                  total_pressure_released=prev_state.total_pressure_released + released)
                cur_states.append(cur_state)

        # find states with max pressure released
        max_pressure_released = max([x.last_step_pressure_released for x in cur_states])
        min_pressure_released = min([x.last_step_pressure_released for x in cur_states])

        max_total_pressure_released = max([x.total_pressure_released for x in cur_states])

        max_open_valves = max([sum(x.valves_state) for x in cur_states])

        print(
            f'Found {len(cur_states)} states (max_open_valves = {max_open_valves}/{max_valves_to_open},  pressure released last_step is between ({min_pressure_released},{max_pressure_released}), and MAX_TOTAL_PRESSURE_RELEASED = {max_total_pressure_released})')

        # HEURISTICS! current state shouldn't be that bad
        states = [state for state in cur_states if sum(state.valves_state) >= max_open_valves - 2]

        print(f'Left only {len(states)} of optimal states for each cur_valve with max_pressure_released')

        print('===================')


def solve_part2():
    pass

# names, flows, connections = read_stats('../inputs/inputs_day16_test.txt', test_input=False)
names, flows, connections = read_stats('../inputs/inputs_day16.txt', test_input=False)

# no flows open at min = 0
valves_state_0 = [0 for x in flows]
# print(f'Valves state 0 = {valves_state_0}')

# build a dict {names:i}
names_to_int={}
for i,name in enumerate(names):
    names_to_int[name]=i
# print(f'Valve names to INT: {names_to_int}')

# PART1
# solve_part1(max_steps_=30)

# PART2
state_zero = StateTwoPlayers(min_passed=0,
                             cur_valve1='AA',
                             cur_valve2='AA',
                             valves_state = valves_state_0,
                             total_pressure_released=0)

MAX_STEPS = 26
states = [state_zero]
max_valves_to_open = sum([1 for x in flows if x > 0])

step = 0
while step < MAX_STEPS:
    step += 1
    print(f'Step = {step}, possible previous states = {len(states)}')
    cur_states = []
    have_states_all_valves_open = False

    for prev_state in states:
        valves_open = prev_state.valves_open
        released = prev_state.last_step_pressure_released

        # ME, ELEPHANT ACTIONS LIST from <MOVE, OPEN, DO_NOTHING>:

        valve_me, valve_el = prev_state.cur_valve1, prev_state.cur_valve2

        need_to_open_valve_me = flows[names_to_int[valve_me]]>0 and prev_state.valves_state[names_to_int[valve_me]] == 0
        need_to_open_valve_el = flows[names_to_int[valve_el]]>0 and prev_state.valves_state[names_to_int[valve_el]] == 0

        # 1) ME OPEN, ELEPHANT OPEN  -- open two players if we can!
        if need_to_open_valve_me and need_to_open_valve_el:
            new_valves = copy.deepcopy(prev_state.valves_state)
            new_valves[names_to_int[valve_me]] = 1 # open both valves
            new_valves[names_to_int[valve_el]] = 1
            cur_state = StateTwoPlayers(min_passed = step,
                              cur_valve1 = valve_me,
                              cur_valve2 = valve_el,
                              valves_state = new_valves,
                              total_pressure_released= prev_state.total_pressure_released + released)
            cur_states.append(cur_state)

        # 2) ME MOVE, ELEPHANT OPEN  -- open one players if they can!
        # open SECOND valve, first-MOVE
        elif not need_to_open_valve_me and need_to_open_valve_el:
            new_valves = copy.deepcopy(prev_state.valves_state)
            new_valves[names_to_int[valve_el]] = 1 # open  valves for elephant
            for next_valve_me in connections[names_to_int[valve_me]]:
                cur_state = StateTwoPlayers(min_passed=step,
                                            cur_valve1=next_valve_me,
                                            cur_valve2=valve_el,
                                            valves_state=new_valves,
                                            total_pressure_released=prev_state.total_pressure_released + released)
                cur_states.append(cur_state)

        # 3) ME OPEN, ELEPHANT MOVE -- open one players if they can!
        # open FIRST valve, second-MOVE
        elif need_to_open_valve_me and not need_to_open_valve_el:
            new_valves = copy.deepcopy(prev_state.valves_state)
            new_valves[names_to_int[valve_me]] = 1  # open  valves for elephant
            for next_valve_el in connections[names_to_int[valve_el]]:
                cur_state = StateTwoPlayers(min_passed=step,
                                            cur_valve1=valve_me,
                                            cur_valve2=next_valve_el,
                                            valves_state=new_valves,
                                            total_pressure_released=prev_state.total_pressure_released + released)
                cur_states.append(cur_state)

        # 4) ME MOVE, ELEPHANT MOVE  -- both move if they can't open AND there are valves to OPEN
        # BOTH players MOVE
        elif valves_open < max_valves_to_open and not need_to_open_valve_me and not need_to_open_valve_el:
            for next_valve_me in connections[names_to_int[valve_me]]:
                for next_valve_el in connections[names_to_int[valve_el]]:
                    cur_state = StateTwoPlayers(min_passed=step,
                                                cur_valve1=next_valve_me,
                                                cur_valve2=next_valve_el,
                                                valves_state=prev_state.valves_state,
                                                total_pressure_released=prev_state.total_pressure_released + released)
                    cur_states.append(cur_state)
        # 5) ME DO_NOTHING, ELEPHANT DO_NOTHING
        # ALL OPENED --> just release pressure
        elif valves_open == max_valves_to_open:
            cur_state = StateTwoPlayers(min_passed=step,
                                        cur_valve1=valve_me,
                                        cur_valve2=valve_el,
                                        valves_state=prev_state.valves_state,
                                        total_pressure_released=prev_state.total_pressure_released + released)
            cur_states.append(cur_state)

    # find states with min/max last_step and total pressure released
    max_pressure_released = max([x.last_step_pressure_released for x in cur_states])
    min_pressure_released = min([x.last_step_pressure_released for x in cur_states])

    max_total_pressure_released = max([x.total_pressure_released for x in cur_states])

    max_open_valves = max([x.valves_open for x in cur_states])

    max_total_pressure_released_max_opened_valves = max([x.total_pressure_released for x in cur_states if x.valves_open==max_open_valves])


    print(f'Found {len(cur_states)} states (max_open_valves = {max_open_valves}/{max_valves_to_open},  pressure released last_step is between ({min_pressure_released},{max_pressure_released}), and MAX_TOTAL_PRESSURE_RELEASED = {max_total_pressure_released})')

    # if max_open_valves < max_valves_to_open:
    if step<8:
        # HEURISTICS! current state shouldn't be that bad !!  another condition on total_pressure_released os very very APPROXIMATE!
        # state.valves_open >= max_open_valves - 2 and
        states = cur_states
        # states = [state for state in cur_states if  state.last_step_pressure_released>=min_pressure_released+ 0.05 * (max_pressure_released-min_pressure_released)]
    else:
        states = [state for state in cur_states if state.last_step_pressure_released >= min_pressure_released + 0.3 * (
                    max_pressure_released - min_pressure_released)]

        # states = [state for state in cur_states if (state.valves_open == max_valves_to_open - 1) or (state.valves_open == max_valves_to_open and state.total_pressure_released == max_total_pressure_released_max_opened_valves) ]

    print(f'Left only {len(states)} of optimal states for each cur_valve with max_pressure_released')

    print('===================')

#     (IVAN) WTF! I don't know, but my both parts are exactly 1 point smaller than the example solutions
