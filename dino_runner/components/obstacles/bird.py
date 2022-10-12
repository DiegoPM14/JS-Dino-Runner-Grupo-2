import random

from .obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type =0
        self.step_index =0
        super().__init__(image,self.type)
        self.rect.y = random.randint(260,310)

    def draw(self, screen):
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(self.images[self.step_index<5],self.rect)
        self.step_index += 1