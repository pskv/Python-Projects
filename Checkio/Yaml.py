def get_val(txt):
    if txt in ['', 'null']:
        return None
    elif txt in {'true','false'}:
        return txt == 'true'
    if txt[0] in {"'",'"'}:
        txt = eval(txt)
    else:
        txt = txt.partition(' #')[0]
    if txt.isdigit():
        return int(txt)
    else:
        return txt
    pass


def yaml(a):
    if not a:
        return None
    res = []
    lines = a.split("\n")
    lid = 0
    while True:
        if lid == len(lines):
            break
        if not lines[lid].strip() or not lines[lid].strip().partition('#')[0]:
            lid += 1
            continue
        if lines[lid].strip()[0] == '-':
            if not lines[lid].strip()[1:].partition('#')[0]:
                sub_a = ''
                while True:
                    lid += 1
                    if lid == len(lines):
                        res.append(yaml(sub_a[:-1]))
                        break
                    if not lines[lid].strip() or not lines[lid].strip().partition('#')[0]:
                        continue
                    if lines[lid][0:2] == '  ':
                        sub_a += lines[lid][2:]+'\n'
                    else:
                        res.append(yaml(sub_a[:-1]))
                        break
            else:
                res.append(get_val(lines[lid][2:].strip()))
                lid += 1
        else:
            if isinstance(res, list):
                res = {}
            key, sign, value = lines[lid].partition(':')
            if not value:
                sub_a = ''
                while True:
                    lid += 1
                    if lid == len(lines):
                        res[key] = yaml(sub_a[:-1])
                        break
                    if not lines[lid].strip() or not lines[lid].strip().partition('#')[0]:
                        continue
                    if lines[lid][0:2] == '  ':
                        sub_a += lines[lid][2:]+'\n'
                    else:
                        res[key] = yaml(sub_a[:-1])
                        break
            else:
                res[key] = get_val(value.strip())
                lid += 1
    return res


if __name__ == '__main__':
    # {'age': 14,
    #  'name': 'Alex',
    #  'study': [{'num': 89,
    #             'type': 'school'},
    #            {'num': 12,
    #             'type': 'school'}]}

    print(yaml('name: Alex\n'
 'study:\n'
 '  -\n'
 '    type: school\n'
 '    num: 89\n'
 '  -\n'
 '    type: school\n'
 '    num: 12\n'
 'age: 14'))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert yaml('- Alex\n'
 '-\n'
 '  - odessa\n'
 '  - dnipro\n'
 '- Li') == ['Alex', ['odessa', 'dnipro'], 'Li']
    assert yaml('- 67\n'
 '-\n'
 '  name: Irv\n'
 '  game: Mario\n'
 '-\n'
 '- 56') == [67,
 {'game': 'Mario', 'name': 'Irv'},
 None,
 56]
    assert yaml('name: Alex\n'
 'study:\n'
 '  type: school\n'
 '  number: 78\n'
 'age: 14') == {'age': 14,
 'name': 'Alex',
 'study': {'number': 78,
           'type': 'school'}}
    assert yaml('name: Alex\n'
 'study:\n'
 '  - 89\n'
 '  - 89\n'
 '  - "Hell"\n'
 'age: 14') == {'age': 14,
 'name': 'Alex',
 'study': [89, 89, 'Hell']}
    assert yaml('name: Alex\n'
 'study:\n'
 '  -\n'
 '    type: school\n'
 '    num: 89\n'
 '  -\n'
 '    type: school\n'
 '    num: 12\n'
 'age: 14') == {'age': 14,
 'name': 'Alex',
 'study': [{'num': 89,
            'type': 'school'},
           {'num': 12,
            'type': 'school'}]}
    assert yaml('name: Alex\n'
 'study:\n'
 '  -\n'
 '    type: school\n'
 '    nums:\n'
 '      - 12\n'
 '      - 67\n'
 '  -\n'
 '    type: school\n'
 '    num: 12\n'
 'age: 14') == {'age': 14,
 'name': 'Alex',
 'study': [{'nums': [12, 67],
            'type': 'school'},
           {'num': 12,
            'type': 'school'}]}
    print("Coding complete? Click 'Check' to earn cool rewards!")
