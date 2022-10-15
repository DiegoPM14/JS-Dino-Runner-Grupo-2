import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, DEFAULT_TYPE, DINO_START, HAMMER_TYPE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS, FONT_STYLE, GAME_OVER, RESET, FONT_COLOR, FONT_SIZE


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
        self.power_up_manager = PowerUpManager()
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
        self.power_up_manager.update(self, self.score.score)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_active_power_up()
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
        
        fscore= self.score.score

        if self.death_count<=0:
           self.generate_text("Press any Key to play...",self.screen)
           self.print_image(DINO_START,self.screen,pos_center_y=SCREEN_HEIGHT//2 - 80)
           
           self.handle_menu_events()
        elif self.death_count>=1 and self.death_count<=4:
            self.generate_text("You Died",self.screen)
            self.generate_text(f"Deaths: {self.death_count}",self.screen,pos_y_center=SCREEN_HEIGHT//2+50)
            self.generate_text(f"score: {fscore}",self.screen, pos_y_center=SCREEN_HEIGHT//2+100)
            self.generate_text("Press any key to Restart", self.screen, pos_y_center= SCREEN_HEIGHT//2 +170)
            self.print_image(RESET,self.screen,pos_center_y=SCREEN_HEIGHT//2 - 80)
            self.handle_menu_events()
        else:
            print("Game Over")
            self.generate_text("You Died", self.screen, pos_y_center= SCREEN_HEIGHT//2 - 170)
            self.generate_text(f"Deaths: {self.death_count}", self.screen, pos_y_center=SCREEN_HEIGHT//2+50)
            self.generate_text(f"Score: {fscore}", self.screen,pos_y_center= SCREEN_HEIGHT//2 + 100)
            self.generate_text("GAME OVER",self.screen, pos_y_center = SCREEN_HEIGHT//2 + 170)
            self.print_image(GAME_OVER,self.screen, pos_center_y= SCREEN_HEIGHT//2-100)
            pygame.display.update()
            pygame.time.delay(2000)
            self.running = False

        pygame.display.update()
        

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

   

    def on_death(self):
        has_shield= self.player.type== SHIELD_TYPE
        has_hammer= self.player.type== HAMMER_TYPE
        if not has_shield:
            pygame.time.delay(500)
            self.playing = False
            self.death_count +=1
        elif has_shield:
            return has_shield
        elif not has_hammer:
            pygame.time.delay(500)
            self.playing = False
            self.death_count +=1
        return has_hammer
        
       

    def draw_active_power_up(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up -pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
               self.generate_text(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.",
               self.screen,font_size= 18, 
               pos_y_center = 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE


    def reset_game(self):
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.score.reset_score()
        self.power_up_manager.reset_power_up()

    def print_image(self, image, screen,  pos_center_x = SCREEN_WIDTH // 2,  pos_center_y = SCREEN_HEIGHT // 2):
        img= image   
        img_rect = image.get_rect()
        img_rect.center =(pos_center_x, pos_center_y)
        screen.blit(image, img_rect)
            
    def generate_text(self, message, screen, font_color = FONT_COLOR, font_size =FONT_SIZE, pos_y_center = SCREEN_HEIGHT // 2, pos_x_center = SCREEN_WIDTH//2):
       if True:
          font = pygame.font.Font(FONT_STYLE,font_size)
          text = font.render(message, True, font_color)
          text_rect = text.get_rect()
          text_rect.center = (pos_x_center, pos_y_center)
          screen.blit(text, text_rect)

        
