rotdict = {1: ('AELTPHQXRU', 'BKNW', 'CMOY', 'DFG', 'IV', 'JZ', 'S'),
           2: ('FIXVYOMW', 'CDKLHUP', 'ESZ', 'BJ', 'GR', 'NT', 'A', 'Q'),
           3: ('ABDHPEJT', 'CFLVMZOYQIRWUKXSG', 'N'),
           4: ('AEPLIYWCOXMRFZBSTGJQNH', 'DV', 'KU'),
           5: ('AVOLDRWFIUQ', 'BZKSMNHYC', 'EGTJPX'),
           6: ('AJQDVLEOZWIYTS', 'CGMNHFUX', 'BPRK'),
           7: ('ANOUPFRIMBZTLWKSVEGCJYDHXQ'),
           8: ('AFLSETWUNDHOZVICQ', 'BKJ', 'GXY', 'MPR'),
           'beta': ('ALBEVFCYODJWUGNMQTZSKPR', 'HIX'),
           'gamma': ('AFNIRLBSQWVXGUZDKMTPCOYJHE'),
           }

refdict = { 1 : ('AY','BR','CU','DH','EQ','FS','GL','IP','JX','KN','MO','TZ','VW'),
           'C': ('AF','BV','CP','DJ','EI','GO','HY','KR','LZ','MX','NW','TQ','SU')
          }

rotations = {1: 17, 2: 5, 3: 22, 4: 10, 5: 0, 6: (0, 13)}

def rotor(symbol, n, reverse=False):
    if n == 0:
        return symbol
    for seq in rotdict[n]:
        if symbol in seq:
            seq_len = len(seq)
            if reverse:
                pos = seq.index(symbol)-1
            else:
                pos = (seq.index(symbol)+1) % seq_len
            return seq[pos]

def reflector(symbol, n):
    if n == 0:
        return symbol
    for seq in refdict[n]:
        if symbol in seq:
            return seq[(seq.index(symbol)+1) % 2]

def shift(symbol, n):
    return chr(((ord(symbol)+n-65) % 26)+65)

def check_commutation(pairs):
    used_symb = set()
    for pair in pairs.upper().split():
        if len(pair) != 2 or not pair.isalpha() or pair[0] in used_symb:
            return False
        used_symb.add(pair[0])
        if pair[1] in used_symb:
            return False
        used_symb.add(pair[1])
    return True

def commutation(symb, pairs):
    if symb in pairs.upper():
        pair = list(filter(lambda x: symb in x, pairs.upper().split()))[0]
        return pair[(pair.index(symb)+1) % 2]
    return symb


def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs=""):
    if not check_commutation(pairs):
        return "Извините, невозможно произвести коммутацию"
    res = ''
    for symb in text.upper():
        if symb.isalpha():
            if (shift2+1) % 26 in (rotations[rot2], ):
                shift1 = (shift1 + 1) % 26
                shift2 = (shift2 + 1) % 26
            shift3 = (shift3+1) % 26
            if shift3 in (rotations[rot3], ):
                shift2 = (shift2+1) % 26
            res += commutation(shift(rotor(shift(rotor(shift(rotor(shift(reflector(shift(rotor
            (shift(rotor(shift(rotor(shift(commutation(symb, pairs), shift3), rot3),
            shift2-shift3),rot2), shift1-shift2), rot1), -shift1), ref), shift1), rot1, True
            ), shift2 - shift1), rot2, True), shift3-shift2), rot3, True), -shift3), pairs)
    return res

# print(rotor('S', 3))
# print(reflector('Y', 1))
# print(enigma('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1, 1, 2, 3))
# print(enigma('AYIQQLXZMFHQUHQCH', 1, 1, -1, 2, 2, 3, -1))
# print(enigma('AAAAAAA', 1, 1, 0, 2, 0, 3, 0))
# print(enigma('AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA AAAAA', 1, 2, 3, 2, 3, 2, 3))
# print(enigma('BDZGOWC', 1, 1, 0, 2, 0, 3, 0))
# print(enigma('AAAAA AAAAA', 1, 1, 0, 2, 0, 1, 0))
# print(check_commutation('AC qw'))
# print(enigma('A', 1, 1, 0, 2, 0, 3, 0, 'AC QD'))
# print(commutation('A','AC QD RT YU'))
print(enigma('A', 1, 1, 0, 2, 0, 3, 0, 'AC qd'))