def get_diff_ratio(line1,line2):
    if line1 == line2:
        return 0
    res = 0
    for i in range(max(len(line1), len(line2))):
        if i >= len(line1) or i >= len(line2) or line1[i] != line2[i]:
            res +=1
    return res

def steps_to_convert(line1, line2):
    min_diff_ratio = get_diff_ratio(line1, line2)
    cnt_steps = 0

    while True:
        curr_diff_ratio = min_diff_ratio

        for i in range(len(line1)):
            diff_ratio = get_diff_ratio(line1[:i]+line1[i+1:], line2)
            if diff_ratio < min_diff_ratio:
                min_diff_ratio = diff_ratio
                symb_idx = (1, i)
        for i in range(len(line2)):
            diff_ratio = get_diff_ratio(line2[:i]+line2[i+1:], line1)
            if diff_ratio < min_diff_ratio:
                min_diff_ratio = diff_ratio
                symb_idx = (2, i)

        if curr_diff_ratio == min_diff_ratio:
            break

        cnt_steps += 1
        if symb_idx[0] == 1:
            line1 = line1[:symb_idx[1]]+line1[symb_idx[1]+1:]
        else:
            line2 = line2[:symb_idx[1]] + line2[symb_idx[1] + 1:]

    return cnt_steps + curr_diff_ratio


if __name__ == "__main__":
    print(steps_to_convert("pline1", "lqqqine2v"))
    # print(steps_to_convert("lqqqine2v", "pline1"))
    print(steps_to_convert("l1i1n1e1", "1i2n2e2l"))
    # print(steps_to_convert("line1", "1enil"))

    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert steps_to_convert("line1", "line1") == 0, "eq"
    assert steps_to_convert("line1", "line2") == 1, "2"
    assert steps_to_convert("line", "line2") == 1, "none to 2"
    assert steps_to_convert("ine", "line2") == 2, "need two more"
    assert steps_to_convert("line1", "1enil") == 4, "everything is opposite"
    assert steps_to_convert("", "") == 0, "two empty"
    assert steps_to_convert("l", "") == 1, "one side"
    assert steps_to_convert("", "l") == 1, "another side"
    print("You are good to go!")