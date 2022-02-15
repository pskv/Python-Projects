def unix_match(filename: str, pattern: str) -> bool:
    name_pos = 0
    pat_pos = 0
    prev_star_pos = -1
    is_equal = set()
    while True:
        star_pos = pattern.find('*', pat_pos)
        if prev_star_pos == -1 and star_pos == -1:
            for i in range(len(pattern)):
                if filename[i] != pattern[i] and pattern[i] != '?':
                    return False
            return True
        if prev_star_pos == -1 and star_pos != pat_pos:
            for i in range(star_pos):
                if i == len(filename):
                    return False
                if filename[i] != pattern[i] and pattern[i] != '?':
                    return False
            pat_pos = star_pos + 1
            name_pos += star_pos
            prev_star_pos = star_pos
        elif star_pos == pat_pos:
            prev_star_pos = star_pos
            pat_pos += 1
            if pat_pos >= len(pattern):
                return True
        elif star_pos == -1:
            for i in range(pat_pos - len(pattern), 0):
                if filename[i] != pattern[i] and pattern[i] != '?':
                    return False
            return True
        else:
            for i in range(name_pos, len(filename)):
                is_equal.clear()
                for j in range(star_pos - pat_pos):
                    if filename[i+j] != pattern[pat_pos+j] and pattern[pat_pos+j] != '?':
                        is_equal.add(False)
                        break
                    is_equal.add(filename[i+j] == pattern[pat_pos+j] or pattern[pat_pos+j] == '?')
                if True in is_equal and len(is_equal) == 1:
                    pat_pos = star_pos + 1
                    name_pos = i + 1
                    break
            if False in is_equal or len(is_equal) > 1:
                return False


if __name__ == '__main__':
    print("Example:")
    print(unix_match("txt", "????*"))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert unix_match('somefile.txt', '*') == True
    assert unix_match('other.exe', '*') == True
    assert unix_match('my.exe', '*.txt') == False
    assert unix_match('log1.txt', 'log?.txt') == True
    assert unix_match('log12.txt', 'log?.txt') == False
    assert unix_match('log12.txt', 'log??.txt') == True
    print("Coding complete? Click 'Check' to earn cool rewards!")
