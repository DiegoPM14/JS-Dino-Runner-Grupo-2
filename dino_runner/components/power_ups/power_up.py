from random import randint
from dino_runner.utils.constants import SCREEN_WIDTH
from pygame.sprite import Sprite


class PowerUp(Sprite):
    def __init__(self, image, type):
       self.type = type
       self.image = image
       self.rect = self.image.get_rect()
       self.rect.x = SCREEN_WIDTH 
       self.rect.y = randint(150, 250)

       self.duration = randint(3, 5)

    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            power_ups.pop()

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))
        