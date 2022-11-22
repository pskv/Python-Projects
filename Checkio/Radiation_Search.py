def checkio(matrix):

    el_adrses = list()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            el_adrses.append((i,j))

    groups = []
    el_adr_chain = []

    while len(el_adrses) > 0:
        el_adr = el_adrses[0]

        el = matrix[el_adr[0]][el_adr[1]]
        el_adrses.remove(el_adr)
        if el == 0:
            continue

        el_adr_chain.append(el_adr)

        while True:

            if (el_adr[0]-1, el_adr[1]) in el_adrses and (el_adr[0]-1, el_adr[1]) not in el_adr_chain:
                ch_el = matrix[el_adr[0]-1][el_adr[1]]
                if ch_el == el:
                    el_adr_chain.append((el_adr[0]-1, el_adr[1]))
            if (el_adr[0]+1, el_adr[1]) in el_adrses and (el_adr[0]+1, el_adr[1]) not in el_adr_chain:
                ch_el = matrix[el_adr[0]+1][el_adr[1]]
                if ch_el == el:
                    el_adr_chain.append((el_adr[0]+1, el_adr[1]))
            if (el_adr[0], el_adr[1]-1) in el_adrses and (el_adr[0], el_adr[1]-1) not in el_adr_chain:
                ch_el = matrix[el_adr[0]][el_adr[1]-1]
                if ch_el == el:
                    el_adr_chain.append((el_adr[0], el_adr[1]-1))
            if (el_adr[0], el_adr[1]+1) in el_adrses and (el_adr[0], el_adr[1]+1) not in el_adr_chain:
                ch_el = matrix[el_adr[0]][el_adr[1]+1]
                if ch_el == el:
                    el_adr_chain.append((el_adr[0], el_adr[1]+1))

            if len(set(el_adr_chain) & set(el_adrses)) == 0:
                groups.append(list((len(el_adr_chain), el)))
                el_adr_chain.clear()
                break

            el_adr = list(set(el_adr_chain) & set(el_adrses))[0]
            el_adrses.remove(el_adr)

    groups.sort(reverse=True)
    return groups[0]

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([
        [1, 2, 3, 4, 5],
        [1, 1, 1, 2, 3],
        [1, 1, 1, 2, 2],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1]
    ]) == [14, 1], "14 of 1"

    assert checkio([
        [2, 1, 2, 2, 2, 4],
        [2, 5, 2, 2, 2, 2],
        [2, 5, 4, 2, 2, 2],
        [2, 5, 2, 2, 4, 2],
        [2, 4, 2, 2, 2, 2],
        [2, 2, 4, 4, 2, 2]
    ]) == [19, 2], '19 of 2'