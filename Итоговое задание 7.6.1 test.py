game_map = [" ", "0", "1", "2",
            "0", "-", "-", "-",
            "1", "-", "-", "-",
            "2", "-", "-", "-"]

victories = [[5, 6, 7],
             [9, 10, 11],
             [13, 14, 15],
             [5, 9, 13],
             [6, 10, 14],
             [7, 11, 15],
             [5, 10, 15],
             [7, 10, 13]]


def print_map():
    print(game_map[0], end=" ")
    print(game_map[1], end=" ")
    print(game_map[2], end=" ")
    print(game_map[3])

    print(game_map[4], end=" ")
    print(game_map[5], end=" ")
    print(game_map[6], end=" ")
    print(game_map[7])

    print(game_map[8], end=" ")
    print(game_map[9], end=" ")
    print(game_map[10], end=" ")
    print(game_map[11])

    print(game_map[12], end=" ")
    print(game_map[13], end=" ")
    print(game_map[14], end=" ")
    print(game_map[15])


def step_game_map(step, symbol):
    index = step
    game_map[index] = symbol


def step_index(x, y):   ## Тестовая версия проверки на занятость клетки(ошибочная), не могу понять,как ее реализовать.
    while True:
        try:
            if x == 0 and y == 0:
                step = game_map.index("-", 5, 6)
            if x == 0 and y == 1:
                step = game_map.index("-", 9, 10)
            if x == 0 and y == 2:
                step = game_map.index("-", 13, 14)
            if x == 1 and y == 0:
                step = game_map.index("-", 6, 7)
            if x == 1 and y == 1:
                step = game_map.index("-", 10, 11)
            if x == 1 and y == 2:
                step = game_map.index("-", 14, 15)
            if x == 2 and y == 0:
                step = game_map.index("-", 7, 8)
            if x == 2 and y == 1:
                step = game_map.index("-", 11, 12)
            if x == 2 and y == 2:
                step = game_map.index("-", 15, 16)

        except:
            print("Клетка занята,попробуйте снова")
            break

        else:
            return step




def get_result():
    win = ""

    for i in victories:
        if game_map[i[0]] == "X" and game_map[i[1]] == "X" and game_map[i[2]] == "X":
            win = "Игрок №1"
        if game_map[i[0]] == "0" and game_map[i[1]] == "0" and game_map[i[2]] == "0":
            win = "Игрок №2"
    return win


def player_check_x(start, end):
    while True:
        if player1 == True:
            try:
                x = int(input("Игрок №1, ваш ход, выберите столбец: "))

            except ValueError:
                print("Вы ввели не число. Попробуйте снова.")
            else:
                if start <= x <= end:
                    return x
                print("Введённое число вне диапазона: (%d, %d)" % (start, end))
        else:
            try:
                x = int(input("Игрок №2, ваш ход, выберите столбец: "))

            except ValueError:
                print("Вы ввели не число. Попробуйте снова.")
            else:
                if start <= x <= end:
                    return x
                print("Введённое число вне диапазона: (%d, %d)" % (start, end))


def player_check_y(start, end):
    while True:
        if player1 == True:
            try:
                y = int(input("Игрок №1, ваш ход, выберите cтроку: "))

            except ValueError:
                print("Вы ввели не число. Попробуйте снова.")
            else:
                if start <= y <= end:
                    return y
                print("Введённое число вне диапазона: [%d, %d)" % (start, end))
        else:
            try:
                y = int(input("Игрок №2, ваш ход, выберите строку: "))

            except ValueError:
                print("Вы ввели не число. Попробуйте снова.")
            else:
                if start <= y <= end:
                    return y
                print("Введённое число вне диапазона: [%d, %d)" % (start, end))


game_over = False
player1 = True


while game_over == False:
    print_map()
    if player1 == True:
        symbol = "X"
        x = player_check_x(0, 2)
        y = player_check_y(0, 2)
    else:
        symbol = "0"
        x = player_check_x(0, 2)
        y = player_check_y(0, 2)

    step_game_map(step_index(x, y), symbol)
    win = get_result()
    if win != "":
        game_over = True
    else:
        game_over = False
    player1 = not (player1)

print_map()
print("Победил", win)
