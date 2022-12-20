import pyxel

class Tegel():
    def __init__(self, x, y, c):
        self.x = x * 8
        self.y = y * 8
        self.c = c

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, self.c, 8, 8, pyxel.COLOR_BLACK)