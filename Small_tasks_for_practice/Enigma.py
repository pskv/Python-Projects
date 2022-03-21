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


def enigma(text, ref, rot1, rot2, rot3):
    # res = ''
    # for symb in text:
    #     res += rotor(rotor(rotor(reflector(rotor(rotor(rotor(symb, rot3), rot2), rot1), ref), rot1, True), rot2, True), rot3, True)
    # return res
    return ''.join([rotor(rotor(rotor(reflector(rotor(rotor(rotor(symb, rot3), rot2), rot1), ref), rot1, True), rot2, True), rot3, True) for symb in text.upper() if symb.isalpha()])

# print(rotor('S', 3))
# print(reflector('Y', 1))
# print(enigma('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1, 1, 2, 3))
print(enigma('Some encripted text', 1, 1, 2, 3))