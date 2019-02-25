from body import Body


class Snake:
    def __init__(self, init_pos, init_action):
        self.head = Body(init_pos[0], init_pos[1], 0)
        self.bodies = [self.head]
        self.action_list = [init_action]

    def length(self):
        return len(self.bodies)

    def move(self):
        for i in range(self.length()):
            body = self.bodies[i]
            body.step(self.action_list[i])

    def eat_egg(self, egg):
        new_body = Body(egg[0], egg[1], self.length())
        self.bodies.append(new_body)

    def add_action(self, new_action):
        if self.length() > 1 and ((new_action == "上" and self.action_list[0] == "下") or \
                (new_action == "下" and self.action_list[0] == "上") or \
                (new_action == "左" and self.action_list[0] == "右") or \
                (new_action == "右" and self.action_list[0] == "左")):
            new_action = self.action_list[0]
        self.action_list.insert(0, new_action)

    def pop_action(self):
        self.action_list.pop()

    def get_area(self):
        return set((body.x, body.y) for body in self.bodies)

    def is_safe(self):
        area = set((body.x, body.y) for body in self.bodies if body.start >= body.n)
        t_area = [(body.x, body.y) for body in self.bodies if body.start >= body.n]
        return len(area) == len(t_area)
