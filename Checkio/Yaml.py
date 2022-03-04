def yaml(a):
    res = dict()
    for line in a.split("\n"):
        if line.count(':') > 0:
            ind = line[:line.index(':')]
            val_s = line[line.index(':')+2:].strip()
            if val_s in ['', 'null']:
                res[ind] = None
            elif val_s.lower() == 'true':
                res[ind] = True
            elif val_s.lower() == 'false':
                res[ind] = False
            elif val_s.isdigit():
                res[ind] = int(val_s)
            else:
                p = 0
                while True:
                    if p == len(val_s):
                        break
                    if val_s[p:p+1] == "\\":
                        p += 1
                    elif val_s[p] in ["'", '"']:
                        p += 1
                        continue
                    res[ind] = res.get(ind, '') + val_s[p]
                    p += 1
    return res


if __name__ == '__main__':
    print("Example:")
    print(yaml('name: "Bob Dylan"\n'
     'children: 6\n'
     'coding: "null" '))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert yaml('name: "Bob Dylan"\n'
     'children: 6\n'
     'coding: "null" ') == {'children': 6,
     'coding': 'null',
     'name': 'Bob Dylan'}

    print("Coding complete? Click 'Check' to earn cool rewards!")
