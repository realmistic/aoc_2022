def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines


# input_stats = read_stats('../inputs/inputs_day6_test.txt', test_input=False)
input_stats = read_stats('../inputs/inputs_day6.txt', test_input=False)

s = input_stats[0]

# part1
for i, e in enumerate(s):
    if len(set([s[i], s[i + 1], s[i + 2], s[i + 3]])) == 4:
        print(f'Part 1 answer = {i + 4}')
        break

# part2
for i, e in enumerate(s):
    if len(set(s[i:(i + 14)])) == 14:
        print(f'Part 2 answer = {i + 14}')
        break
