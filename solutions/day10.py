def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines

# input_stats = read_stats('../inputs/inputs_day10_test.txt', test_input=False)
input_stats = read_stats('../inputs/inputs_day10.txt', test_input=False)
print(input_stats)

def update_signal(cycle_:int, X_:int):
    print(f'    SIGNAL UPDATE: {cycle_}, local = {cycle_ * X_}')
    return cycle_ * X_


def execute_cycle(X_:int, current_row:str, all_rows)->str:
    pos_to_draw = len(current_row)
    # symbol_to_draw = ''
    if (X_-1)<=pos_to_draw<=(X_+1):
        current_row += '#'
    else:
        current_row += '.'

    if len(current_row) == 40:
        all_rows.append(current_row)
        print(current_row)
        current_row=''

    return current_row

#  ----------------------
#  part1
X = 1
cycle = 1
signal_strength_total = 0
signal_strength_local = 0

crt_row = ''
crt_image=[]

for line in input_stats:
    print(f'Command = {line}, X={X}, cycle_in_beginning={cycle}')

    if line == 'noop':
        c='noop'
        v=''
        crt_row = execute_cycle(X, crt_row, crt_image)

        if (cycle-20) % 40 ==0:
            signal_strength_total += update_signal(cycle,X)

        cycle += 1

    else:
        c, v = line.split(' ')

        crt_row = execute_cycle(X, crt_row, crt_image)
        crt_row = execute_cycle(X, crt_row, crt_image)

        if (cycle-20) % 40 ==0:
            signal_strength_total += update_signal(cycle,X)
        elif (cycle-19) % 40 ==0:
            signal_strength_total += update_signal(cycle + 1 , X)

        cycle += 2
        X += int(v)

print(f' PART1 rez = {signal_strength_total}')

print(f' PART2 rez (8 capital letters on the screen) = ')
for r in crt_image:
    print(r)