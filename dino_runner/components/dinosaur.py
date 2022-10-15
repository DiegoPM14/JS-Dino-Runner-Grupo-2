import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_HAMMER, DUCKING_SHIELD, JUMPING, JUMPING_HAMMER, JUMPING_SHIELD, RUNNING, RUNNING_HAMMER, RUNNING_SHIELD, SHIELD_TYPE, HAMMER_TYPE

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.jump_velocity = self.JUMP_VEL
        self.dino_running= True
        self.dino_jumping= False
        self.dino_ducking= False
        self.has_power_up= False
        self.power_up_time_up= 0
        
    def update(self,user_input):
        if self.dino_running:
            self.run()
        elif self.dino_jumping:
            self.jump()
        elif self.dino_ducking:
            self.duck()

        if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.dino_jumping:
            self.dino_jumping = True
            self.dino_running = False
            self.dino_ducking = False
        elif user_input[pygame.K_DOWN] and not self.dino_jumping:
            self.dino_jumping = False
            self.dino_running = False
            self.dino_ducking = True
        elif not self.dino_jumping:
            self.dino_jumping = False
            self.dino_running = True
            self.dino_ducking = False
        
        if self.step_index >= 9:
            self.step_index=0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5 ]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index+=1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        self.dino_rect.y -= self.jump_velocity *4
        self.jump_velocity -=0.8

        if self.jump_velocity < -8.5:
            self.dino_rect.y = self.Y_POS
            self.dino_jumping = False
            self.jump_velocity = self.JUMP_VEL

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5 ]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y= self.Y_POS_DUCK

    def draw(self, screen):
        screen.blit(self.image,(self.dino_rect.x, self.dino_rect.y))
    
    def on_pick_power_up(self, start_time, duration, type):
        self.has_power_up = True
        self.power_up_time_up = start_time + (duration *1000)
        self.type = type