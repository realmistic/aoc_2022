def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines

def adjust_tail(h_, t_):
    need_tail_adj = False
    if h_[0] == t_[0] or h_[1] == t_[1]:
        return need_tail_adj, t_  # NO need to adj

    need_tail_adj = True  # need to adj tail - AND RECORD IT'S NEW POSITION
    # if abs(h_[0] - t_[0])== 1 or abs(h_[1] - t_[1]) == 1:
    #     need_tail_adj = True #need to adj tail - AND RECORD IT'S NEW POSITION

    if abs(h_[0] - t_[0]) > 1:
        if h_[1] > t_[1]:  # change the coord where the diff. is not 2!!
            t_[1] += 1
        else:
            t_[1] -= 1
    elif abs(h_[1] - t_[1]) > 1:
        if h_[0] > t_[0]:
            t_[0] += 1
        else:
            t_[0] -= 1
    return need_tail_adj, t_




# part1
def move_rope(rope, command_dir: str, command_steps: int, visited):

    head, tail = rope

    # debug
    # print(f'ROPE={rope}')
    # print(f' COMMAND DIR={command_dir}, COMMAND STEPS={command_steps}')

    while command_steps > 0:

        if command_dir == 'R':
            head[1] += 1
            adj, tail = adjust_tail(head, tail)
            if head[1] > tail[1] + 1:
                tail[1] += 1
                visited.append(tail.copy())
            command_steps -= 1
        elif command_dir == 'L':
            head[1] -= 1
            adj, tail = adjust_tail(head, tail)
            command_steps -= 1
            if head[1] < tail[1] - 1:
                tail[1] -= 1
                visited.append(tail.copy())
        elif command_dir == 'U':
            head[0] += 1
            adj, tail = adjust_tail(head, tail)
            command_steps -= 1
            if head[0] > tail[0] + 1:
                tail[0] += 1
                visited.append(tail.copy())

        elif command_dir == 'D':
            head[0] -= 1
            adj, tail = adjust_tail(head, tail)
            command_steps -= 1
            if head[0] < tail[0] - 1:
                tail[0] -= 1
                visited.append(tail.copy())

    # print(f'VISITED={visited}')
    # print('--------------------')

    return [head, tail], visited

# get max distance between 2 elems of the chain
def distance(elem1, elem2):
    return max(abs(elem1[0]-elem2[0]),abs(elem1[1]-elem2[1]))

# move rope_[elem_j] after rope_[elem_i], elem_j ALWAYS FOLLOWS elem_i
def do_move(rope_, elem_i, elem_j, command_dir):

    # sign = lambda x: (1, -1)[x < 0] # function sign :: https://stackoverflow.com/questions/1986152/why-doesnt-python-have-a-sign-function

    is_moved_tail = False

    head = rope_[elem_i]
    tail = rope_[elem_j]

    if distance(head,tail)<=1:  # do not move close enough knots ==> move only if the distance is 2
        return rope_, is_moved_tail

    if elem_j == len(rope_)-1:  # in this case we definitely move the tail
        is_moved_tail = True

    if head[0] > tail[0]:  # modelling the movement of a snake ==> tail always follows the head in the same direction
        tail[0] += 1
    elif head[0] < tail[0]:
        tail[0] -= 1

    if head[1] > tail[1]:
        tail[1] += 1
    elif head[1] < tail[1]:
        tail[1] -= 1

    return rope_, is_moved_tail

# part2
def move_long_rope(rope, command_dir: str, command_steps: int, visited):
    while command_steps>0:
        for i,elem in enumerate(rope): #check elem by elem
            if i==0:  # move head
                if command_dir == 'R':
                    elem[1] += 1
                elif command_dir == 'L':
                    elem[1] -= 1
                elif command_dir == 'U':
                    elem[0] += 1
                elif command_dir == 'D':
                    elem[0] -= 1
                print(f'    debug: {rope},  dir = {command_dir}, steps = {command_steps}, moved {i}')
            else: #other elems of chain
                if distance(rope[i-1], rope[i])>1:
                    rope, is_moved_tail = do_move(rope, i-1, i, command_dir)
                    print(f'    debug: {rope},  dir = {command_dir}, steps = {command_steps}, moved {i}')
                    if is_moved_tail:
                        visited.append(rope[len(rope)-1].copy())  #tail's new position
        command_steps -= 1
    return rope, visited

#part2 - model one move

# input_stats = read_stats('../inputs/inputs_day9_test.txt', test_input=False)
input_stats = read_stats('../inputs/inputs_day9.txt', test_input=False)
print(input_stats)

# ------------------------------------------
# part 1 solution
t = [1, 1]  # tail
h = [1, 1]  # head
r = [t, h]  # rope
v = [[1, 1]]  # visited

for line in input_stats:
    d, s_ = line.split(' ')  # direction
    s = int(s_)  # steps
    r, v = move_rope(r, d, s, v)

# remove duplicates in the visited points
map_visited = {}
for e in v:
    if str(e) in map_visited:
        map_visited[str(e)] += 1
    else:
        map_visited[str(e)] = 1

# print(map_visited)
print(f'PART 1 result (visited different points on the map) =  {len(map_visited.keys())}')
print('-----------------------------------------------------------------------------------')
# ------------------------------------------
# part 2 solution
r = [[1, 1] for _ in range(10)]  # rope
v = [[1, 1]]  # visited
print(f'Initial state of the rope = {r}')

step=0
for line in input_stats:
    step += 1
    print(f' STEP NO {step},  command = {line}')

    d, s_ = line.split(' ')  # direction
    s = int(s_)  # steps
    r,v = move_long_rope(r,d,s, v)

    print(f'     NEW ROPE = {r}')
    print(f'     NEW VISITED = {v}')
    print(f'==================')

# remove duplicates in the visited points
map_visited = {}
for e in v:
    if str(e) in map_visited:
        map_visited[str(e)] += 1
    else:
        map_visited[str(e)] = 1

print(f'PART 2 result (visited different points on the map) =  {len(map_visited.keys())}')
print('-----------------------------------------------------------------------------------')