def get_crates(lines):
    # print('stack of crates:')
    # print(lines)
    # print(len(lines))

    # get indexes
    indexes = {}
    crates_ = []
    for i, elem in enumerate(lines[len(lines) - 1]):
        if elem != ' ':
            indexes[int(elem)] = i
            crates_.append([])
    # print(f' Indexes: {indexes}')
    # print(crates_)

    # get crates stacks
    for line in lines[:-1]:
        # print(line)
        for c in indexes.keys():
            v = ' '
            if len(line) > indexes[c]:
                v = line[indexes[c]]
            # print(v)
            if v != ' ':
                crates_[c - 1].append(v)

    print(f'crates: {crates_}')
    print('-----------')
    return crates_


def get_commands(lines):
    print(f'commands:')
    # print(lines)
    commands_ = []
    for elem in lines:
        s = elem.split(' ')
        count_, from_, to_ = int(s[1]), int(s[3]), int(s[5])
        commands_.append((count_, from_, to_))
        # print(from_, to_, count_)
    print(commands_)
    print('----------------------')
    return commands_


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    crates_ = []
    commands_ = []
    for i, line in enumerate(lines):
        if line == '':
            crates_ = get_crates(lines[0:i])
            commands_ = get_commands(lines[i + 1:])

    return crates_, commands_



# crates, commands = read_stats('../inputs/inputs_day5_test.txt')
crates, commands = read_stats('../inputs/inputs_day5.txt', test_input=False)

crates2 = crates.copy()
commands2 = commands.copy()

# PART 1 - REVERSE ORDER WHEN MOVING
print(f'original crates stack = {crates}')
for command in commands:
    c, f, t = command
    print(f'command = {c, f, t}')
    elems_to_move = crates[f-1][0:c]
    elems_to_move.reverse()
    from_new = crates[f-1][c:]
    to_new = elems_to_move + crates[t-1]
    crates[f-1] = from_new
    crates[t-1] = to_new
    print(f' elems to move {elems_to_move}')
    print(f'crates stack = {crates}')

rez1 = ''
for crate in crates:
    rez1 += crate[0]

# PART 2 - SAME ORDER WHEN MOVING
print(f'original crates stack = {crates2}')
for command in commands2:
    c, f, t = command
    print(f'command = {c, f, t}')
    elems_to_move = crates2[f-1][0:c]
    from_new = crates2[f-1][c:]
    to_new = elems_to_move + crates2[t-1]
    crates2[f-1] = from_new
    crates2[t-1] = to_new
    print(f' elems to move {elems_to_move}')
    print(f'crates stack = {crates2}')

rez2 = ''
for crate in crates2:
    rez2 += crate[0]

print(f'RESULT PART1 = {rez1}')
print(f'RESULT PART2 = {rez2}')
