import pygame
import time
from src.constants import WIDTH, HEIGHT, screen, MUSIC_BACKGROUND_1
from src.player import Player
from src.ball import Ball
from src.score_display import ScoreDisplay
from src.bonus_malus import BonusMalus
from src.brick import Brick
from src.game_render import GameRenderer
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Configuration de l'écran et du jeu
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Créer d'abord le score display
        self.score_display = ScoreDisplay()
        interface_height = self.score_display.get_interface_height()
        
        # Initialiser les objets du jeu
        self.player = Player()
        self.ball = Ball(interface_height)
        self.balls = [self.ball]
        
        # Score et progression
        self.score = 0
        self.high_score = self.load_high_score()
        self.score_multiplier = 1
        self.level = 1
        self.lives = 3
        
        # État du jeu
        self.running = True
        self.game_over = False
        self.victory = False
        self.paused = False
        self.showing_level_selector = False
        
        # Éléments du jeu
        self.create_bricks()
        self.bonus_malus_list = []
        self.active_effects = []
        
        # Temps et animations
        self.victory_time = None
        self.multiplier_time = 0
        self.animation_time = 0
        
        # Initialiser le renderer
        self.renderer = GameRenderer(self)
        
        # Musique
        self.current_music = MUSIC_BACKGROUND_1
        self.showing_music_selector = False
        self.load_and_play_music()

        # Score display et autres initialisations...
        self.score_display = ScoreDisplay()
        interface_height = self.score_display.get_interface_height()

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass

    def create_bricks(self):
        self.bricks = []
        brick_width = 80
        brick_height = 20
        rows = self.level + 2
        spacing_x = (WIDTH - (6 * brick_width)) / 7
        
        start_y = self.score_display.get_interface_height() + 20
        
        for row in range(rows):
            y = start_y + (row * (brick_height + 5))
            for col in range(6):
                x = spacing_x + col * (brick_width + spacing_x)
                points = (rows - row) * 5
                self.bricks.append(Brick(x, y, col, points))

    def jump_to_level(self, level):
        interface_height = self.score_display.get_interface_height()
        self.level = level
        self.ball = Ball(interface_height)
        self.balls = [self.ball]
        self.player = Player()
        self.victory = False
        self.paused = False
        self.game_over = False
        self.create_bricks()
        self.bonus_malus_list.clear()
        self.victory_time = None
        self.active_effects.clear()

    def reset_game(self):
        interface_height = self.score_display.get_interface_height()
        self.ball = Ball(interface_height)
        self.balls = [self.ball]
        self.player = Player()
        self.game_over = False
        self.victory = False
        self.score = 0
        self.level = 1
        self.lives = 3
        self.create_bricks()
        self.bonus_malus_list.clear()
        self.active_effects.clear()
        self.score_multiplier = 1

    def start_next_level(self):
        interface_height = self.score_display.get_interface_height()
        self.level += 1
        self.ball = Ball(interface_height)
        self.balls = [self.ball]
        self.player = Player()
        self.victory = False
        self.paused = False
        self.create_bricks()
        self.bonus_malus_list.clear()
        self.victory_time = None
        self.active_effects.clear()

    def update_effects(self):
        current_time = pygame.time.get_ticks()
        
        if self.score_multiplier > 1 and current_time - self.multiplier_time > 10000:
            self.score_multiplier = 1
        
        if self.player.is_strong and current_time - self.player.strong_time > 10000:
            self.player.is_strong = False

    def update(self):
        if not self.game_over and not self.victory and not self.paused:
            self.animation_time += 0.05
            self.player.update()
            self.player.move()
            self.update_effects()
            
            # Mise à jour des balles
            for ball in self.balls[:]:
                ball.move()
                points, new_bonus = ball.check_collision(self.player, self.bricks)
                
                if points > 0:
                    self.score += points * self.score_multiplier
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                
                if new_bonus and len(self.bonus_malus_list) == 0:
                    self.bonus_malus_list.append(new_bonus)
                
                if ball.is_out():
                    self.balls.remove(ball)
                    if len(self.balls) == 0:
                        self.lives -= 1
                        if self.lives > 0:
                            self.ball = Ball(self.score_display.get_interface_height())
                            self.balls = [self.ball]
                        else:
                            self.game_over = True
            
            # Mise à jour des bonus/malus
            for bonus in self.bonus_malus_list[:]:
                bonus.move()
                if bonus.rect.colliderect(self.player.rect):
                    bonus.apply_effect(self)
                    self.bonus_malus_list.remove(bonus)
                elif bonus.is_out():
                    self.bonus_malus_list.remove(bonus)
            
            # Mise à jour des briques et vérification de la victoire
            active_bricks = 0
            for brick in self.bricks:
                brick.update()
                if brick.active:
                    active_bricks += 1
            
            if active_bricks == 0:
                self.victory = True
                self.victory_time = time.time()

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.showing_level_selector:
                        self.showing_level_selector = False
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_SPACE and self.victory:
                    self.start_next_level()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.renderer.handle_click(event.pos)
    def load_and_play_music(self):
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def change_music(self, music_path):
        pygame.mixer.music.stop()
        self.current_music = music_path
        self.load_and_play_music()
        self.showing_music_selector = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        return "menu"  # Retourne au menu principal
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.victory:
                mouse_pos = pygame.mouse.get_pos()
                if self.next_level_button.collidepoint(mouse_pos):
                    self.start_next_level()
        
        return None
    def run(self):
        while self.running:
            result = self.handle_events()
            if result == "menu":
                return result

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()