from typing import List, Tuple
from math import sqrt


def is_intersect(circles):
    # print((circles[0][0] - circles[1][0])**2 + (circles[0][1] - circles[1][1])**2)
    # print((circles[0][2] + circles[1][2])**2)
    # print(min(circles[0][2], circles[1][2])**2)
    # print(max(circles[0][2], circles[1][2])**2)
    return (circles[0][0] - circles[1][0])**2 + \
           (circles[0][1] - circles[1][1])**2 < (circles[0][2] + circles[1][2])**2 and\
           sqrt((circles[0][0] - circles[1][0])**2 + (circles[0][1] - circles[1][1])**2) + \
           min(circles[0][2], circles[1][2]) > max(circles[0][2], circles[1][2])


def count_chains(circles: List[Tuple[int, int, int]]) -> int:
    lvl = 1
    group = list()
    group.append(circles[0])
    while True:
        cnt = 0
        other = list()
        for crcl in circles[1:]:
            if crcl in group:
                continue
            for el in group:
                if is_intersect([el]+[crcl]):
                    group.append(crcl)
                    cnt += 1
                    break
            if crcl not in group:
                other.append(crcl)
        if cnt == 0:
            break
    if len(other) > 0:
        lvl += count_chains(other)
    return lvl


if __name__ == '__main__':
    print("Example:")
    print(is_intersect([[0,8,4],[-2,9,3]]))

    # print(count_chains([[3,8,1],[-3,-7,3],[0,8,4],[7,-10,3],[-2,9,3],[-1,-9,2],[-9,2,2],[-6,2,3],[-2,4,2]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    # assert count_chains([(1, 1, 1), (4, 2, 1), (4, 3, 1)]) == 2, 'basic'
    # assert count_chains([(1, 1, 1), (2, 2, 1), (3, 3, 1)]) == 1, 'basic #2'
    # assert count_chains([(2, 2, 2), (4, 2, 2), (3, 4, 2)]) == 1, 'trinity'
    # assert count_chains([(2, 2, 1), (2, 2, 2)]) == 2, 'inclusion'
    # assert count_chains([(1, 1, 1), (1, 3, 1), (3, 1, 1), (3, 3, 1)]) == 4, 'adjacent'
    # assert count_chains([(0, 0, 1), (-1, 1, 1), (1, -1, 1), (-2, -2, 1)]) == 2, 'negative coordinates'
    print("Coding complete? Click 'Check' to earn cool rewards!")
