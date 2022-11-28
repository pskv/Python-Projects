def checkio(numbers):
    tgt = numbers[-1]

    edges = []
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            if sum(map(lambda x: x[0]==x[1], zip(str(numbers[i]), str(numbers[j])))) == 2:
                edges.append((numbers[i], numbers[j]))

    paths = {numbers[0]: [numbers[0]]}

    while True:
        vert_l = sorted([(vert, paths.get(vert)) for vert in numbers if paths.get(vert)], key = lambda x:len(x[1]))
        if not vert_l:
            break
        vert = vert_l[0][0]

        while True:
            edge_l = list(filter(lambda x:vert in x, edges))
            if not edge_l:
                break
            edge = edge_l[0]

            dest = edge[abs(edge.index(vert)-1)]
            if not paths.get(dest) or len(paths[dest]) > len(paths[vert])+1:
                paths[dest] = paths[vert] + [dest]

            edges.remove(edge)

        numbers.remove(vert)

    return paths[tgt]

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([123, 991, 323, 321, 329, 121, 921, 125, 999]) == [123, 121, 921, 991, 999], "First"
    assert checkio([111, 222, 333, 444, 555, 666, 121, 727, 127, 777]) == [111, 121, 127, 727, 777], "Second"
    assert checkio([456, 455, 454, 356, 656, 654]) == [456, 454, 654], "Third, [456, 656, 654] is correct too"


