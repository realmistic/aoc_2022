import numpy as np

def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')




    return lines

def construct_field(inputs_, is_part2=False, how_much_wider = 0):
    points = []

    for line in inputs_:
        s = [x.split(',') for x in line.split('->')]
        for e in s:
            points.append([int(x) for x in e])

    # for a,b in points:
    #     print(a,b)
    print(f'Length points = {len(points)}')
    print(f'Length lines = {len(inputs_)}')
    min_x, max_x = min([a for a, b in points]), max([a for a, b in points])
    min_y, max_y = min([b for a, b in points]), max([b for a, b in points])
    range_x = max_x-min_x
    range_y = max_y-min_y
    print(f' MIN - MAX for X: {min_x}, {max_x}, range_X = {range_x}')
    print(f' MIN - MAX for Y: {min_y}, {max_y}, range_Y = {range_y}')

    if is_part2:
        X = np.zeros((max_x - min_x + 1 + how_much_wider, max_y + 3), str)

    else: #part1
        X = np.zeros((max_x - min_x + 1, max_y + 1), str)

    for i in range(len(X)):
        for j in range(len(X[i])):
            X[i, j] = '.'

    if is_part2: #additional line for part2
        for i in range(max_x-min_x+1 + how_much_wider):
            X[i, max_y+2] = '#'
        min_x = min_x - how_much_wider // 2   #this is for the correct initial shift

    for line in inputs_:
        s = [x.split(',') for x in line.split('->')]
        for i in range(len(s) - 1):
            a_x, a_y = [int(x) for x in s[i]]
            b_x, b_y = [int(x) for x in s[i + 1]]
            print(a_x, a_y, b_x, b_y, '==>', a_x - min_x, a_y - min_y, b_x - min_x, b_y - min_y)

            if a_x == b_x:
                if a_y <= b_y:
                    for p in range(b_y - a_y + 1):
                        X[a_x - min_x, a_y + p  ] = '#'
                else:
                    for p in range(a_y - b_y + 1):
                        X[a_x - min_x, b_y + p ] = '#'

            if a_y == b_y:
                if a_x <= b_x:
                    for p in range(b_x - a_x + 1):
                        X[a_x + p - min_x, a_y ] = '#'
                else:
                    for p in range(a_x - b_x + 1):
                        X[b_x + p - min_x, a_y ] = '#'

    sand_ = (500 - min_x , 0)

    return X.T, sand_



def print_field(field_):
    for i in range(len(field_)):
        for j in range(len(field_[i])):
            print(field_[i, j], end='')
        print()
    return

def drop_sand(field_:np.matrix, start_sand_):
    max_x, max_y = field_.shape
    next_down = (start_sand_[0]+1, start_sand_[1])
    next_diag_left = (start_sand_[0] + 1, start_sand_[1]-1)
    next_diag_right = (start_sand_[0] + 1, start_sand_[1]+1)

    if next_down[0]<max_x and field_[next_down] == '.':
        return drop_sand(field_,next_down)
    elif next_diag_left[0]<max_x and next_diag_left[1]>=0 and field_[next_diag_left] == '.':
        return drop_sand(field_, next_diag_left)
    elif next_diag_right[0]<max_x and next_diag_right[1]<max_y and field_[next_diag_right] == '.':
        return drop_sand(field_, next_diag_right)

    if next_down[0]>=max_x:
        return -1,-1
    if next_diag_left[1]<0 or next_diag_right[1]>=max_y:
        return -1,-1

    # can't move --> return start_sand_
    return start_sand_


# inputs = read_stats('../inputs/inputs_day14_test.txt', test_input=True)
inputs = read_stats('../inputs/inputs_day14.txt', test_input=False)

field, sand_starting_point = construct_field(inputs, is_part2=False)
print(f'Initial state field: shape = {field.shape}')
print(sand_starting_point)
print_field(field)

print('============================')

# ============================= Part1 ===============================
start = (0,sand_starting_point[0])

cnt = 0
while cnt<1e6:
    print(f'Step = {cnt+1}')
    landed = drop_sand(field,start)

    if landed[0]==-1 and landed[1]==-1:
        break

    field[landed]='o'
    # print(landed)
    # print_field(field)
    cnt+=1

print('============')
print('End state ')
print_field(field)
part1_rez = cnt
print(f'Part1 rez = {cnt}')


print('*************************************************************')
# ============================= Part2 ===============================
print('Part2')

# !!! ITERATE WITH how_much_wider ==> start from 10 to ... doubling down --> normally to range_Y*2 max

field, sand_starting_point = construct_field(inputs, is_part2=True, how_much_wider=400)
print(f'Initial state field: shape = {field.shape}')
print(sand_starting_point)
# print_field(field)

start = (0,sand_starting_point[0])

cnt = 0
part2_rez = 0
while cnt<1e6:
    # print(f'Step = {cnt+1}')
    landed = drop_sand(field,start)

    if landed[0]==start[0] and landed[1]==start[1]:
        print('WoW WoW -- reached needed capacity!! ==> can print the result!')
        cnt += 1
        part2_rez = cnt
        break

    if landed[0]==-1 and landed[1]==-1:
        break

    field[landed]='o'
    cnt+=1

print('============')
print('End state ')

print(f'Part1 rez = {part1_rez}')

if part2_rez != 0:
    print(f'Part2 rez = {part2_rez}')
else:
    print(f'Continue to play with how_much_wider param making it bigger --> need wider field to find the answer!')