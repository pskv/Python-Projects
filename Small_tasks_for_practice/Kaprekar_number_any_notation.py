# https://stepik.org/lesson/180027/step/6?unit=154907

def find_symbol(n):
    if n < 10:
        return str(n)
    return chr(n+55)


def convert(num, to_base=10, from_base=10):
    res = ''
    src = int(str(num), from_base)
    if to_base == 10:
        return str(src)
    while src:
        modulo = src % to_base
        res += find_symbol(modulo)
        src //= to_base
    return res[::-1]


def kaprekar(n, base=10):
    sq = convert(int(str(n), base)**2, base)
    for i in range(1, len(sq)):
        if int(sq[i:], base) != 0 and convert(int(sq[:i], base) + int(sq[i:], base), base) == str(n):
            return True
    return False


print(kaprekar('38E', 16))