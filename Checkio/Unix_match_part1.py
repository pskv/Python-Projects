def compare_part(text, pat):
    pat_pos = 0
    for i in range(len(text)):
        if pat_pos >= len(pat):
            return -1
        if pat[pat_pos] == '[' and pat[pat_pos:pat_pos+3] != '[!]':
            if pat[pat_pos + 1] == '!':
                if text[i] in pat[pat_pos + 2:pat.index(']', pat_pos + 2)]:
                    return -1
            else:
                if text[i] not in pat[pat_pos + 1:pat.index(']', pat_pos + 1)]:
                    return -1
            pat_pos = pat.index(']', pat_pos + 2)
        elif pat[pat_pos] == '*' and pat_pos == len(pat)-1:
            return i
        elif text[i] != pat[pat_pos] and pat[pat_pos] != '?':
            return -1
        pat_pos += 1
    if pat_pos < len(pat):
        return -1
    return i


def unix_match(filename: str, pattern: str) -> bool:
    f_res = 0
    name_pos = 0
    pat_pos = 0
    prev_star_pos = -1
    # is_equal = set()
    while True:
        star_pos = pattern.find('*', pat_pos)
        if prev_star_pos == -1 and star_pos == -1:
            f_res = compare_part(filename, pattern)
            if f_res == -1:
                return False
            else:
                return True
        elif prev_star_pos == -1 and star_pos != pat_pos:
            f_res = compare_part(filename, pattern[pat_pos:star_pos+1])
            if f_res == -1:
                return False
            prev_star_pos = star_pos
            pat_pos = star_pos + 1
            name_pos += f_res
            continue
        elif star_pos == pat_pos:
            prev_star_pos = star_pos
            pat_pos += 1
            if pat_pos >= len(pattern):
                return True
        elif star_pos == -1:
            for i in range(name_pos, len(filename)):
                f_res = compare_part(filename[i:], pattern[pat_pos:])
                if f_res != -1:
                    return True
            return False
        else:
            for i in range(name_pos, len(filename)):
                f_res = compare_part(filename[i:], pattern[pat_pos:star_pos+1])
                if f_res != -1:
                    pat_pos = star_pos + 1
                    name_pos = i + f_res
                    break
            if f_res == -1:
                return False


if __name__ == '__main__':
    print("Example:")
    # print(unix_match('2211name[.txt', '22*1*1[123na]ame[!].t?t'))
    # print(unix_match('1name.txt', '1*[123na]me*t'))
    print(unix_match("[!]check.txt", "[!]check.txt"))

    # These "asserts" are used for self-checking and not for an auto-testing
    # assert unix_match('somefile.txt', 'somefile.txt') == True
    # assert unix_match('1name.txt', '[!abc]name.txt') == True
    # assert unix_match('log1.txt', 'log[!0].txt') == True
    # assert unix_match('log1.txt', 'log[1234567890].txt') == True
    # assert unix_match('log1.txt', 'log[!1].txt') == False
    # print("Coding complete? Click 'Check' to earn cool rewards!")
