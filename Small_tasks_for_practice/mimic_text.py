# https://stepik.org/lesson/54762/step/10?unit=37456

import random


def mimic_dict(string):
    res = dict()
    for pair in sorted(list(zip([""] + string.upper().split(), string.upper().split()))):
        res[pair[0]] = res.get(pair[0], []) + [pair[1]]
    return res


def print_mimic(mimic_dict, word):
    text = word
    text_len = 1
    while text_len < 200:
        word = random.choice(mimic_dict.get(word, mimic_dict['']))
        text += ' '+word
        text_len += 1
    return text


text = 'We are not what we should be '
text += 'We are not what we need to be '
text += 'But at least we are not what we used to be '
text += '-- Football Coach '


# print(mimic_dict('Uno dos tres cuatro cinco'))
# print(mimic_dict('a cat and a dog\na fly'))
print(print_mimic(mimic_dict(text), '').lower())