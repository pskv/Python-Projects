def repeat_inside(line: str) -> str:
    res = ''
    for i in range(len(line)):
        j = line.find(line[i], i+1)
        while j != -1:
            if line[j] == line[i]:
                pattern = line[i:j] if line[i:j] == line[j: j+j-i] else None
                if pattern:
                    k = 2
                    while True:
                        if pattern == line[i+k*(j-i): j+k*(j-i)]:
                            k += 1
                        else:
                            break
                    if (j-i)*k > len(res):
                        res = line[i:j+(j-i)*(k-1)]
                    j += (j-i)*(k-2)
            j = line.find(line[i], j + 1)
    return res


# print("Example:")
# print(repeat_inside("aaaaa"))
# print(repeat_inside("aabbff"))
# print(repeat_inside("aabababcc"))
print(repeat_inside("aababccababcc"))
print(repeat_inside("xabcdefghijxabcdefghi"))

# s = 'aababcc'
# print(s[:])

assert repeat_inside("aaaaa") == "aaaaa"
assert repeat_inside("aabbff") == "aa"
assert repeat_inside("aababcc") == "abab"
assert repeat_inside("abc") == ""
assert repeat_inside("abcabcabab") == "abcabc"

# print("The mission is done! Click 'Check Solution' to earn rewards!")
