import numpy

def calc_coefs(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return(dy, -dx, dy*point1[0]-dx*point1[1])


def shot(wall1, wall2, shot_point, later_point):
    koefs1 = calc_coefs(wall1, wall2)
    koefs2 = calc_coefs(shot_point, later_point)

    M1 = numpy.array([koefs1[:2], koefs2[:2]])
    v1 = numpy.array([koefs1[2], koefs2[2]])

    try:
        x,y = numpy.linalg.solve(M1, v1)
    except:
        return -1

    if min(wall1[0], wall2[0]) <= x <= max(wall1[0], wall2[0])\
    and min(wall1[1], wall2[1]) <= y <= max(wall1[1], wall2[1])\
    and min(shot_point[0], x) <= later_point[0] <= max(shot_point[0], x)\
    and min(shot_point[1], y) <= later_point[1] <= max(shot_point[1], y):
        if wall1[0] == wall2[0]:
            return round(100-abs((((wall1[1]+wall2[1])/2)-y)*200/(wall1[1]-wall2[1])))
        return round(100-abs((((wall1[0]+wall2[0])/2)-x)*200/(wall1[0]-wall2[0])))
    return -1

if __name__ == '__main__':
    print(shot((10,10),(10,90),(50,90),(50,50)))
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert shot((2, 2), (5, 7), (11, 2), (8, 3)) == 100, "1st case"
    assert shot((2, 2), (5, 7), (11, 2), (7, 2)) == 0, "2nd case"
    assert shot((2, 2), (5, 7), (11, 2), (8, 4)) == 29, "3th case"
    assert shot((2, 2), (5, 7), (11, 2), (9, 5)) == -1, "4th case"
    assert shot((2, 2), (5, 7), (11, 2), (10.5, 3)) == -1, "4th case again"
