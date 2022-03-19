def simple_multiplication(x, y):
    return (100-((100-x)+(100-y)))*100 + (100-x)*(100-y)


def multiplication_check(x, y, length_check = True):
    return wisdom_multiplication(x, y, length_check) == x * y


def wisdom_multiplication(x, y, length_check = True):
    a = 100 - x
    b = 100 - y
    return int(str(100-a-b) + ('0' if len(str(a*b)) == 1 and length_check else '') + str(a*b))


def multiplication_check_list(start=10, stop=99, length_check = True):
    res_list = [multiplication_check(i,j,length_check) for i in range(start, stop+1) for j in range(start, stop+1)]
    print(f"Правильных результатов: {res_list.count(True)}")
    print(f"Неправильных результатов: {res_list.count(False)}")


# print(simple_multiplication(97, 96))
# multiplication_check_list(11, 13)
multiplication_check_list(98, 99, length_check = False)
# print(wisdom_multiplication(91, 99))