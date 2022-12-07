
# https://towardsdatascience.com/python-tree-implementation-with-bigtree-13cdabd77adc
from bigtree import Node, print_tree


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')
    return lines


def part1_total_sizes(node: Node):
    global small_dirs_size
    size = 0
    if node.type == 'dir':
        for e in node.children:
            size += part1_total_sizes(e)
        print(node.path, size)
        if size <= 100000:
            small_dirs_size += size
        node.size = size  # update dir size

    if node.type == 'file':
        size = node.size
    return size


def part2_find_dir_to_delete(node: Node, min_size: int):
    if node.type == 'file':
        return None
    else:  # this is dir
        min_dir = min([child.size for child in node.descendants if child.size >= min_size and child.type == 'dir'])
        return min_dir.size


# input_stats = read_stats('../inputs/inputs_day7_test.txt', test_input=True)
input_stats = read_stats('../inputs/inputs_day7.txt', test_input=True)


# init tree
small_dirs_size = 0
dirNodes = []

nodes = []
cur_path = ''
cur_node = ''
root = None  # root node

for elem in input_stats:
    print(elem)
    c = elem.split(' ')

    if elem == '$ cd /':
        root = Node('root', path='', type='dir')
        dirNodes.append(root)
        cur_path = '/'
        cur_node = root
        continue

    if elem.startswith('$ ls'):
        continue

    if elem.startswith('$ cd'):
        if c[2] == '..':
            cur_path = cur_node.parent.path
            cur_node = cur_node.parent
        elif c[2] == '/':
            continue
        else:
            # $ cd <dir_name>
            cur_path = cur_path + '/' + c[2]
            n = Node(c[2], path=cur_path, parent=cur_node, type='dir')
            dirNodes.append(n)
            cur_node = n
        continue

    if c[0] == 'dir':
        # already created the node earlier
        # n = Node(c[1], path=cur_path, parent=cur_node, type='dir')
        continue
    else:
        n = Node(c[1], path=cur_path, parent=cur_node, type='file', size=int(c[0]))
        continue

print_tree(root)

total_size = part1_total_sizes(root)
print(f'   Total size of files in root = {total_size}')
print(f' RESULT Part1 small dirs size = {small_dirs_size}')

min_dir_to_delete = 30000000-(70000000-total_size)
print(f'   Min dir size to delete = {min_dir_to_delete}')

dir_sizes = [d.size for d in dirNodes if d.size >= min_dir_to_delete]
print(f' All dirs sizes of candidates to delete above min size = {dir_sizes}')
print(f' RESULT Part2 min dir to delete = {min(dir_sizes)}')
