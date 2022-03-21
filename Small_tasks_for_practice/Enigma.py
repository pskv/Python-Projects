rdict = {1: ('AELTPHQXRU', 'BKNW', 'CMOY', 'DFG', 'IV', 'JZ', 'S'),
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

def rotor(symbol, n, reverse=False):
    if n == 0:
        return symbol
    for seq in rdict[n]:
        if symbol in seq:
            seq_len = len(seq)
            if reverse:
                pos = seq.index(symbol)-1
            else:
                pos = (seq.index(symbol)+1) % seq_len
            return seq[pos]


print(rotor('S', 3))