from typing import List


def get_all_mirrors(n):
    res = set()
    res.add(n)
    res.add(n % 8 * 8 + 7 - n // 8)
    res.add((7 - n // 8)*8+(7 - n % 8))
    res.add((7 - n % 8) * 8 + (n // 8))
    return res


def rotate_grille(grille, nr=0):
    ratio = len(grille)
    for n in range(nr % ratio):
        res = [['.' for _ in range(ratio)] for _ in range(ratio)]
        for i in range(ratio):
            for j in range(ratio):
                res[i][j] = grille[ratio-1-j][i]
        grille = list(map(lambda x: ''.join(x), res))
    return grille


def apply_grille(plaintext: str, grille: List[str]):
    res = [['' for _ in range(8)] for _ in range(8)]
    pointer = 0
    for k in range(4):
        for i in range(8):
            for j in range(8):
                if rotate_grille(grille, k)[i][j] == 'X':
                    res[i][j] = plaintext[pointer]
                    pointer += 1
    return ''.join(list(map(lambda x: ''.join(x), res)))


def find_grille(plaintext: str, cryptogram: str) -> List[str]:
    angle = sorted([(i, sum(
                            [(plaintext[0:i * 16]+plaintext[i * 16 + 16:]).count(plaintext[i*16+j]) for j in range(16)]
                            )) for i in range(4)], key=lambda x: (x[1], x[0]))[0][0]
    res = [cryptogram.find(plaintext[angle*16])]
    used_cells = get_all_mirrors(res[0])

    i = 1
    while True:
        idx = cryptogram.find(plaintext[angle*16+i], res[i]+1 if len(res) > i else res[i-1]+1)

        if idx == -1:
            if i < len(res):
                res.pop()
            i -= 1
            used_cells -= get_all_mirrors(res[i])
            continue

        if len(res) <= i:
            res.append(idx)
        else:
            res[i] = idx

        if idx in used_cells:
            continue

        used_cells |= get_all_mirrors(idx)

        i += 1
        if i == 16:
            gr = rotate_grille([''.join(['X' if (i*8+j) in res else '.' for j in range(8)]) for i in range(8)], 4-angle)
            if cryptogram == apply_grille(plaintext, gr):
                return gr
            i -= 1
            used_cells -= get_all_mirrors(res[-1])
    return []


if __name__ == "__main__":

    print(find_grille("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb",
                      "ababaaaababbbbbaaaaaaaaaaabaaaaaaabbaaabaabaaaaaaaaaaaaababaabaa"))
    print(find_grille("ccccccccccccccccccccccccccccccccccccdddddddddddddddddddddddddddd",
                      "dcdccdccccccccdcdccddddcdccddcdcdcdccddcdccccddcccdccdcdddcddcdc"))
    print(find_grille("lllllllllllllllllllllllllllllllllllllllllllllllllllllmmmmmmmmmmm",
                      "lllllllllllllllllllllmllllllmmllllllllmmllllllmmmmllllllmmllllll"))
