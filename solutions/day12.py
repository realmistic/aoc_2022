import numpy as np



def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    m = []
    for line in lines:
        m.append(list(line))

    mm = np.matrix(m, dtype=str)

    return mm

def find_start_end(m_:np.matrix):
    sx_,sy_,ex_,ey_=[-1,-1,-1,-1]
    for i in range(m_.shape[0]):
        for j in range(m_.shape[1]):
            if m_[i,j]=='S':
                sx_= i
                sy_= j
            elif m_[i,j] == 'E':
                ex_= i
                ey_= j
    return (sx_,sy_), (ex_,ey_)


def find_starting_points(m_:np.matrix):
    res_=[]
    for i in range(m_.shape[0]):
        for j in range(m_.shape[1]):
            if m_[i, j] == 'S' or m_[i, j] == 'a':
                res_.append((i,j))
    return res_


def get_next_step(m_:np.matrix, cx_:int, cy_:int):
    next_=[]
    if cx_>0:
        next_.append((cx_-1,cy_))
    if cx_ < m_.shape[0]-1:
        next_.append((cx_+1, cy_))
    if cy_ > 0:
        next_.append((cx_, cy_-1))
    if cy_ < m_.shape[1] - 1:
        next_.append((cx_, cy_+1))
    return next_


def find_shortest_path(m_:np.matrix, start_point, end_point, debug=False):
    # max route length == All cells
    max_steps = m_.shape[0] * m_.shape[1]

    # init matrix with max length
    min_route = max_steps * np.ones(m.shape)
    min_route[start_point] = 0

    step = 1
    where_to_go = [start_point]  # starting position

    while step <= max_steps:
        next_steps = []
        # debug: print(f'Step = {step}')
        while len(where_to_go) > 0:
            cur_cell = where_to_go.pop()
            cur_elem = m[cur_cell] if m[cur_cell] != 'S' else 'a'
            # debug: print(f'  Cur cell = {m[cur_cell]}')
            for next_cell in get_next_step(m, cx_=cur_cell[0], cy_=cur_cell[1]):
                # debug: print(f'    checking next cell = {next_cell}')
                next_elem = m[next_cell] if m[next_cell] != 'E' else 'z'
                if ord(next_elem) <= ord(cur_elem) + 1:
                    if min_route[next_cell] > min_route[cur_cell] + 1:
                        min_route[next_cell] = min_route[cur_cell] + 1
                        next_steps.append(next_cell)
        where_to_go = next_steps
        # debug: print(f'  Generated next steps: {where_to_go}')
        # debug: print('---------------')
        step += 1

    if debug:
        print(f'Min routes matrix: {min_route}')
    return min_route[end_point]

# ------------------------
#         INPUTS

# m = read_stats('../inputs/inputs_day12_test.txt', test_input=False)
m = read_stats('../inputs/inputs_day12.txt', test_input=False)
print(f'Input matrix = {m}')
start, end = find_start_end(m)

print(f'Start point: {start}, end point = {end}')

part1_res = find_shortest_path(m, start_point=start, end_point=end, debug=True)
print(f'Part1 result = {part1_res}')

print('----------------------------')

start_points = find_starting_points(m)
print(f' Part2 starting points {start_points}')

global_shortest_path = m.shape[0]*m.shape[1]
for i,start in enumerate(start_points):
    print(f'  ..checking starting point {i} out of {len(start_points)} = {start}')
    cur_shortest_path = find_shortest_path(m, start_point=start, end_point=end)
    if cur_shortest_path < global_shortest_path:
        global_shortest_path = cur_shortest_path

print(f' Part2 result = {global_shortest_path}')
# # init matrix with max length
# min_route =  max_steps * np.ones(m.shape)
# min_route[start] = 0
# print(min_route)
#
# step=1
# where_to_go = [start]  #starting position
#
# while step <= max_steps:
#     next_steps = []
#     print(f'Step = {step}')
#     while len(where_to_go)>0:
#         cur_cell = where_to_go.pop()
#         cur_elem = m[cur_cell] if m[cur_cell]!='S' else 'a'
#         print(f'  Cur cell = {m[cur_cell]}')
#         for next_cell in get_next_step(m, cx_=cur_cell[0],cy_=cur_cell[1]):
#             print(f'    checking next cell = {next_cell}')
#             next_elem = m[next_cell] if m[next_cell] != 'E' else 'z'
#             if ord(next_elem)<=ord(cur_elem)+1:
#                 if min_route[next_cell]> min_route[cur_cell]+1:
#                     min_route[next_cell] = min_route[cur_cell]+1
#                     next_steps.append(next_cell)
#     where_to_go = next_steps
#     print(f'  Generated next steps: {where_to_go}')
#     print('---------------')
#     step +=1

