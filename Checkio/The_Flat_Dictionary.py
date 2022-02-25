def flatten(dictionary):
    res_dict = dict()
    tmp = dict()
    for el in dictionary:
        if dictionary[el] == {}:
            res_dict[el] = ""
        elif isinstance(dictionary[el], dict):
            tmp = flatten(dictionary[el])
            for el2 in tmp:
                res_dict[el+"/"+el2] = tmp[el2]
        else:
            res_dict[el] = dictionary[el]
    return res_dict


if __name__ == '__main__':
    # test_input = {"key": {"deeper": {"more": {"enough": "value"}}}}
    # test_input = {"enough": "value", "123": {"k1": "v1", "k2": "v2"}}
    test_input = {"empty": {}}
    print(test_input)

    # a = list(map(lambda x: (x, test_input[x]), test_input))
    # print(a)
    # print(map(lambda x: {x: test_input[x]}, test_input))

    print(' Input: {}'.format(test_input))
    print('Output: {}'.format(flatten(test_input)))

    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert flatten({"key": "value"}) == {"key": "value"}, "Simple"
    assert flatten(
        {"key": {"deeper": {"more": {"enough": "value"}}}}
    ) == {"key/deeper/more/enough": "value"}, "Nested"
    assert flatten({"empty": {}}) == {"empty": ""}, "Empty value"
    assert flatten({"name": {
                        "first": "One",
                        "last": "Drone"},
                    "job": "scout",
                    "recent": {},
                    "additional": {
                        "place": {
                            "zone": "1",
                            "cell": "2"}}}
    ) == {"name/first": "One",
          "name/last": "Drone",
          "job": "scout",
          "recent": "",
          "additional/place/zone": "1",
          "additional/place/cell": "2"}
    print('You all set. Click "Check" now!')
