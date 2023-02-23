def rotate_cube(cube, direction):
    if direction == 1:
        return [cube[4], cube[5], cube[2], cube[3], cube[1], cube[0]]
    elif direction == 2:
        return [cube[2], cube[3], cube[1], cube[0], cube[4], cube[5]]
    elif direction == -1:
        return [cube[5], cube[4], cube[2], cube[3], cube[0], cube[1]]
    elif direction == -2:
        return [cube[3], cube[2], cube[0], cube[1], cube[4], cube[5]]


def paper_dice(paper):
    ln_len = len(paper[0])
    for rn,cn in [(i,j) for i in range(len(paper)) for j in range(len(paper[0]))]:
        if paper[rn][cn] != ' ':
            break
    points = []
    points.append((rn, cn))
    paths = [[]]
    pointer = 0

    cube = [int(paper[rn][cn]), 7-int(paper[rn][cn]), 0, 0, 0, 0]

    while pointer<5:

        for i in paths[pointer]:
            cube = rotate_cube(cube, i)
        rn, cn = points[pointer][0], points[pointer][1]

        for i,j,m,n,k in ((0,1,4,5,1), (1,0,2,3,2), (0,-1,5,4,-1), (-1,0,3,2,-2)):
            if cn+j<ln_len and rn+i<len(paper) and paper[rn+i][cn+j] != ' ' and (rn+i, cn+j) not in points:
                points.append((rn+i, cn+j))
                paths.append(paths[pointer]+[k])
                if cube[m] == 0:
                    cube[m] = int(paper[rn+i][cn+j])
                    cube[n] = 7 - int(paper[rn+i][cn+j])
                elif cube[m] != int(paper[rn+i][cn+j]):
                    return False

        for i in paths[pointer][::-1]:
            cube = rotate_cube(cube, i*-1)
        pointer += 1

    return True


if __name__ == '__main__':
    print(paper_dice(["      ", " 1  6 ", " 2354 ", "      "]))

    # assert paper_dice([
    #             '  1  ',
    #             ' 235 ',
    #             '  6  ',
    #             '  4  ']) is True, 'cross'
    # assert paper_dice([
    #             '    ',
    #             '12  ',
    #             ' 36 ',
    #             '  54',
    #             '    ']) is True, 'zigzag'
    # assert paper_dice(['123456']) is False, '1 line'
    # assert paper_dice([
    #             '123  ',
    #             '  456']) is False, '2 lines_wrong'
    # assert paper_dice([
    #             '126  ',
    #             '  354']) is True, '2 lines_right'
    # print("Check done.")

