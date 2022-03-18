# https://stepik.org/lesson/65382/step/1?unit=154908


def numerics(n):
    return list(map(int, str(n)))

def kaprekar_step(L):
    val = ''.join(map(str, sorted(L)))
    return int(val[::-1]) - int(val)

def kaprekar_loop(n, prev_numbers = set()):
    if kaprekar_check(n):
        if n in prev_numbers:
            print(f"Следующее число - {n}, кажется процесс зациклился...")
            return
        print(n)
        if n in {495, 6174, 549945, 631764}:
            return
        kaprekar_loop(kaprekar_step(numerics(n)), prev_numbers.union({n}))
    else:
        print(f"Ошибка! На вход подано число {n}, не удовлетворяющее условиям процесса Капрекара")

def kaprekar_check(n):
    return len(numerics(n)) in [3,4,6] and len(set(numerics(n))) != 1 and n not in (100,1000,100000)



kaprekar_loop(103303)
