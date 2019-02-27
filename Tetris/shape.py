class Shape:
    def __init__(self, x, y, color):
        self.x_center = x
        self.y_center = y
        self.color = color
        self.total_type = 4

    def move_left(self):
        self.area = [(p[0] - 1, p[1]) for p in self.area]
        self.x_center -= 1

    def move_right(self):
        self.area = [(p[0] + 1, p[1]) for p in self.area]
        self.x_center += 1

    def move_down(self):
        self.area = [(p[0], p[1]+1) for p in self.area]
        self.y_center += 1

    def rotate(self):
        self.curr_type = (self.curr_type+1) % self.total_type
        self.reset_area()

    def reset_area(self):
        self.area = [(self.x_center+s[0], self.y_center+s[1]) for s in self.directions[self.curr_type]]

    def get_right_x(self):
        return max(a[0] for a in self.area)

    def get_left_x(self):
        return min(a[0] for a in self.area)

    def get_down_y(self):
        return max(a[1] for a in self.area)


class Rect(Shape):
    """正方形
    [][]
    [][]
    """

    def __init__(self, x, y, color, type=0):
        super(Rect, self).__init__(x, y, color)
        self.area = [(x + i, y + j) for i in range(2) for j in range(2)]

    def reset_area(self):
        self.area = [(self.x_center + i, self.y_center + j) for i in range(2) for j in range(2)]

    def rotate(self):
        pass


class LZtype(Shape):
    """left Z型, 以o为中心
      [ ][]    [ ]                 []
    [][o]      [o][]      [o][]    [][o]
                  []    [][ ]        [ ]
     0         1          2          3
    """
    def __init__(self, x, y, color, type=0):
        super(LZtype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(0, 0), (0, -1), (-1, 0), (1, -1)],
                           [(0, 0), (0, -1), (1, 0), (1, 1)],
                           [(0, 0), (1, 0), (0, 1), (-1, 1)],
                           [(0, 0), (-1, 0), (-1, -1), (0, 1)]]
        self.reset_area()


class RZtype(Shape):
    """right Z型
    [][ ]         []                 [ ]
      [o][]    [o][]    [][o]      [][o]
               [ ]        [ ][]    []
     0         1          2         3
    """
    def __init__(self, x, y, color, type=0):
        super(RZtype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(0, 0), (0, -1), (-1, -1), (1, 0)],
                           [(0, 0), (1, 0), (0, 1), (1, -1)],
                           [(0, 0), (-1, 0), (0, 1), (1, 1)],
                           [(0, 0), (0, -1), (-1, 0), (-1, 1)]]
        self.reset_area()


class LLtype(Shape):
    """left L型
      [ ]      []         [ ][]
      [o]      [][o][]    [o]       [][o][]
    [][ ]                 [ ]            []
      0           1        2            3
    """
    def __init__(self, x, y, color, type=0):
        super(LLtype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(0, 0), (0, -1), (0, 1), (-1, 1)],
                           [(0, 0), (-1, 0), (-1, -1), (1, 0)],
                           [(0, 0), (0, -1), (1, -1), (0, 1)],
                           [(0, 0), (-1, 0), (1, 0), (1, 1)]]
        self.reset_area()


class RLtype(Shape):
    """right L型
      [ ]                [][ ]            []
      [o]      [][o][]     [o]       [][o][]
      [ ][]    []          [ ]
      0           1        2            3
    """
    def __init__(self, x, y, color, type=0):
        super(RLtype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(0, 0), (0, -1), (0, 1), (1, 1)],
                           [(0, 0), (-1, 0), (-1, 1), (1, 0)],
                           [(0, 0), (0, -1), (-1, -1), (0, 1)],
                           [(0, 0), (-1, 0), (1, 0), (1, -1)]]
        self.reset_area()


class Ttype(Shape):
    """T 型
                  [ ]       [ ]        [ ]
    [][o][]     [][o]     [][o][]      [o][]
      [ ]         [ ]                  [ ]
      0           1          2          3
    """
    def __init__(self, x, y, color, type=0):
        super(Ttype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(0, 0), (0, 1), (-1, 0), (1, 0)],
                           [(0, 0), (-1, 0), (0, 1), (0, -1)],
                           [(0, 0), (0, -1), (-1, 0), (1, 0)],
                           [(0, 0), (1, 0), (0, 1), (0, -1)]]
        self.reset_area()


class Itype(Shape):
    """I 型
    []                   [ ]
    []o    [][][o][]     [o]          o
    []                   [ ]     [][][][]
    []                   [ ]
    0         1         2        3
    """
    def __init__(self, x, y, color, type=0):
        super(Itype, self).__init__(x, y, color)
        self.curr_type = type
        self.directions = [[(-1, 0), (-1, -1), (-1, 1), (-1, 2)],
                           [(0, 0), (-2, 0), (-1, 0), (1, 0)],
                           [(0, 0), (0, -1), (0, 1), (0, 2)],
                           [(0, 1), (-1, 1), (-2, 1), (1, 1)]]
        self.reset_area()
