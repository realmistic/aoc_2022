from ast import literal_eval
import copy

def read_stats(file_path: str, test_input: bool = True):

    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    return lines

def get_matching_bracket_pos(s_:str, pos_opening:int)->int:
    if s_[pos_opening] !='[':
        return -1
    cur_=1
    pos_ = pos_opening+1

    while cur_>0:
        # print(s_[pos_])
        if pos_>=len(s_):
            return -1
        if s_[pos_] == '[':
            cur_+=1
        if s_[pos_] == ']':
            cur_-=1
        pos_ += 1

    if cur_==0:
        return pos_-1
    else:
        return -1

def construct_list(input_:str):

    res = []

    print(f' construct list call from input ="{input_}" , len={len(input_)}')

    if len(input_)==0:
        return res

    str_ = input_

    while len(str_)>0:
        comma_pos = str_.find(',')
        close_pos_ = get_matching_bracket_pos(str_, 0)
        # print(f'close_pos = {close_pos_}, len_str = {len(str_)}')
        if close_pos_ == len(str_)-1:
            print(f' only one elem in {str_}')
            res = construct_list(str_[1:close_pos_])
            return res

        if comma_pos!=-1:
            print(f'case comma detected , str_={str_}, len={len(str_)}')
            if close_pos_ == -1:
                lst_=int(str_[0:comma_pos])
            else:
                lst_ = construct_list(str_[0:comma_pos])

            res.append(lst_)
            print(f'  appended list {lst_}')
            str_ = "".join(c for c in str_[comma_pos+1:])
            print(f' new str ={str_}')

        elif str_[0]=='[':
            close_pos_ = get_matching_bracket_pos(str_, 0)
            lst_ = construct_list(str_[1:close_pos_])
            res.append(lst_)

            str_ = str_[close_pos_+1:]
        #
        # if str_[0]=='[':
        #     close_pos_ = get_matching_bracket_pos(str_, 0)
        #     lst_ = construct_list(input_[1:close_pos_])
        #
        #     if close_pos_ == len(str_)-1:
        #         print(f'found ONLY one list {lst_}')
        #         return input_[1:close_pos_-1]
        #
        #     res.append(lst_)
        #     str_ = str_[close_pos_+2:]
        #     print(f'case open [ , new str_={str_}, len={len(str_)}')
        #
        # elif comma_pos!=-1: # there is at least one comma
        #     res.append(str_[:comma_pos])
        #     # cur_pos_ = comma_pos + 1
        #     str_ = str_[comma_pos+1:]
        #     print(f'case comma detected , new str_={str_}, len={len(str_)}')
        elif str_[0]==']':
            str_=''
        else: # only value
            res.append(int(str_))
            str_=''

    return res

def compare_lists(l1,l2):

    # two ints
    if isinstance(l1, int) and isinstance(l2, int):
        print(f'- Compare two ints {l1} vs {l2}')
        if l1 < l2:
            print(f'found solution: <')
            return '<'
        elif l1 == l2:
            return '='
        elif l1 > l2:
            print(f'found solution: >')
            return '>'

    # one integer another is list
    if isinstance(l1, int) and not isinstance(l2, int):
        print(f'- wrap the first param to list')
        elem = l1
        l1 = [elem]
        return compare_lists(l1, l2)

    # one integer another is list
    if not isinstance(l1, int) and isinstance(l2, int):
        print(f'- wrap the second param to list')
        elem = l2
        l2 = [elem]
        return compare_lists(l1, l2)

    if len(l1)==0:
        print(f'- empty list l1 ==> right order')
        return '<'
    if len(l2)==0:
        print(f'- empty list l2 ==> wrong order (>)')
        return '>'

    # two lists
    if not isinstance(l1, int) and not isinstance(l2, int):
        print(f'- Compare two lists {l1} vs {l2}')
        for i_ in range(len(l1)):
            if i_>=len(l2):
                return '>'
            print(f'- Compare {i_}th elem {l1[i_]} vs. {l2[i_]} (len l1={len(l1)}, len l2={len(l2)})')
            compare = compare_lists(l1[i_], l2[i_])
            if compare != '=':
                print(f'found solution: {compare}')
                return compare
        # walked till the end, first list ran out of elems
        if len(l1)<len(l2):
            return '<'

    return '='
# ------------------------
#         INPUTS

# inputs = read_stats('../inputs/inputs_day13_test.txt', test_input=True)
inputs = read_stats('../inputs/inputs_day13.txt', test_input=False)

lists = []

for inp in inputs:
    if inp=='':
        continue
    # l = construct_list(inp)
    l = literal_eval(inp)
    lists.append(l)
print(lists)

print(len(lists)//2)


trues = []
s= 0
for i in range(len(lists)//2):
    print(lists[2*i])
    print(lists[2*i+1])
    if compare_lists(lists[2*i], lists[2*i+1])=='<':
        trues.append(i+1)
        s+=i+1
    print('----------')

print(trues)
print(s)