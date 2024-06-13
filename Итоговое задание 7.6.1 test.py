game_map = [["-"] * 3 for i in range(3)]


def print_map():
    print()
    print("    | 0 | 1 | 2 | ")
    print("  ----------------")
    for i, row in enumerate(game_map):
        row_str = f"  {i} | {' | '.join(row)} | "
        print(row_str)
        print("  ---------------")
    print()


def player_input():
    while True:
        x = input("Выберите строку: ")
        y = input("Выберите столбец: ")

        if not (x.isdigit()) or not (y.isdigit()):
            print("Введите число!")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print("Координаты вне диапазона")
            continue

        if game_map[x][y] != "-":
            print(" Клетка занята! ")
            continue

        return x, y


def win_check():
    win_cord = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2))]
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(game_map[c[0]][c[1]])
            if symbols == ["X", "X", "X"]:
                print("Выиграл игрок №1 'X'")
                return True
            if symbols == ["0", "0", "0"]:
                print("Выиграл игрок №2 '0'")
                return True
    return False


step_num = 0

while True:
    step_num += 1
    print_map()

    if step_num % 2 == 1:
        print(" Ходит игрок №1 ("'X'") ")
    else:
        print(" Ходит игрок №2 ("'0'") ")

    x, y = player_input()

    if step_num % 2 == 1:
        game_map[x][y] = "X"
    else:
        game_map[x][y] = "0"

    if win_check():
        print_map()
        break

    if step_num == 9:
        print("Ничья!")
        print_map()
        break

