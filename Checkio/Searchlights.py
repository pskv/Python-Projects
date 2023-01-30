from collections import namedtuple
from math import sin, pi, sqrt, acos, cos
import time

# The idea is to work with angles instead of coordinates of each point.
# First check if polygon intersects with X axis.
#       If intersects then find a width of this intersection determined by angle and remove particular points from analysis.
# Repeat previos step with Y axis
# Find width of intersection of polygon and circle.
#      If intersects then count points with particular angles.
#
# P.S. All angles are in radians.


Shape = namedtuple('Shape', ['x', 'y', 'r', 'p_cnt'], defaults=[-1])

def searchlights(polygons, lights):

    res = 0
    for polygon in polygons:

        r = round(polygon[2]/2/sin(pi/polygon[3]), 1)  # radius
        p = Shape(x=polygon[0], y=polygon[1]-r, r=r, p_cnt=polygon[3])

        point_angles = [i * (2 * pi / p.p_cnt) for i in range(p.p_cnt)]

        if p.x - p.r < 0:  # check points with negative X coordinates
            # remove them from analysis
            point_angles = filter(lambda x: sin(x)*p.r+p.x >= 0, point_angles)

        if p.y - p.r < 0:  # check points with negative Y coordinates
            # remove them from analysis
            point_angles = filter(lambda x: cos(x)*p.r+p.y >= 0, point_angles)

        visible_points = set()  # result set of points

        for light in lights:
            l = Shape(x=light[0], y=light[1], r=light[2])
            d = sqrt((p.x-l.x)**2 + (p.y-l.y)**2)  # distance between centers

            if d == 0:  # Centers are equal
                if p.r <= l.r:
                    visible_points |= set(point_angles)
                continue
            if d > p.r+l.r:  # No intersection
                continue
            if p.r > d+l.r:  # Circle is in the polygon. No intersection
                continue
            if l.r >= d + p.r:  # Polygon is in the circle
                visible_points |= set(point_angles)
                continue
            if d == p.r+l.r:  # One point intersection
                if l.x > p.x:
                    visible_points |= acos((l.y - p.y) / d)
                    continue
                visible_points |= 2*pi - acos((l.y - p.y) / d)
                continue

            #  Two points intersection
            angle = acos((d**2+p.r**2-l.r**2)/(2*d*p.r))
            if l.x >= p.x:
                angle2 = acos((l.y-p.y)/d)
            else:
                angle2 = 2*pi - acos((l.y-p.y)/d)


            visible_points |= set(
                filter(
                    lambda x: angle2-angle <= x <= angle2+angle or
                              angle2-angle <= x - 2*pi <= angle2+angle or
                              angle2-angle <= x + 2*pi <= angle2+angle
                    ,point_angles))
            continue
        res += len(visible_points)

    return res


if __name__ == "__main__":

    start = time.time()

    # print("Example:")

    # print(searchlights([(4, 2, 2, 6)], [(4, 2, 3)]))
    # print(searchlights([(4, 3, 2, 8)], [(4, 2, 2)]))
    # print(searchlights([[1,5,2,4],[7,5,2,4],[4,6,2,4]],[[2,4,1],[3,4,1],[4,4,1],[5,4,1],[6,4,1]]))
    # print(searchlights([[2,5,3,3],[6,5,3,3]],[[3,4,2],[4,2,2]]))
    # print(searchlights([[2,2,2,7],[1,5,2,8]],[[1,2,2],[3,5,1],[2,3,2],[8,1,1],[4,3,2],[4,4,1]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    for _ in range(10000):
        assert (searchlights([(2, 3, 2, 3)], [(1, 2, 1)])) == 1, "regular triangle"
        assert (searchlights([(4, 5, 2, 4)], [(4, 4, 3)])) == 4, "square"
        assert (searchlights([(6, 7, 2, 5)], [(2, 3, 2)])) == 0, "regular pentagon"
        assert (searchlights([(4, 2, 2, 6)], [(4, 2, 3)])) == 3, "regular hexagon"
        assert (searchlights([(1, 7, 2, 8)], [(0, 5, 4)])) == 5, "regular octagon"
        # print("Coding complete? Click 'Check' to earn cool rewards!")



    end = time.time()
    print(end - start)