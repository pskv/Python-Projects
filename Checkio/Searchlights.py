from collections import namedtuple
from math import sin, pi, sqrt, acos


def searchlights(polygons, lights):
    Shape = namedtuple('Shape', ['x', 'y', 'r', 'p_cnt'], defaults=[-1])

    res = 0
    for polygon in polygons:

        r = round(polygon[2]/2/sin(pi/polygon[3]), 4)  # radius
        p = Shape(x=polygon[0], y=polygon[1]-r, r=r, p_cnt=polygon[3])
        print(p)

        point_angles = set([i * (360 / p.p_cnt) for i in range(p.p_cnt)])

        if p.x - p.r < 0:  # check points with negative X coordinates
            angle = acos(p.x / p.r) * 180 / pi
            point_angles = set(
                filter(lambda x: angle - 90 <= x <= 360 - angle - 90 or angle - 90 <= x - 360 <= 360 - angle - 90,
                       point_angles))

        if p.y - p.r < 0:  # check points with negative Y coordinates
            angle = acos(p.y / p.r) * 180 / pi
            point_angles = set(
                filter(lambda x: angle - 180 <= x <= 180 - angle or angle - 180 <= x - 360 <= 180 - angle,
                       point_angles))

        visible_points = set()

        for light in lights:
            l = Shape(x=light[0], y=light[1], r=light[2])
            d = sqrt((p.x-l.x)**2 + (p.y-l.y)**2)  # distance between centers

            if d == 0:  # Centers are equal
                if p.r <= l.r:
                    # res += len(point_angles)
                    visible_points |= point_angles
                continue
            if d == p.r+l.r:  # One point intersection
                # res += 1
                if l.x>p.x:
                    visible_points |= acos((l.y - p.y) / d) * 180 / pi
                    continue
                visible_points |= 360 - acos((l.y - p.y) / d) * 180 / pi
                continue
            if d > p.r+l.r:  # No intersection
                continue
            if p.r > d+l.r:  # Circle is in the polygon
                continue
            if l.r >= d + p.r:  # Polygon is in the circle
                # res += len(point_angles)
                visible_points |= point_angles
                continue

            #  Two point intersection
            angle = (acos((d**2+p.r**2-l.r**2)/(2*d*p.r)) * 180 / pi)  # angle
            if l.x >= p.x:
                angle2 = acos((l.y-p.y)/d) * 180 / pi
            else:
                angle2 = 360-acos((l.y-p.y)/d) * 180 / pi


            visible_points |= set(
                filter(
                    lambda x: angle2-angle <= x <= angle2+angle or
                              angle2-angle <= x - 360 <= angle2+angle or
                              angle2-angle <= x + 360 <= angle2+angle
                    ,point_angles))
            continue
        res += len(visible_points)

    return res


if __name__ == "__main__":
    # print("Example:")

    # print(searchlights([(4, 2, 2, 6)], [(4, 2, 3)]))
    # print(searchlights([(4, 3, 2, 8)], [(4, 2, 2)]))
    # print(searchlights([[1,5,2,4],[7,5,2,4],[4,6,2,4]],[[2,4,1],[3,4,1],[4,4,1],[5,4,1],[6,4,1]]))
    # print(searchlights([[2,5,3,3],[6,5,3,3]],[[3,4,2],[4,2,2]]))
    print(searchlights([[2,2,2,7],[1,5,2,8]],[[1,2,2],[3,5,1],[2,3,2],[8,1,1],[4,3,2],[4,4,1]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    # assert (searchlights([(2, 3, 2, 3)], [(1, 2, 1)])) == 1, "regular triangle"
    # assert (searchlights([(4, 5, 2, 4)], [(4, 4, 3)])) == 4, "square"
    # assert (searchlights([(6, 7, 2, 5)], [(2, 3, 2)])) == 0, "regular pentagon"
    # assert (searchlights([(4, 2, 2, 6)], [(4, 2, 3)])) == 3, "regular hexagon"
    # assert (searchlights([(1, 7, 2, 8)], [(0, 5, 4)])) == 5, "regular octagon"
    print("Coding complete? Click 'Check' to earn cool rewards!")
