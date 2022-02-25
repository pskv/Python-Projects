def checkio(data):
    res = list()
    dist_letters = list(sorted(set(''.join(data))))
    for el in dist_letters:
        go_to_next_letter = False
        ind = 0
        greater_ind = -1
        for el2 in res:
            for el3 in data:
                if el3.count(el) > 0 and el3.count(el2) > 0:
                    if el3.index(el) < el3.index(el2):
                        res.insert(ind, el)
                        go_to_next_letter = True
                    if el3.index(el) > el3.index(el2):
                        greater_ind = res.index(el2) + 1
                    break
            if go_to_next_letter:
                break
            ind += 1
        if go_to_next_letter:
            continue
        if len(res) == 0 or greater_ind == ind or dist_letters.count(el) > 10:
            res.insert(ind, el)
        elif el != dist_letters[-1]:
            dist_letters.append(el)
    return ''.join(res)


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == "__main__":
    print(checkio(["qwerty","bjcfg","zxavd","ybgz"]))
    # assert checkio(["acb", "bd", "zwa"]) == "zwacbd", "Just concatenate it"
    # assert checkio(["klm", "kadl", "lsm"]) == "kadlsm", "Paste in"
    # assert (
    #     checkio(["a", "b", "c"]) == "abc"
    # ), "Cant determine the order - use english alphabet"
    # assert checkio(["aazzss"]) == "azs", "Each symbol only once"
    # assert checkio(["dfg", "frt", "tyg"]) == "dfrtyg", "Concatenate and paste in"
