from random import randint
from .obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, images,y_pos):
        type = randint(0, 2)
        super().__init__(images, type)
        self.rect.y = y_pos

