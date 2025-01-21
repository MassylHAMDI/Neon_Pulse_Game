import pygame
import random
from src.constants import WIDTH, HEIGHT

class BonusMalus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed_y = 3
        self.active_time = 10000
        self.start_time = None
        
        # Types de bonus/malus avec leurs probabilités
        self.bonus_types = {
            "extra_life": 15,        # Vie supplémentaire (15%)
            "increase_paddle": 20,    # Agrandir la raquette (20%)
            "decrease_paddle": 15,    # Rétrécir la raquette (15%)
            "speed_up_ball": 0,     # Accélérer la balle (15%)
            "slow_ball": 0,         # Ralentir la balle (20%)
            "points_multiplier": 0   # Multiplicateur de points x2 (15%)
        }
        
        # Sélection du type basée sur les probabilités
        total = sum(self.bonus_types.values())
        rand = random.randint(1, total)
        current = 0
        
        for bonus_type, prob in self.bonus_types.items():
            current += prob
            if rand <= current:
                self.type = bonus_type
                break
                
        self.color = self.get_color()

    def get_color(self):
        colors = {
            "extra_life": (0, 255, 0),        # Vert
            "increase_paddle": (0, 0, 255),    # Bleu
            "decrease_paddle": (255, 165, 0),  # Orange
            "speed_up_ball": (255, 0, 0),      # Rouge
            "slow_ball": (0, 255, 255),        # Cyan
            "points_multiplier": (148, 0, 211)  # Violet
        }
        return colors.get(self.type, (255, 255, 255))

    def get_symbol(self):
        symbols = {
            "extra_life": "♥",
            "increase_paddle": "↔",
            "decrease_paddle": "↕",
            "speed_up_ball": "⚡",
            "slow_ball": "⊙",
            "points_multiplier": "×2"
        }
        return symbols.get(self.type, "?")

    def move(self):
        self.rect.y += self.speed_y

    def is_out(self):
        return self.rect.top >= HEIGHT

    def apply_effect(self, game):
        """Applique l'effet du bonus/malus au jeu"""
        if self.type == "extra_life":
            game.lives += 1
        elif self.type == "increase_paddle":
            game.player.rect.width = min(200, game.player.rect.width + 40)
        elif self.type == "decrease_paddle":
            game.player.rect.width = max(40, game.player.rect.width - 20)
        elif self.type == "speed_up_ball":
            for ball in game.balls:
                ball.speed_x *= 1.5
                ball.speed_y *= 1.5
        elif self.type == "slow_ball":
            for ball in game.balls:
                ball.speed_x *= 0.7
                ball.speed_y *= 0.7
        elif self.type == "points_multiplier":
            game.score_multiplier = 2
            game.multiplier_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Dessiner le fond du bonus
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Contour
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Symbole
        font = pygame.font.Font(None, 30)
        symbol = font.render(self.get_symbol(), True, (0, 0, 0))
        symbol_rect = symbol.get_rect(center=self.rect.center)
        screen.blit(symbol, symbol_rect)