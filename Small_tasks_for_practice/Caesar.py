# https://stepik.org/lesson/277101/step/8?thread=solutions&unit=273851

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



# bruteforce('СТВМФКМХОСРОВФЖОВФКМЖКСВЛФРП', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')


source_text = 'ТЛБЛДУЭППТКЛФЧУВНУПБКЗИХТЛТТЫХНЛОИНУВЖММИНПФНПШОКЧЛЕРНТФНАХЖИДМЯКЛТУБЖИУЕЖЕАХЛГЩЕЕЪУВНГАХИЯШПЙАОЦЦПВТЛБФТТИИНДИДНЧЮОНЯОФВТЕАТФУШБЛРЮЮЧЖДРУУШГЕХУРПЧЕУВАЭУОЙБДБНОЛСКЦБСАОЦЦПВИШЮТППЦЧНЖОИНШВРЗЕЗКЗСБЮНЙРКПСЪЖФФШНЦЗРСЭШЦПЖСЙНГЭФФВЫМЖИЛРОЩСЗЮЙФШФДЖОИЗТРМООЙБНФГОЩЧФЖООКОФВЙСЭФЖУЬХИСЦЖГИЪЖДШПРМЖПУПГЦНВКБНРЕКИБШМЦХЙИАМФЛУЬЙИСЗРТЕС'
bruteforce(source_text, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 6)

# 8610
# 31245
# 71283
# 86610

# print(jarriquez_encryption('У СУДЬИ ЖАРРИКЕСА ПРОНИЦАТЕЛЬНЫЙ УМ', 423, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', reverse=False))
# print(jarriquez_encryption('ЧУЦИЮЛКВУФКНЙУГУТССКЩДФИПЮРЯЛЦР', 423, 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', reverse=True))
# print(jarriquez_encryption('UUNEFWKXKVUEECMDVLPRUQQYCYTIHWUKPZ',26101986, reverse=True))

# print('0'*2)
# print('АЛМАЗ' in '123АЛМАЗЗ')