# import networkx as nx
from typing import List


# def cheapest_flight(costs: List, a: str, b: str) -> int:
#     G = nx.Graph()
#     for el in costs:
#         G.add_edge(el[0], el[1], cost=el[2])
#     try:
#         return nx.algorithms.shortest_paths.generic.shortest_path_length(G, a, b, "cost")
#     except:
#         return 0


def cheapest_flight(costs: List, a: str, b: str) -> int:
    min_cost = 0
    for i in range(len(costs)):
        if a in costs[i][0:2]:
            if b in costs[i][0:2]:
                if min_cost == 0 or costs[i][2] < min_cost:
                    min_cost = costs[i][2]
            else:
                calc_cost = cheapest_flight(costs[0:i]+costs[i+1:], (costs[i][0] if costs[i][1] == a else costs[i][1]), b)  #  , costs[i][2])
                if calc_cost != 0 and (min_cost == 0 or calc_cost < min_cost):
                    min_cost = calc_cost + costs[i][2]
    return min_cost


if __name__ == '__main__':
    print("Example:")
    print(cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['D', 'F', 900]],
 'A',
 'F'))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['B', 'C', 50]],
 'A',
 'C') == 70
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['B', 'C', 50]],
 'C',
 'A') == 70
    assert cheapest_flight([['A', 'C', 40],
  ['A', 'B', 20],
  ['A', 'D', 20],
  ['B', 'C', 50],
  ['D', 'C', 70]],
 'D',
 'C') == 60
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['D', 'F', 900]],
 'A',
 'F') == 0
    assert cheapest_flight([['A', 'B', 10],
  ['A', 'C', 15],
  ['B', 'D', 15],
  ['C', 'D', 10]],
 'A',
 'D') == 25
    print("Coding complete? Click 'Check' to earn cool rewards!")
