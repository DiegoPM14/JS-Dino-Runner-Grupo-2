from turtle import pos
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score

from dino_runner.utils.constants import BG, DINO_START, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAME_OVER


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.score = Score()
        self.death_count = 0
        self.running = False 


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
               self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
       

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed,self.player, self.on_death)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255,255,255))

        pos_center_x = SCREEN_WIDTH // 2
        pos_center_y = SCREEN_HEIGHT // 2
        
        dino_rect = DINO_START.get_rect()
        dino_rect.center =(pos_center_x, pos_center_y - 80)

       # fscore= self.score

        if self.death_count<=0:
           self.generate_text("Press any Key to play...",pos_center_x,pos_center_y, 45, (0,0,0))
           self.screen.blit(DINO_START, dino_rect)
           self.handle_menu_events()
        elif self.death_count>=1 and self.death_count<=4:
            self.generate_text("You Died", pos_center_x, pos_center_y-170,70,(0,0,0))
            self.generate_text(f"Deaths: {self.death_count}", pos_center_x, pos_center_y,40,(0,0,0))
            #self.generate_text(f"score: {fscore}", pos_center_x, pos_center_y+50,40,(0,0,0))
            self.generate_text("Press any key to Restart", pos_center_x, pos_center_y+170,50,(0,0,0))
            fscore=0
            self.handle_menu_events()
        else:
            self.generate_text("You Died", pos_center_x, pos_center_y-170,70,(0,0,0))
            self.generate_text(f"Deaths: {self.death_count}", pos_center_x, pos_center_y,40,(0,0,0))
           # self.generate_text(f"Score: {fscore}", pos_center_x, pos_center_y+50,40,(0,0,0))
            self.generate_text("Press any key to Restart", pos_center_x, pos_center_y+170,50,(0,0,0))
            self.screen.blit(GAME_OVER,dino_rect)
            fscore=0
            pygame.time.delay(5000)
            self.running= False
        
        pygame.display.update()
        

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def generate_text(self, text, h_screen_width, h_screen_heigh, size, color):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = (h_screen_width, h_screen_heigh)
        self.screen.blit(text,text_rect)

    def on_death(self):
        self.playing = False
        self.death_count +=1

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.score.reset_score()
        

        
