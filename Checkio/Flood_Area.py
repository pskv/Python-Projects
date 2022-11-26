from typing import Iterable

def max_lvl(diagram):
    res = 0
    max_res = 1
    for el in diagram:
        if el == '\\':
           res -= 1
        elif el == '/':
            res += 1
            if max_res == 1 or max_res<res:
                max_res = res
                if max_res == 0:
                    return max_res
    return max_res

def flood_area(diagram: str) -> Iterable[int]:
    res = []
    cnt_el = -1
    while True:
        cnt_el += 1
        if cnt_el>=len(diagram):
            break

        if diagram[cnt_el] != '\\':
            continue

        lvl = max_lvl(diagram[cnt_el:])

        if lvl == 1:
            break
        if lvl < 0:
            while True:
                cnt_el += 1
                if diagram[cnt_el] == '\\':
                    lvl += 1
                elif diagram[cnt_el] == '/':
                    lvl -= 1
                if lvl == 0:
                    break

        cur_res = 0
        while True:
            if diagram[cnt_el] == '\\':
                lvl -= 1
                cur_res += -lvl-1+0.5
            elif diagram[cnt_el] == '/':
                lvl += 1
                cur_res += -lvl+0.5
            else:
                cur_res += -lvl
            if lvl == 0:
                break
            cnt_el += 1
        res.append(int(cur_res))


    return res


if __name__ == '__main__':
    print("Example:")
    # print(list(flood_area(r'\\//')))
    # print(list(flood_area(r'\\//\\')))
    print(list(flood_area(r'/\\///\_/\/\\\\/_/\\///__\\\_\\/_\/_/')))
    # assert list(flood_area(r'\\//')) == [4], 'valley'
    # assert list(flood_area(r'/\\///\_/\/\\\\/_/\\///__\\\_\\/_\/_/')) == [4, 2, 1, 19, 9], 'mountains'
    # assert list(flood_area(r'_/_\_')) == [], 'hill'

    # print("Coding complete? Click 'Check' to earn cool rewards!")

