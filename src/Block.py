class Block:
    x = 0
    y = 0
    n = 0
    shapes = None
    def __init__(self, x, y,n, shapes):
        self.x = x
        self.y = y
        self.type = n
        self.color = n
        self.rotation = 0
        self.shapes = shapes
    def image(self):
        return self.shapes[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes[self.type])
