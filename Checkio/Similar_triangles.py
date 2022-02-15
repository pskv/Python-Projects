from math import sqrt
from typing import List, Tuple
Coords = List[Tuple[int, int]]

def dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


def similar_triangles(coords_1: Coords, coords_2: Coords) -> bool:
    t1 = sorted(list(map(lambda x: dist(*x), zip(coords_1, coords_1[1:] + coords_1[0:1]))))
    t2 = sorted(list(map(lambda x: dist(*x), zip(coords_2, coords_2[1:] + coords_2[0:1]))))
    if t1 == t2:
        return True
    if len(set(map(lambda x: x[0]/x[1], zip(t1, t2)))) == 1:
        return True
    return False


if __name__ == '__main__':
    print("Example:")
    print(similar_triangles([(0, 0), (1, 2), (2, 0)], [(2, 0), (4, 4), (6, 0)]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(3, 0), (4, 2), (5, 0)]) is True, 'basic'
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(3, 0), (4, 3), (5, 0)]) is False, 'different #1'
    assert similar_triangles([(0, 0), (1, 2), (2, 0)], [(2, 0), (4, 4), (6, 0)]) is True, 'scaling'
    assert similar_triangles([(0, 0), (0, 3), (2, 0)], [(3, 0), (5, 3), (5, 0)]) is True, 'reflection'
    assert similar_triangles([(1, 0), (1, 2), (2, 0)], [(3, 0), (5, 4), (5, 0)]) is True, 'scaling and reflection'
    assert similar_triangles([(1, 0), (1, 3), (2, 0)], [(3, 0), (5, 5), (5, 0)]) is False, 'different #2'
    print("Coding complete? Click 'Check' to earn cool rewards!")
