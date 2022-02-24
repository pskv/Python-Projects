def reverse_ascending(items):
    row = list()
    res_list = list()
    for i in range(len(items)):
        if i != 0 and items[i] <= items[i-1]:
            res_list += row[::-1]
            row.clear()
        row.append(items[i])
    if len(row) != 0:
        res_list += row[::-1]
    return res_list


if __name__ == '__main__':
    print("Example:")
    print(reverse_ascending([1, 1, 2]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert list(reverse_ascending([1, 2, 3, 4, 5])) == [5, 4, 3, 2, 1]
    assert list(reverse_ascending([5, 7, 10, 4, 2, 7, 8, 1, 3])) == [10, 7, 5, 4, 8, 7, 2, 3, 1]
    assert list(reverse_ascending([5, 4, 3, 2, 1])) == [5, 4, 3, 2, 1]
    assert list(reverse_ascending([])) == []
    assert list(reverse_ascending([1])) == [1]
    assert list(reverse_ascending([1, 1])) == [1, 1]
    assert list(reverse_ascending([1, 1, 2])) == [1, 2, 1]
    print("Coding complete? Click 'Check' to earn cool rewards!")
