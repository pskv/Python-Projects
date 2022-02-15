def can_pass(matrix, first, second):
    processed = list()
    n_r, n_c = len(matrix), len(matrix[0])
    val = matrix[first[0]][first[1]]
    line = list()

    line.append([first, 0, 1])
    while True:
        if line[-1][2] == line[-1][1]:
            processed.append(line[-1][0])
            line.pop()
            line[-1][2] = line[-1][2] % 4 + 1
            continue

        i = line[-1][0][0]
        j = line[-1][0][1]
        if line[-1][2] == 1:
            i -= 1
        elif line[-1][2] == 2:
            j += 1
        elif line[-1][2] == 3:
            i += 1
        elif line[-1][2] == 4:
            j -= 1

        if 0 <= i < n_r and 0 <= j < n_c and matrix[i][j] == val and \
                (i, j) not in list(map(lambda x: x[0], line)) and  \
                (i, j) not in processed:
            line.append([(i, j), (line[-1][2] + 1) % 4 + 1, (line[-1][2] + 2) % 4 + 1])
            if (i, j) == second:
                return True
        else:
            line[-1][2] = line[-1][2] % 4 + 1
            if len(line) == line[0][2] == 1:
                return False


line = [[(5,2),0,1],[(3,3),2,3]]
# print(list(map(lambda x: x[0], line)))
# print((3,3) in list(map(lambda x: x[0], line)))
# print(can_pass(((3,3,2,2,2),(2,2,3,3,3),(3,3,2,2,2),(3,2,2,2,3),(2,3,2,2,2),(2,3,2,3,3)), (5,2), (0,2)))
print(can_pass(((0,0,6,0,8,6,5,6),(0,0,8,5,0,0,6,8),(5,6,5,6,0,6,6,5),(8,6,8,0,0,6,8,0),(8,6,5,6,6,8,8,0)), (1,1), (3,3)))

if __name__ == '__main__':
    print(can_pass(((0, 0, 0, 0, 0, 0),
                     (0, 2, 0, 2, 3, 2),
                     (0, 2, 0, 1, 0, 2),
                     (0, 2, 0, 2, 0, 2),
                     (0, 2, 2, 2, 0, 2),
                     (0, 0, 0, 0, 0, 2),
                     (2, 2, 2, 2, 2, 2),),
                    (3, 2), (0, 5)))
    assert can_pass(((0, 0, 0, 0, 0, 0),
                     (0, 2, 2, 2, 3, 2),
                     (0, 2, 0, 0, 0, 2),
                     (0, 2, 0, 2, 0, 2),
                     (0, 2, 2, 2, 0, 2),
                     (0, 0, 0, 0, 0, 2),
                     (2, 2, 2, 2, 2, 2),),
                    (3, 2), (0, 5)) == True, 'First example'
    assert can_pass(((0, 0, 0, 0, 0, 0),
                     (0, 2, 2, 2, 3, 2),
                     (0, 2, 0, 0, 0, 2),
                     (0, 2, 0, 2, 0, 2),
                     (0, 2, 2, 2, 0, 2),
                     (0, 0, 0, 0, 0, 2),
                     (2, 2, 2, 2, 2, 2),),
                    (3, 3), (6, 0)) == False, 'First example'
