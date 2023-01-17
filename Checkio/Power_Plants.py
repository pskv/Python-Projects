from typing import Set, Tuple, List, Dict
import itertools
import collections


def power_plants(network: Set[Tuple[str, str]], ranges: List[int]) -> Dict[str, int]:

    # List of cities
    cities = set([i[j] for i in network for j in range(2)])

    # For every city determine and save the coverage of plant with every range from 1 to maximum range provided in "ranges" parameter
    coverage = list()
    coverage.append({c: {c} for c in cities})  # for 0 coverage every plant only covers the same city

    for i in range(1, max(ranges)+1):
        coverage.append({c: set([i[j] for i in network if (i[0] in coverage[-1][c]) or (i[1] in coverage[-1][c]) for j in range(2)]) for c in cities})

    # generator of plants locations for list of cities and range
    # returning locations from the biggest coverage to smallest
    def get_next_location(cities_l: set[str], rang: int):
        for cntr in sorted(collections.Counter(list(itertools.chain.from_iterable([list(i[1]) for i in coverage[rang].items() if i[0] in cities_l]))).items(), key=lambda x: -x[1]):
            yield cntr[0]


    # recursively find all locations
    ranges.sort(reverse=True)
    def get_all_locations(cities_l: set[str], ranges_l: List[int]):
        for loc in get_next_location(cities_l, ranges_l[0]):
            remaining_cities = cities_l - coverage[ranges_l[0]][loc]
            if len(remaining_cities) == 0:  # All cities are covered.
                return {loc: ranges_l[0]}

            if len(remaining_cities) and len(ranges_l) == 1:  # Not all cities are covered but only one plant left
                continue

            next_plant = get_all_locations(remaining_cities, ranges_l[1:])
            if next_plant:
                next_plant.update({loc: ranges_l[0]})
                return next_plant

        return dict()

    return(get_all_locations(cities, ranges))


if __name__ == '__main__':
    # print(power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')}, [1, 1]))
    assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')}, [2]) == {'C': 2}
    assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')}, [1, 1]) == {'B': 1, 'E': 1}
    assert power_plants({('A', 'B'), ('B', 'C'), ('A', 'D'), ('B', 'E')}, [1, 0]) == {'B': 1, 'D': 0}

    print('The local tests are done. Click on "Check" for more real tests.')
