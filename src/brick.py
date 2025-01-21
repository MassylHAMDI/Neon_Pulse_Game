import pygame
import time
import math

class Brick:
    def __init__(self, x, y, column, points):
        self.rect = pygame.Rect(x, y, 80, 20)
        self.points = points
        self.active = True
        self.column = column
        self.flash_start = 0
        self.flashing = False
        self.animation_time = 0
        
        # Définition des couleurs néon en fonction des points
        if points <= 5:
            self.base_color = (255, 51, 102)  # Rose néon
            self.glow_color = (255, 102, 153)
        elif points <= 10:
            self.base_color = (102, 204, 255)  # Bleu néon
            self.glow_color = (153, 217, 255)
        else:
            self.base_color = (57, 255, 20)    # Vert néon
            self.glow_color = (153, 255, 153)
        
        self.pulse_speed = 0.05
        self.glow_intensity = 1.0

    def start_flash(self):
        """Active le flash et désactive la brique"""
        self.flashing = True
        self.flash_start = time.time()
        self.active = False  # Désactive immédiatement la brique

    def update(self):
        """Met à jour les animations"""
        current_time = time.time()
        self.animation_time += self.pulse_speed
        
        # Animation de pulsation
        self.glow_intensity = 0.7 + math.sin(self.animation_time * 2) * 0.3
        
        # Désactive le flash après 0.2 secondes
        if self.flashing and current_time - self.flash_start > 0.2:
            self.flashing = False

    def draw_glow(self, surface, color, alpha):
        """Dessine l'effet de lueur"""
        glow_surf = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        glow_rect = pygame.Rect(5, 5, self.rect.width, self.rect.height)
        
        for i in range(3):
            expanded_rect = glow_rect.inflate(i * 2, i * 2)
            glow_alpha = int(alpha * (1 - i * 0.3))
            pygame.draw.rect(glow_surf, (*color, glow_alpha), expanded_rect, border_radius=3)
        
        surface.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5))

    def draw_neon_effect(self, surface):
        """Dessine l'effet néon principal"""
        # Valeurs d'alpha basées sur l'intensité
        base_alpha = int(255 * self.glow_intensity)
        glow_alpha = int(160 * self.glow_intensity)
        
        # Lueur externe
        self.draw_glow(surface, self.glow_color, glow_alpha)
        
        # Rectangle principal avec gradient
        gradient_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        for i in range(self.rect.height):
            progress = i / self.rect.height
            current_color = [
                int(self.base_color[0] * (0.8 + 0.2 * progress)),
                int(self.base_color[1] * (0.8 + 0.2 * progress)),
                int(self.base_color[2] * (0.8 + 0.2 * progress))
            ]
            pygame.draw.line(gradient_surf, (*current_color, base_alpha),
                           (0, i), (self.rect.width, i))
        
        surface.blit(gradient_surf, self.rect)
        
        # Bordure brillante
        pygame.draw.rect(surface, (*self.base_color, base_alpha), self.rect, 2, border_radius=2)
        
        # Reflet supérieur
        highlight_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 2)
        pygame.draw.rect(surface, (255, 255, 255, int(100 * self.glow_intensity)), 
                        highlight_rect)

    def draw_flash_effect(self, surface):
        """Dessine l'effet de flash"""
        if not self.flashing:
            return
            
        flash_progress = (time.time() - self.flash_start) / 0.2  # 0.2 secondes de flash
        if flash_progress >= 1:
            return
            
        flash_alpha = int(255 * (1 - flash_progress))
        flash_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(flash_surf, (255, 255, 255, flash_alpha), flash_surf.get_rect())
        surface.blit(flash_surf, self.rect)

    def draw(self, screen):
        """Dessine la brique si elle est active"""
        if not self.active:
            return
            
        self.draw_neon_effect(screen)
        self.draw_flash_effect(screen)