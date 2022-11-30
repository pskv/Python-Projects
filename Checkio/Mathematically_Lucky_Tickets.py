import itertools

def conv(nb):
    base = 5
    a = nb // base
    if a < base:
        return str(a) + str(nb % base)
    return str(conv(a)) + str(nb % base)

def checkio(value: str) -> bool:
    opers = ['','+','-','*','/']
    for i in range(5**5):
        nums = [value[0]]
        ops = []
        ops_codes = f'{conv(i):0>5}'

        for j in range(5):
            if ops_codes[j] == '0':
                nums[-1] = nums[-1]+value[j+1]
                continue
            ops.append(opers[int(ops_codes[j])])
            nums.append(value[j+1])

        for k in map(list, itertools.permutations(range(len(ops)))):
            task_ops = ops.copy()
            task = nums.copy()
            while True:
                if len(k) == 0:
                    break
                m = k.pop(0)
                res = '('+task[m]+task_ops[m]+task[m+1]+')'
                task[m] = res

                task.pop(m+1)
                task_ops.pop(m)
                for n in range(len(k)):
                    if k[n] > m:
                        k[n] -= 1

            try:
                n1 = eval(task[0])
            except:
                continue

            if n1 == 100:
                return False


    return True



print("Example:")
# print(checkio("100478"))  # True

# These "asserts" are used for self-checking
# assert checkio("000000") == True
# assert checkio("707409") == True
# assert checkio("595347") == False
# assert checkio("271353") == False
# assert checkio("000955") == False
# assert checkio("100478") == True
# assert checkio("100479") == False
# assert checkio("725126") == True
# assert checkio("836403") == False
# assert checkio("240668") == False
# assert checkio("082140") == True
# assert checkio("574699") == False
# assert checkio("324347") == False
# assert checkio("064377") == True
# assert checkio("111111") == False
assert checkio("555555") == False
assert checkio("777777") == False
assert checkio("392039") == False

print("The mission is done! Click 'Check Solution' to earn rewards!")