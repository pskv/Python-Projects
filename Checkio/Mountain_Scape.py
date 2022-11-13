from typing import List, Tuple

def mountain_scape(tops: List[Tuple[int, int]]) -> int:
    # print(sorted(tops))
    total_sqr = 0
    for i in range(len(tops)):
        # print('top ', i, ':', tops[i])
        cnt_crsd = 0
        cnt = 0
        for j in range(tops[i][1]):
            for k in range((j)*2+1):
                # print('Analysed point:', (tops[i][0]-j+k, tops[i][1]-j))
                cnt += 1
                for n in range(i+1, len(tops)):
                    # print('n:', tops[n], abs(tops[n][1]-(tops[i][1]-j)), abs(tops[n][0]-(tops[i][0]-j+k)))
                    if tops[i][1]-j<=tops[n][1] \
                            and tops[n][1]-(tops[i][1]-j) >= abs(tops[n][0]-(tops[i][0]-j+k)):
                        cnt_crsd += 1
                        # print('YES')
                        break
                    # else:
                        # print('NO')
        total_sqr += tops[i][1]*tops[i][1]-cnt_crsd
        # print('GO TO Next TOP. cnt:', cnt, 'total_sqr:', total_sqr, 'cnt_crsd:', cnt_crsd)
    return total_sqr


if __name__ == '__main__':
    print("Example:")
    # print(mountain_scape([(1, 1), (4, 2), (7, 3)]))
    # print(mountain_scape([(1, 3), (5, 3), (5, 5), (8, 4)]))
    print(mountain_scape([[55,17],[68,18],[23,3],[67,17],[17,1]]))
    # print(mountain_scape([[3,3],[2,2]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    # assert mountain_scape([(1, 1), (4, 2), (7, 3)]) == 13
    # assert mountain_scape([(0, 2), (5, 3), (7, 5)]) == 29
    # assert mountain_scape([(1, 3), (5, 3), (5, 5), (8, 4)]) == 37
    print("Coding complete? Click 'Check' to earn cool rewards!")