def checkio(first, second):
    return sum([sum(map(lambda x:int(''.join(x),2), zip(*[(str(int(s1) and int(s2)), str(int(s1) or int(s2)), str(int(s1 != s2))) for s2 in bin(second)[2:]]))) for s1 in bin(first)[2:]])
    # return [[(s1,s2) for s2 in bin(second)[2:]] for s1 in bin(first)[2:]]

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    print(checkio(4, 6))
    assert checkio(4, 6) == 38
    assert checkio(2, 7) == 28
    assert checkio(7, 2) == 18