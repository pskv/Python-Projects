from collections import Counter

def x_and_o(grid, your_mark):

    if grid == ('...', '...', '...'):
        return 1, 1

    other_mark = 'O' if your_mark == 'X' else 'X'

    lines = [[(i, j) for j in range(3)] for i in range(3)] + \
            [[(j, i) for j in range(3)] for i in range(3)] + \
            [[(i, i) for i in range(3)]] + [[(i, 2-i) for i in range(3)]]

    weight = {(1, 1): 4, (0, 0): 3, (0, 2): 3, (2, 0): 3, (2, 2): 3, (0, 1): 2, (1, 0): 2, (2, 1): 2, (1, 2): 2}  # to fill cell with more priority

    # can we win?
    win_lines = [sorted(''.join(map(lambda x: grid[x[0]][x[1]], i))) == sorted('.'+your_mark+your_mark) for i in lines]
    if len(set(win_lines)) > 1:
        return [i for i in lines[win_lines.index(True)] if grid[i[0]][i[1]] == '.'][0]

    # defence grid. More dangerous lines have greater rating
    defence_list = list(sorted(enumerate(map(lambda x: x.count(other_mark) if x.count(your_mark) == 0 else -1, map(lambda x: ''.join(map(lambda y: grid[y[0]][y[1]], x)), lines))), key=lambda x:-x[1]))

    if defence_list[0][1] == 2:  # need to defend anyway
        print([i for i in lines[defence_list[0][0]] if grid[i[0]][i[1]] == '.'][0])
        return [i for i in lines[defence_list[0][0]] if grid[i[0]][i[1]] == '.'][0]


    if defence_list[0][1] == 1:  # need to defend from potential forks
        cntr = Counter([i[j] for i in list(map(lambda x:lines[x], [i[0] for i in defence_list if i[1] == 1])) for j in range(3) if grid[i[j][0]][i[j][1]] == '.'])
        return sorted([i[0] for i in cntr.items() if i[1] == max(cntr.values())], key=lambda x: -weight[x])[0]


    row = [i for i in range(3) if grid[i].count('.')>0][0]  # fill last empty cell to draw
    return row, grid[row].index('.')


if __name__ == '__main__':


    #These "asserts" using only for self-checking and not necessary for auto-testing
    from random import choice

    def random_bot(grid, mark):
        empties = [(x, y) for x in range(3) for y in range(3) if grid[x][y] == "."]
        return choice(empties) if empties else (None, None)

    def referee(field):
        lines = (["".join(row) for row in field] + ["".join(row) for row in zip(*field)] +
                 [''.join(row) for row in zip(*[(r[i], r[2 - i]) for i, r in enumerate(field)])])
        if "X" * 3 in lines:
            return "X"
        elif "O" * 3 in lines:
            return "O"
        elif not "." in "".join(lines):
            return "D"
        else:
            return "."

    def check_game(user_func, user_mark, bot_mark, bot_algorithm=random_bot):
        grid = [["."] * 3 for _ in range(3)]
        if bot_mark == "X":
            x, y = bot_algorithm(grid, bot_mark)
            grid[x][y] = "X"
        while True:
            user_result = user_func(tuple("".join(row) for row in grid), user_mark)
            if (not isinstance(user_result, (tuple, list)) or len(user_result) != 2 or
                    not all(isinstance(u, int) and 0 <= u < 3 for u in user_result)):
                print("The result must be a list/tuple of two integers from 0 to 2.")
                return False

            if grid[user_result[0]][user_result[1]] != ".":
                print("You tried to mark the filled cell.")
                return False
            grid[user_result[0]][user_result[1]] = user_mark
            game_result = referee(grid)

            if game_result == "D" or game_result == user_mark:
                return True
            bot_move = bot_algorithm(grid, bot_mark)
            grid[bot_move[0]][bot_move[1]] = bot_mark
            game_result = referee(grid)
            if game_result == bot_mark:
                print("Lost :-(")
                return False
            elif game_result == "D":
                return True

    # assert check_game(x_and_o, "X", "O"), "Random X"
    # assert check_game(x_and_o, "O", "X"), "Random O"

    print(x_and_o(("O.X",".X.","..."), "O"))