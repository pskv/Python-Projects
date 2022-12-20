import time
start_time = time.time()


def repeat_inside(line: str) -> str:
    res = ''
    for i in range(len(line)):

        if len(res) >= len(line)-i:  # to avoid unnecessary checks
            return res

        j = line.find(line[i], i+1)
        while j != -1:
            pattern = line[i:j] if line[i:j] == line[j: j+j-i] else None
            if pattern:
                k = 2
                while pattern == line[i+k*(j-i): j+k*(j-i)]:
                    k += 1
                if (j-i)*k > len(res):
                    res = pattern * k

                    if len(res)>len(line)/2:  # to avoid unnecessary checks
                        return res

                j += (j-i)*(k-2)
            j = line.find(line[i], j + 1)

    return res

for i in range(10000):
    assert repeat_inside('aaaaa') == 'aaaaa'
    assert repeat_inside('aabbff') == 'aa'
    assert repeat_inside('aababcc') == 'abab'
    assert repeat_inside('abc') == ''
    assert repeat_inside('abcabcabab') == 'abcabc'
    assert repeat_inside('ccccc') == 'ccccc'
    assert repeat_inside('rtafafafaf') == 'afafafaf'
    assert repeat_inside('rghtyjdfrtdfdf56r') == 'dfdf'
    assert repeat_inside('') == ''



print("time elapsed: {:.2f}s".format(time.time() - start_time))