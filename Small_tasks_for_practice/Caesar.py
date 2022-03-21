# https://stepik.org/lesson/277101/step/8?thread=solutions&unit=273851
import random

def caesar(text, key, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    alph = dict()
    for symb in enumerate(alphabet):
        alph[symb[1]] = symb[0]
    return ''.join([alphabet[(alph[symb.upper()]+key) % len(alphabet)] for symb in text if symb.upper() in alphabet])


# def bruteforce(text, alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
#     for i in range(1, len(alphabet)):
#         print(caesar(text, -i, alphabet))


def jarriquez_encryption(text, key, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ', reverse=False):
    alph = dict()
    direction = -1 if reverse else 1
    for symb in enumerate(alphabet):
        alph[symb[1]] = symb[0]
    pure_text = [symb for symb in text.upper() if symb in alphabet]
    key_text = str(key) * ((len(text) // len(str(key))) + 1)
    return ''.join(list(map(lambda x: alphabet[(alph[x[0]]+(int(x[1])*direction)) % len(alphabet)], zip(pure_text, key_text))))


def bruteforce(text, alphabet, key_len):
    # print([i for i in range(1, 10**key_len)])
    for i in range(1, 10 ** key_len):
        if 'АЛМАЗ' in jarriquez_encryption(text, '0'*(key_len-len(str(i)))+str(i), alphabet, reverse=True)\
                and 'ДАКОСТА' in jarriquez_encryption(text, '0'*(key_len-len(str(i)))+str(i), alphabet, reverse=True):
            print(i, jarriquez_encryption(text, '0'*(key_len-len(str(i)))+str(i), alphabet, reverse=True))
        # print(jarriquez_encryption(text, '0'*(key_len-len(str(i)))+str(i), alphabet, reverse=True))


def disc_generator(alphabet):
    res = list(alphabet)
    random.shuffle(res)
    return ''.join(res)

def jefferson_encryption(text, discs, step, reverse=False):
    l = [s.upper() for s in text if s.isalnum()]
    if reverse:
        step *= -1
    return ''.join([discs[i % len(discs)][(discs[i % len(discs)].index(l[i])+step) % len(discs[0])] for i in range(len(l))])


def kidds_encryption(text, reverse=False):
    cypher = {'e': '8', 't': ';', 'h': '4', 'o': '‡', 's': ')', 'n': '*', 'a': '5', 'i': '6', 'r': '(', 'f': '1',
              'd': '†', 'l': '0', 'm': '9', 'b': '2', 'y': ':', 'g': '3', 'u': '?', 'v': '¶', 'c': '-', 'p': '.'}
    if reverse:
        rev_cypher = dict([(cypher[i], i) for i in cypher])
        return text.translate(text.lower().maketrans(rev_cypher))
    for i in set(text.lower()):
        if i not in cypher:
            cypher[i] = None
    return text.lower().translate(str.maketrans(cypher))

# print(kidds_encryption('ethosnairfdlmbyguvcp'))
print(kidds_encryption('XxL ,L, LxX'))
print(kidds_encryption('000', True))

# dict = {"a": "123", "b": "456", "c": None}
# string = "abc"
# print(string.translate(string.maketrans(dict)))

# bruteforce('СТВМФКМХОСРОВФЖОВФКМЖКСВЛФРП', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
# source_text = 'ТЛБЛДУЭППТКЛФЧУВНУПБКЗИХТЛТТЫХНЛОИНУВЖММИНПФНПШОКЧЛЕРНТФНАХЖИДМЯКЛТУБЖИУЕЖЕАХЛГЩЕЕЪУВНГАХИЯШПЙАОЦЦПВТЛБФТТИИНДИДНЧЮОНЯОФВТЕАТФУШБЛРЮЮЧЖДРУУШГЕХУРПЧЕУВАЭУОЙБДБНОЛСКЦБСАОЦЦПВИШЮТППЦЧНЖОИНШВРЗЕЗКЗСБЮНЙРКПСЪЖФФШНЦЗРСЭШЦПЖСЙНГЭФФВЫМЖИЛРОЩСЗЮЙФШФДЖОИЗТРМООЙБНФГОЩЧФЖООКОФВЙСЭФЖУЬХИСЦЖГИЪЖДШПРМЖПУПГЦНВКБНРЕКИБШМЦХЙИАМФЛУЬЙИСЗРТЕС'
# bruteforce(source_text, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 6)
# 8610
# 31245
# 71283
# 86610
# print(jarriquez_encryption('У СУДЬИ ЖАРРИКЕСА ПРОНИЦАТЕЛЬНЫЙ УМ', 423, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', reverse=False))
# print(jarriquez_encryption('ЧУЦИЮЛКВУФКНЙУГУТССКЩДФИПЮРЯЛЦР', 423, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', reverse=True))
# print(jarriquez_encryption('UUNEFWKXKVUEECMDVLPRUQQYCYTIHWUKPZ',26101986, reverse=True))
# print('0'*2)
# print('АЛМАЗ' in '123АЛМАЗЗ')
# print(disc_generator('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))


# clear_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# n = 6
# text = 'Some encripted text'
# random.seed(42)
# discs = list()
# for i in range(n):
#     discs.append(disc_generator(clear_alphabet))
# print(jefferson_encryption(text, discs, 4, reverse=False))
# print(jefferson_encryption('NUXHUEVGQBIJJZNVI', discs, 4, reverse=True))