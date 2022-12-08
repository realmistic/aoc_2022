import numpy as np


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    matrix = []

    for line in lines:
        matrix.append([int(x) for x in line])

    return matrix


# check whether m[x,y] if visible from either side
def check_visible(m: np.matrix, x: int, y: int) -> bool:
    up = m[0:x, y]
    down = m[x + 1:m.shape[0], y]
    left = m[x, 0:y]
    right = m[x, y + 1:m.shape[1]]

    if m[x, y] > left.max() or m[x, y] > right.max() or m[x, y] > up.max() or m[x, y] > down.max():
        return True

    return False


def find_scenic_score(m: np.matrix, x: int, y: int) -> int:
    def how_many_less(val, l: list) -> int:
        count = 1
        if val > max(l):
            return len(l)

        for e in l:
            if e < val:
                count += 1
            else:
                break
        # debug: print(val, l, count)
        return count

    left = m[0:x, y]
    right = m[x + 1:m.shape[0], y]
    up = m[x, 0:y]
    down = m[x, y + 1:m.shape[1]]

    up_list = up.reshape(-1).tolist()[0][::-1]  # reverse order
    down_list = down.reshape(-1).tolist()[0]
    left_list = left.reshape(-1).tolist()[0][::-1]  # reverse order
    right_list = right.reshape(-1).tolist()[0]

    return how_many_less(m[x, y], up_list) * how_many_less(m[x, y], down_list) * \
           how_many_less(m[x, y], left_list) * how_many_less(m[x, y], right_list)


# input_stats = read_stats('../inputs/inputs_day8_test.txt', test_input=False)
input_stats = read_stats('../inputs/inputs_day8.txt', test_input=False)

# get the matrix
m = np.matrix(input_stats)
print(m)

cnt = 0
perimeter = (m.shape[0] + m.shape[1] - 2) * 2
max_scenic_score=0
for i in range(len(input_stats) - 1):
    for j in range(len(input_stats[i]) - 1):
        if 0 < i:
            if 0 < j:
                if check_visible(m, i, j):
                    cnt += 1

                ss = find_scenic_score(m, i, j)
                if ss > max_scenic_score:
                    max_scenic_score = ss
                # print(f' {m[i, j]}, is_visible = {check_visible(m, i, j)}')

print(f'Part1 result (visible trees): {cnt + perimeter}')
print(f'Part2 result (max scenic score): {max_scenic_score}')

# DEBUG
# x = 2
# y = 2
# up = m[0:x, y]
# down = m[x + 1:m.shape[0], y]
# left = m[x, 0:y]
# right = m[x, y + 1:m.shape[1]]
#
# print(up)
# up_list = up.reshape(-1).tolist()[0][::-1]  # reverse order
# print(up_list)
#
# print(down)
# down_list = down.reshape(-1).tolist()[0]
# print(down_list)
#
# print(left)
# left_list = left.reshape(-1).tolist()[0][::-1] # reverse order
# print(left_list)
#
# print(right)
# right_list = right.reshape(-1).tolist()[0]
# print(right_list)
