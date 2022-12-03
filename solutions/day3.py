def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines


input_stats = read_stats('../inputs/inputs_day3.txt')

s = 0
for elem in input_stats:
    l = (len(elem) + 1) // 2
    elem1 = elem[:l]
    elem2 = elem[-l:]
    common = set(elem1).intersection(set(elem2))
    c = ''.join(common).strip()
    print(elem, ' =', elem1, ' + ', elem2, ' [common=', c, ']')
    if c.isupper():
        r = ord(c) - ord('A') + 27
    else:
        r = ord(c) - ord('a') + 1
    s += r
    print(f'common = {c}, common\'s priority is = {r}')

print('=================== END OF PART1 =========================')

# PART2
sum2 = 0
for i, elem in enumerate(input_stats):
    if i % 3 == 0:
        s1 = elem
        s2 = input_stats[i + 1]
        s3 = input_stats[i + 2]
        common2 = set(s1).intersection(set(s2)).intersection(set(s3))
        c2 = ''.join(common2).strip()
        print(s1, ' ', s2, ' ', s3, ' [common=', c2, ']')
        r2 = 0
        if c2.isupper():
            r2 = ord(c2) - ord('A') + 27
        else:
            r2 = ord(c2) - ord('a') + 1
        sum2 += r2
        print(f'common\'s priority is {r2}')

print(f'result part1 = {s}')
print(f'result part2 = {sum2}')
