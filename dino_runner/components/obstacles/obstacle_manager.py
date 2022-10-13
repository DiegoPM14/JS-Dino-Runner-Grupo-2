import random

from dino_runner.components import obstacles
from .cactus import Cactus
from .bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game_speed , player, on_death):
        if len(self.obstacles)== 0:
            rndm_obstacle = random.randint(0,2)
            if rndm_obstacle ==0:
               s_cactus = Cactus(SMALL_CACTUS,325)
               self.obstacles.append(s_cactus)
            elif rndm_obstacle ==1:
               l_cactus = Cactus(LARGE_CACTUS,300)
               self.obstacles.append(l_cactus)
            elif rndm_obstacle == 2:
                bird = Bird(BIRD)
                self.obstacles.append(bird)

        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
               on_death()
               break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles= []