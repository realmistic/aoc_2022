def read_stats(filepath:str, test_input=True):
    text_file = open(filepath, 'r')
    lines = text_file.read().splitlines()
    lines.append("") # appending the last empty input to the file

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines

input_stats =  read_stats('../inputs/inputs_day1.txt')

max_val = 0
cur = 0
elves = []

for i, elem in enumerate(input_stats):
    if elem == '':
        if cur > max_val:
            max_val = cur
        elves.append(cur)
        print(f'{len(elves)} :current Elv carrying calories = {cur}, max Elv = {max_val}')
        cur = 0

    else:
        cur = int(elem) + cur

print(f'Max val = {max_val}')


print(f'Original list =  {elves}')
sorted_elfs = sorted(elves)
print('-----------------')
print(f'Sorted list of Elves: {sorted_elfs}')

top3 = sum(sorted_elfs[-3:])
print(f'Sum top 3 Elves carry = {top3}')
