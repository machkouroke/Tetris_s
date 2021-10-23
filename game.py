import numpy as np
import copy as cp


def hyphen(w, h):
    return '\n'.join(' '.join('-' for _ in range(w)) for _ in range(h))


def coordinate(array, number):
    """
    Returns the coordinates of a point according to its number
    :param array:Coordinate number table
    :param number:An array with the number of point
    :return: An array with the coordinate of point
    """
    return [
        [[np.argwhere(number == j)[0][k] for k in (0, 1)] for j in i]
        for i in array
    ]


class Grid:
    ch = {
        'T': np.array([[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]),
        'O': np.array([[4, 14, 15, 5]]),
        'L': np.array([[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
        'J': np.array([[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
        'I': np.array([[4, 14, 24, 34], [3, 4, 5, 6]]),
        'S': np.array([[5, 4, 14, 13], [4, 14, 15, 25]]),
        'Z': np.array([[4, 5, 15, 16], [5, 15, 14, 24]])
    }

    def __init__(self, w: 'width', h: 'height', c: 'Tetris Character'):
        self.w = w
        self.h = h
        # An array with number of each point in grid
        self.form = np.array([[y for y in range(x, x + w)] for x in range(0, w * h, w)])
        self.plan = [['-' for _ in range(w)] for _ in range(h)]
        # Table that keeps the state of the grid when adding a new point
        self.actual = [['-' for _ in range(w)] for _ in range(h)]
        self.piece = [Piece(c, {x: coordinate(y, self.form) for x, y in Grid.ch.items()}[c][0], w, h)]
        self.plan_actualise()

    def add_piece(self, n: 'Name of piece'):
        self.actual = self.plan
        self.piece.append(Piece(n, {x: coordinate(y, self.form) for x, y in Grid.ch.items()}[n][0], self.w, self.h))
        self.plan_actualise()

    def plan_actualise(self):
        temp_plan = cp.deepcopy(self.actual)
        for x in self.piece[-1].coord:
            if temp_plan[x[0]][x[1]] == '-':
                temp_plan[x[0]][x[1]] = '0'
            else:
                self.piece[-1].collision = True
                self.actual = self.plan
                return
        self.plan = temp_plan

    @property
    def maps(self):
        return '\n'.join(' '.join(x) for x in self.plan)

    def break_line(self):
        for k in range(self.h):
            if all(x == '0' for x in self.plan[k]):
                self.plan.pop(k)
                self.plan.insert(0, ['-' for _ in range(self.w)])

    def move(self, type_):
        if type_ == 'down':
            self.piece[-1].down()
            self.plan_actualise()
        elif type_ == 'right':
            self.piece[-1].right()
            self.plan_actualise()
        elif type_ == 'left':
            self.piece[-1].left()
            self.plan_actualise()
        elif type_ == 'rotate':
            if self.piece[-1].reach:
                n, i, t = self.piece[-1].name, self.piece[-1].count['rotate'], len(Grid.ch[self.piece[-1].name])
                self.piece[-1].coord = {x: coordinate(y, self.form) for x, y in Grid.ch.items()}[n][i % t]
                self.piece[-1].rotate()
                self.plan_actualise()


class Piece:

    def __init__(self, name, coord, w_grid, h_grid):
        self.name = name
        self.coord = coord
        self.grid = [w_grid, h_grid]
        # Contains a counter for each movement
        self.count = {'down': 0, 'right': 0, 'left': 0, 'rotate': 1}
        self.collision = False

    @property
    def reach(self):
        return all(x[0] + 1 < self.grid[1] for x in self.coord)

    def down(self, inside=True):
        if self.reach:
            for x in range(len(self.coord)):
                self.coord[x][0] = (self.coord[x][0] + 1) % self.grid[1]
            if inside:
                self.count['down'] += 1

    def right(self, inside=True):
        border = all(x[1] + 1 < self.grid[0] for x in self.coord)
        if border and self.reach:
            for x in range(len(self.coord)):
                self.coord[x][1] = (self.coord[x][1] + 1) % self.grid[0]
            if inside:
                self.count['right'] += 1
        self.down(inside=False)

    def left(self, inside=True):
        border = all(x[1] >= 1 for x in self.coord)
        if border and self.reach:
            for x in range(len(self.coord)):
                self.coord[x][1] = (self.coord[x][1] - 1) % self.grid[0]
            if inside:
                self.count['left'] += 1
        self.down(inside=False)

    def rotate(self):
        if self.reach:
            for i in {'left', 'right', 'down'}:
                for _ in range(self.count[i]):
                    eval('self.' + i + '(inside=False)')
            self.down()
            self.count['rotate'] += 1


def main():
    # Dimension
    w, h = [int(x) for x in input().split()]
    print(hyphen(w, h) + '\n')
    # first command and piece
    input()
    piece = input()
    game = Grid(w, h, piece)
    print(game.maps + '\n')
    # input command
    choice = input()
    while choice != 'exit':
        if choice == 'piece':
            game.add_piece(input())
            print(game.maps + '\n')
        elif choice == 'break':
            game.break_line()
            print(game.maps + '\n')
        else:
            game.move(choice)
            print(game.maps + '\n')
            m = np.array(game.plan).transpose()
            if any(all(y == '0' for y in x) for x in m) and len(game.plan) > 0:
                # Game over
                break

        choice = input()


if __name__ == '__main__':
    main()
