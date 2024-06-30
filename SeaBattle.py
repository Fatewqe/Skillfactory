from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Земля плоская! Вы вышли за пределы, попробуйте снова!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Что-то с памятью моей стало... вы уже стреляли в эту клетку,попробуйте снова!"


class BoardWrongShipException(BoardException):
    pass


class Cells:
    empty_cell = ' '
    ship_cell = '■'
    damaged_ship = '□'
    miss_cell = '•'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, start, length, direction):
        self.start = start
        self.length = length
        self.direction = direction
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.start.x
            cur_y = self.start.y

            if self.direction == 0:
                cur_x += i

            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide

        self.count = 0

        self.field = [[Cells.empty_cell] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        map = ""
        map += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            map += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.hide:
            map = map.replace(Cells.ship_cell, Cells.empty_cell)
        return map

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        around = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in around:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = Cells.miss_cell
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = Cells.ship_cell
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shoten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = Cells.damaged_ship
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль повреждён!")
                    return True

        self.field[d.x][d.y] = Cells.miss_cell
        print("Мазила!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("------------------------")
        print("    Приветствуем вас    ")
        print("         в игре         ")
        print("      морской бой!      ")
        print("------------------------")
        print("    формат ввода: x y   ")
        print("    x - номер строки    ")
        print("    y - номер столбца   ")

    def print_boards(self):
        print("-" * 28)
        print("Доска игрока:")
        print(self.us.board)
        print("-" * 28)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-" * 28)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            print("-" * 28)
            print("Карта игрока:")
            print(self.us.board)
            print("-" * 28)
            print("Карта компьютера:")
            print(self.ai.board)
            print("-" * 28)
            if num % 2 == 0:
                print("Ходит игрок!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 28)
                print("Игрок победил!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 28)
                print("Компьютер победил!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

