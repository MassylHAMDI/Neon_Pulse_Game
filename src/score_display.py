import pygame
import math
from src.constants import WIDTH

class ScoreDisplay:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 40)
        self.value_font = pygame.font.Font(None, 48)
        self.level_font = pygame.font.Font(None, 45)
        self.highscore_font = pygame.font.Font(None, 30)
        
        # Couleurs néon
        self.neon_blue = (102, 204, 255)
        self.neon_pink = (255, 51, 102)
        self.neon_yellow = (255, 255, 102)
        self.neon_green = (57, 255, 20)
        
        # Dimensions et positions
        panel_width = WIDTH // 5
        spacing = 20
        self.interface_height = 100
        
        # Position des panneaux
        total_width = panel_width * 4 + spacing * 3
        start_x = (WIDTH - total_width) // 2
        
        self.score_pos = (start_x, 20)
        self.lives_pos = (start_x + panel_width + spacing, 20)
        self.highscore_pos = (start_x + (panel_width + spacing) * 2, 20)
        self.level_pos = (start_x + (panel_width + spacing) * 3, 20)
        
        # Animation
        self.score_animation = 0
        self.target_score = 0
        self.animation_speed = 0.1
        self.animation_time = 0
        
        # Dimensions des panneaux
        self.panel_width = panel_width
        self.panel_height = 60
        self.border_radius = 10

    def draw_neon_panel(self, screen, rect, color, glow_intensity=1.0):
        """Dessine un panneau avec effet néon"""
        # Lueur externe
        for i in range(3):
            glow_rect = rect.inflate(i * 6, i * 4)
            alpha = int(100 * glow_intensity) - (i * 30)
            if alpha <= 0:
                continue
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=self.border_radius)
            screen.blit(s, glow_rect)
        
        # Rectangle principal
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s, (*color[:3], 40), s.get_rect(), border_radius=self.border_radius)
        screen.blit(s, rect)
        
        # Bordure brillante
        pygame.draw.rect(screen, color, rect, 2, border_radius=self.border_radius)
        
        # Reflet supérieur
        highlight_rect = pygame.Rect(rect.x, rect.y, rect.width, 2)
        pygame.draw.rect(screen, (255, 255, 255, int(50 * glow_intensity)), highlight_rect)

    def animate_score(self, score):
        """Anime le score de manière fluide"""
        self.target_score = score
        diff = self.target_score - self.score_animation
        self.score_animation += diff * self.animation_speed
        if abs(diff) < 1:
            self.score_animation = self.target_score

    def draw_score(self, screen, score):
        """Dessine le score avec animation et effet néon"""
        self.animate_score(score)
        displayed_score = int(self.score_animation)
        
        panel_rect = pygame.Rect(self.score_pos[0], self.score_pos[1], 
                               self.panel_width, self.panel_height)
        self.draw_neon_panel(screen, panel_rect, self.neon_blue)
        
        # Textes avec effet de lueur
        glow = abs(math.sin(self.animation_time * 3)) * 0.3 + 0.7
        score_text = self.title_font.render("SCORE", True, self.neon_blue)
        score_value = self.value_font.render(f"{displayed_score:,}", True, 
                                          tuple(int(c * glow) for c in self.neon_blue))
        
        screen.blit(score_text, (self.score_pos[0] + 10, self.score_pos[1] + 5))
        screen.blit(score_value, (self.score_pos[0] + 10, self.score_pos[1] + 30))

    def draw_level(self, screen, level):
        """Dessine le niveau avec effet néon"""
        panel_rect = pygame.Rect(self.level_pos[0], self.level_pos[1],
                               self.panel_width, self.panel_height)
        self.draw_neon_panel(screen, panel_rect, self.neon_yellow)
        
        # Textes avec effet de lueur
        glow = abs(math.sin(self.animation_time * 3)) * 0.3 + 0.7
        level_title = self.title_font.render("LEVEL", True, self.neon_yellow)
        level_value = self.level_font.render(str(level), True, 
                                           tuple(int(c * glow) for c in self.neon_yellow))
        
        screen.blit(level_title, (self.level_pos[0] + 10, self.level_pos[1] + 5))
        screen.blit(level_value, (self.level_pos[0] + 10, self.level_pos[1] + 30))

    def draw_lives(self, screen, lives):
        """Dessine les vies avec effet néon"""
        panel_rect = pygame.Rect(self.lives_pos[0], self.lives_pos[1],
                               self.panel_width, self.panel_height)
        self.draw_neon_panel(screen, panel_rect, self.neon_pink)
        
        heart_spacing = (self.panel_width - 20) // lives if lives > 0 else 0
        for i in range(lives):
            x = self.lives_pos[0] + 10 + i * heart_spacing
            y = self.lives_pos[1] + 20
            
            glow = abs(math.sin(self.animation_time * 3 + i)) * 0.3 + 0.7
            color = tuple(int(c * glow) for c in (255, 64, 64))
            
            heart_points = [
                (x + 10, y + 5),
                (x + 5, y),
                (x, y + 5),
                (x + 10, y + 20),
                (x + 20, y + 5),
                (x + 15, y)
            ]
            pygame.draw.polygon(screen, color, heart_points)

    def draw_highscore(self, screen, highscore):
        """Dessine le high score avec effet néon"""
        panel_rect = pygame.Rect(self.highscore_pos[0], self.highscore_pos[1],
                               self.panel_width, self.panel_height)
        self.draw_neon_panel(screen, panel_rect, self.neon_green)
        
        # Textes avec effet de lueur
        glow = abs(math.sin(self.animation_time * 3)) * 0.3 + 0.7
        title = self.title_font.render("HIGH", True, self.neon_green)
        value = self.value_font.render(f"{highscore:,}", True, 
                                     tuple(int(c * glow) for c in self.neon_green))
        
        screen.blit(title, (self.highscore_pos[0] + 10, self.highscore_pos[1] + 5))
        screen.blit(value, (self.highscore_pos[0] + 10, self.highscore_pos[1] + 30))

    def draw_multiplier(self, screen, multiplier):
        """Dessine le multiplicateur avec effet néon"""
        if multiplier > 1:
            glow = abs(math.sin(self.animation_time * 5)) * 0.3 + 0.7
            color = tuple(int(c * glow) for c in self.neon_yellow)
            
            text = self.value_font.render(f"x{multiplier}", True, color)
            text_rect = text.get_rect(midtop=(WIDTH // 2, 90))
            
            scale = abs(math.sin(self.animation_time * 4)) * 0.2 + 1.0
            scaled_text = pygame.transform.rotozoom(text, 0, scale)
            scaled_rect = scaled_text.get_rect(center=text_rect.center)
            
            screen.blit(scaled_text, scaled_rect)

    def draw(self, screen, score, level, lives, highscore=0, multiplier=1):
        """Dessine l'interface complète"""
        self.animation_time += 0.05
        
        # Fond semi-transparent avec effet de gradient
        interface_surface = pygame.Surface((WIDTH, self.interface_height), pygame.SRCALPHA)
        for i in range(self.interface_height):
            alpha = 180 - int(i * 0.5)
            if alpha < 0:
                alpha = 0
            interface_surface.fill((20, 24, 32, alpha), (0, i, WIDTH, 1))
        screen.blit(interface_surface, (0, 0))
        
        # Éléments de l'interface
        self.draw_score(screen, score)
        self.draw_level(screen, level)
        self.draw_lives(screen, lives)
        self.draw_highscore(screen, highscore)
        self.draw_multiplier(screen, multiplier)
        
        # Ligne de séparation avec effet néon
        separator_y = self.interface_height - 2
        glow = abs(math.sin(self.animation_time * 2)) * 0.3 + 0.7
        color = tuple(int(c * glow) for c in self.neon_blue)
        
        for i in range(3):
            alpha = 255 - (i * 80)
            pygame.draw.line(screen, (*color[:3], alpha),
                           (0, separator_y + i), (WIDTH, separator_y + i))

    def get_interface_height(self):
        return self.interface_height