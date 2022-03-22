def list_pull(L):
    res_list = list()
    for el in L:
        if isinstance(el, list):
            res_list += list_pull(el)
        else:
            res_list.append(el)
    return(res_list)

def my_deepcopy(L):
    res_list = list()
    if isinstance(L, list):
        for el in L:
            res_list.append(my_deepcopy(el))
        return res_list
    return(L)


# print(*[['one'], [343, 2], [[9, 9, 9], [[666, 666], [[[[42]]]]]]])
# print(list_pull([['one'], [343, 2], [[9, 9, 9], [[666, 666], [[[[42]]]]]]]))
# print([] + ['one', 'two'])

L1 = [['one'], [343, 2], [[9, 9, 9], [[666, 666], [[[[42]]]]]]]
print(my_deepcopy(L1))