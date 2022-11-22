from typing import List, Tuple

def get_points(rect):
    points = set()
    for i in range(rect[0], rect[2]):
        for j in range(rect[1], rect[3]):
            points.add((i, j))
    return points

def rectangles_union(recs: List[Tuple[int]]) -> int:
    points = set()
    for rect in recs:
        points = points | (get_points(rect))
    return len(points)


if __name__ == '__main__':
    print("Example:")
    print(rectangles_union([
        (6, 3, 8, 10),
        (4, 8, 11, 10),
        (16, 8, 19, 11)
    ]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert rectangles_union([
        (6, 3, 8, 10),
        (4, 8, 11, 10),
        (16, 8, 19, 11)
    ]) == 33
    assert rectangles_union([
        (16, 8, 19, 11)
    ]) == 9
    assert rectangles_union([
        (16, 8, 19, 11),
        (16, 8, 19, 11)
    ]) == 9
    assert rectangles_union([
        (16, 8, 16, 8)
    ]) == 0
    assert rectangles_union([
    ]) == 0
    print("Coding complete? Click 'Check' to earn cool rewards!")
