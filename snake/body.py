class Body:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.start = 0

    def move(self, action):
        if action == "上":
            self.y -= 1
        elif action == "下":
            self.y += 1
        elif action == "左":
            self.x -= 1
        elif action == "右":
            self.x += 1

    def step(self, action):
        if self.start < self.n:
            self.start += 1
        else:
            self.move(action)