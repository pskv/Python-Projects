from typing import List, Tuple, Iterable
import math

def get_edge_weight(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

def connect_stars(coords: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    groups = [tuple([i]) for i in range(len(coords))]
    res_tree = []
    while len(groups)>1:
        min_weight = -1
        min_weight_vert = ()
        min_weight_ind = ()
        for i in range(len(groups)):
            for j in range(i+1,len(groups)):

                for m in groups[i]:
                    for n in groups[j]:
                        weight = get_edge_weight(coords[m], coords[n])
                        if weight < min_weight or min_weight == -1:
                            min_weight = weight
                            min_weight_vert = (m, n)
                            min_weight_ind = (i, j)

        res_tree += [min_weight_vert]
        groups[min_weight_ind[0]] = tuple(set(min_weight_vert) | set(groups[min_weight_ind[0]]) | set(groups[min_weight_ind[1]]))
        del groups[min_weight_ind[1]]

    return res_tree


if __name__ == '__main__':

    print("Example:")
    # print(connect_stars([(6, 6), (6, 8), (8, 4), (3, 2)]))

    def sort_edges(edges): return sorted(map(lambda e: tuple(sorted(e)), edges))

    # These "asserts" are used for self-checking and not for an auto-testing
    # assert sort_edges(connect_stars([(1, 1), (4, 4)])) == [(0, 1)], '2 vertices'
    # assert sort_edges(connect_stars([(1, 1), (4, 1), (4, 4)])) == [(0, 1), (1, 2)], '3 vertices'
    assert sort_edges(connect_stars([(6, 6), (6, 8), (8, 4), (3, 2)])) == [(0, 1), (0, 2), (0, 3)], '4 vertices'
    assert sort_edges(connect_stars([(5, 4), (5, 1), (2, 6), (7, 2), (6, 9)])) == [(0, 2), (0, 3), (1, 3), (2, 4)], '5 vertices'
    assert sort_edges(connect_stars([(5, 8), (5, 1), (4, 2), (7, 6), (8, 6), (2, 2)])) == [(0, 3), (1, 2), (2, 3), (2, 5), (3, 4)], '6 vertices'
    assert sort_edges(connect_stars([(2, 7), (9, 9), (4, 9), (9, 6), (3, 3), (1, 6), (9, 7)])) == [(0, 2), (0, 5), (1, 2), (1, 6), (3, 6), (4, 5)], '7 vertices'
    print("Coding complete? Click 'Check' to earn cool rewards!")
