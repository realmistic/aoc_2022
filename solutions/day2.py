def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines


input_stats = read_stats('../inputs/inputs_day2.txt')

mapping = {
    'A X': 4,
    'A Y': 8,
    'A Z': 3,
    'B X': 1,
    'B Y': 5,
    'B Z': 9,
    'C X': 7,
    'C Y': 2,
    'C Z': 6
}

mapping_part2 = {
    'A X': 3,
    'A Y': 4,
    'A Z': 8,
    'B X': 1,
    'B Y': 5,
    'B Z': 9,
    'C X': 2,
    'C Y': 6,
    'C Z': 7
}

rez = 0
rez_part2 = 0

# quick solution
for elem in input_stats:
    # print(elem)
    # print(mapping[elem.replace('/n','')])
    rez += mapping[elem.replace('/n', '')]
    rez_part2 += mapping_part2[elem.replace('/n', '')]

print('Dumb solution')
print(f'result part1={rez}')
print(f'result part2={rez_part2}')
print('-----------------')

# elegant solution
# https://stackoverflow.com/questions/36329412/map-list-from-dictionaries
rez_v2 = sum(list(map(mapping.get, input_stats)))
rez_part2_v2 = sum(list(map(mapping_part2.get, input_stats)))

print('Elegant solution')
print(f'result part1={rez_v2}')
print(f'result part2={rez_part2_v2}')
print('-----------------')


