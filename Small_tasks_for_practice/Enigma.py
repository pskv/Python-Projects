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

def shift(symbol, n):
    return chr(((ord(symbol)+n-65) % 26)+65)

# def enigma(text, ref, rot1, rot2, rot3):
#     return ''.join([rotor(rotor(rotor(reflector(rotor(rotor(rotor(symb, rot3), rot2), rot1), ref), rot1, True), rot2, True), rot3, True) for symb in text.upper() if symb.isalpha()])

def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3):
    return ''.join([shift(rotor(shift(rotor(shift
            (rotor(shift(reflector(shift(rotor(shift(rotor(shift(rotor(shift(symb, shift3), rot3
            ),shift2-shift3), rot2), shift1-shift2), rot1), -shift1), ref), shift1), rot1, True
             ), shift2 - shift1), rot2, True), shift3-shift2), rot3, True), -shift3)
            for symb in text.upper() if symb.isalpha()])


# print(rotor('S', 3))
# print(reflector('Y', 1))
# print(enigma('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1, 1, 2, 3))
print(enigma('Some encripted text', 1, 1, -1, 2, 2, 3, -1))