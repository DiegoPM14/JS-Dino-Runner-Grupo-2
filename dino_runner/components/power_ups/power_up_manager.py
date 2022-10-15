from random import randint, random
import pygame

from dino_runner.utils.constants import HAMMER, HAMMER_TYPE, SHIELD, SHIELD_TYPE

from .hammer import Hammer
from .shield import Shield


class PowerUpManager:
    def __init__(self) -> None:
        self.power_ups = []
        self.when_appears =0

    def generate_power_up(self, score):
        if len(self.power_ups) ==0 and self.when_appears == score:
           if randint(0,1) == 0:
              self.when_appears += randint(200, 400)
              self.power_ups.append(Shield())
           else:
                self.when_appears += randint(200, 400)
                self.power_ups.append(Hammer())

    def update(self, game, score):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed,self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                start_time = pygame.time.get_ticks()
                # game.player.has_power_up = True
                # game.player.type = power_up.type
                # if game.player.type == SHIELD_TYPE:
                #     game.player.on_pick_power_up(start_time,power_up.duration, power_up.type)
                #     self.power_ups.remove(power_up)
                # elif game.player.type == HAMMER_TYPE:
                game.player.on_pick_power_up(start_time,power_up.duration, power_up.type)
                self.power_ups.remove(power_up)

    def draw(self,screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_up(self):
        self.power_ups = []
        self.when_appears = randint(200,300)