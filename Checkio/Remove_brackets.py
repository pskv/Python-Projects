def symb_type(symb):
    if symb == '(':
        return ('open', '()')
    if symb == '[':
        return ('open', '[]')
    if symb == '{':
        return ('open', '{}')
    if symb == ')':
        return ('close', '()')
    if symb == ']':
        return ('close', '[]')
    if symb == '}':
        return ('close', '{}')


def remove_brackets(line: str) -> str:
    res = str()
    symb_queue = {'()': [], '[]': [], '{}': []}
    # pairs = {'()': [], '[]': [], '{}': []}
    pairs = list()
    for i in range(len(line)):
        symb = line[i]
        s_type = symb_type(symb)
        if s_type[0] == 'open':
            symb_queue[s_type[1]] += [i]
        elif s_type[0] == 'close':
            if len(symb_queue[s_type[1]]) > 0:
                pairs.append([symb_queue[s_type[1]][-1], i, s_type[1]])
                symb_queue[s_type[1]].pop()
            elif len(list(filter(lambda x: x[2] == s_type[1], pairs))) > 0:
                # print(pairs)
                # print(s_type[1], list(sorted(filter(lambda x: x[2] == s_type[1], pairs))))
                pairs[pairs.index(list(sorted(filter(lambda x: x[2] == s_type[1], pairs)))[0])][1] = i
                # print(pairs)

    # print(pairs)

    while True:
        cnt_conf = 0
        max_conf = 0
        max_ind = int()
        for i in range(len(pairs)):
            for tgt_pair in pairs:
                if pairs[i] == tgt_pair:
                    continue
                if pairs[i][0] < tgt_pair[0] < pairs[i][1] and tgt_pair[1] > pairs[i][1] or\
                        pairs[i][0] < tgt_pair[1] < pairs[i][1] and tgt_pair[0] < pairs[i][0]:
                    cnt_conf += 1
            if cnt_conf > max_conf:
                max_conf = cnt_conf
                max_ind = i
            cnt_conf = 0
        if max_conf == 0:
            break
        pairs.pop(max_ind)
    # print(pairs)
    # print(sorted([ind[0] for ind in pairs]+[ind[1] for ind in pairs]))
    return ''.join(map(lambda x: line[x], sorted([ind[0] for ind in pairs]+[ind[1] for ind in pairs])))


if __name__ == "__main__":
    print("Example:")
    print(remove_brackets("[[{}()]]([{])}(]{"))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert remove_brackets("(()()") == "()()"
    assert remove_brackets("[][[[") == "[]"
    assert remove_brackets("[[(}]]") == "[[]]"
    assert remove_brackets("[[{}()]]") == "[[{}()]]"
    assert remove_brackets("[[[[[[") == ""
    assert remove_brackets("[[[[}") == ""
    assert remove_brackets("") == ""
    assert remove_brackets("[(])") == "()"
    print("Coding complete? Click 'Check' to earn cool rewards!")
