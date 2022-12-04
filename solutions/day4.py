def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines


input_stats = read_stats('../inputs/inputs_day4.txt')


# part1 function - if one inside another
def is_fully_contained(line):
    first, second = line.split(',')
    ax, ay = [int(x) for x in first.split('-')]
    bx, by = [int(x) for x in second.split('-')]
    # print(ax, ay, bx, by)
    if ax >= bx and ay <= by:
        return True
    if bx >= ax and by <= ay:
        return True
    return False


# part2 function - if there is an intersection
def is_overlap(line):
    first, second = line.split(',')
    ax, ay = [int(x) for x in first.split('-')]
    bx, by = [int(x) for x in second.split('-')]
    if ax <= bx <= ay:
        return True
    if bx <= ax <= by:
        return True
    return False


# solution
rez = [is_fully_contained(elem) for elem in input_stats]
rez_part2 = [is_overlap(elem) for elem in input_stats]

print(f'First 10 outcomes in Part1: {rez[0:10]}')
print(f'First 10 outcomes in Part2: {rez_part2[0:10]}')
print('--------------------------')
print(f'Part one result = {sum(rez)}')
print(f'Part two result = {sum(rez_part2)}')
