import copy
from typing import List


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    numbers_ = []
    for line in lines:
        numbers_.append(int(line))

    return numbers_


def get_l_r_siblings(l_: List[int], cur_pos_, move_count_):
    print(f' Finding siblings for elem {l_[cur_pos_]} that move to {move_count_} elems')
    new_pos_ = cur_pos_ + move_count_
    cnt_ = len(l_)
    left = 0
    right = 0
    if new_pos_ == 0:
        left = l_[cnt_ - 1]
        right = -1
        # return l_[cnt_ - 1], -1
    elif new_pos_ == cnt_ - 1:
        left = l_[cnt_ - 1]
        right = -1
        # return l_[cnt_ - 1], -1
    elif 0 < new_pos_ < cnt_ - 1:
        left = l_[new_pos_]
        right = l_[new_pos_ + 1]
        # return l_[new_pos_], l_[new_pos_ + 1]
    elif new_pos_ > cnt_ - 1:
        while new_pos_ > cnt_ - 1:
            new_pos_ -= cnt_
        left = l_[new_pos_]
        right = l_[new_pos_ + 1]
        # return l_[new_pos_], l_[new_pos_ + 1]
    elif new_pos_ < 0:
        left = l_[new_pos_ + cnt_ - 1]
        right = l_[new_pos_ + cnt_]
        # return l_[new_pos_ + cnt_ - 1], l_[new_pos_ + cnt_]

    if left == l_[cur_pos_]:
        if cur_pos_ == 0:
            left = -1
        else:
            left = l_[cur_pos_ - 1]

    if right == l_[cur_pos_]:
        if cur_pos_ == cnt_ - 1:
            right = -1
        else:
            right = l_[cur_pos_ + 1]

    return left, right


# numbers = read_stats('../inputs/inputs_day20_test.txt', test_input=False)
numbers = read_stats('../inputs/inputs_day20.txt', test_input=False)

print(f'Len input {len(numbers)}, min_number = {min(numbers)}, max_number = {max(numbers)}')

count = len(numbers)
stats = copy.deepcopy(numbers)

# print(f'Original stats: {stats}')
#
# s = []
# s.append([1, 2, -3, 3, -2, 0, 4])
# s.append([2, 1, -3, 3, -2, 0, 4])
# s.append([1, -3, 2, 3, -2, 0, 4])
# s.append([1, 2, 3, -2, -3, 0, 4])
# s.append([1, 2, -2, -3, 0, 3, 4])
# s.append([1, 2, -3, 0, 3, 4, -2])
# s.append([1, 2, -3, 0, 3, 4, -2])
# # s.append([1, 2, -3, 4, 0, 3, -2])

# for i, elem in enumerate(s):
#     x = numbers[i]
#     pos_x = elem.index(x)
#     print(f'find new pos for elem = {x} (pos={pos_x}) in array: {elem}')
#     print(f'  {get_l_r_siblings(elem, pos_x, x)}')


for i, number in enumerate(numbers):
    if number == 0:
        print(f' {number} does not move:')
        # print(", ".join([str(x) for x in stats]))
        continue

    l, r = get_l_r_siblings(stats, stats.index(number), number)
    print(f'  returned {l}, {r}')
    stats.remove(number)
    if l == -1:
        stats.insert(0, number)
    elif r == -1:
        stats.append(number)
    else:
        stats.insert(stats.index(r), number)

    print(f'{i + 1}/{count} : {number} moves between {l} and {r}:')
    # print(", ".join([str(x) for x in stats]))

zero_pos = stats.index(0)

part1 = [stats[(zero_pos + x) % count] for x in [1000, 2000, 3000]]
print(f'Part 1 values = {part1}, sum={sum(part1)}')
#
# print(stats[(zero_pos + 1000) % count])
# print(stats[(zero_pos + 2000) % count])

# print(get_l_r_siblings(stats, 1, -3))

#
# for i, number in enumerate(numbers):
#     index = stats.index(number)
#     pos_insert = index + number + 1
#     if index + number < 0:
#         pos_insert += count - 1
#     if pos_insert > count - 1:
#         print('asd')
#         pos_insert = pos_insert % count
#     # if index + number > 0:
#     # if index >= (index + number + 1):
#     # pos_insert = index + number
#     # else:
#     #     pos_insert = (index + number + count - 1)
#
#     stats.insert(pos_insert, number)
#     print(
#         f' {i + 1}/{count} Insert elem {number} located at pos {index} before elem at pos {pos_insert}: {",".join([str(x) for x in stats])}')
#
#     indices = [i for i, x in enumerate(stats) if x == number]
#     if indices[0] == pos_insert:
#         stats.pop(indices[1])
#     else:
#         stats.pop(indices[0])
#
#     print(f' {i + 1}/{count} remove elem {number} at index {index}: {",".join([str(x) for x in stats])}')

# if index + number != 0:
#     stats.insert(index + number, number)
# elif index + number > len(numbers):
#     stats.insert((index + number) % len(numbers))
# else:
# stats.insert(len(numbers) - 1, number)

# if index + number + 1 > 0:
#     stats.insert(index + number, number)
# else:
#     stats.insert(index + number - 1, number)

# print(f'  NEW array: {",".join([str(x) for x in stats])}')
