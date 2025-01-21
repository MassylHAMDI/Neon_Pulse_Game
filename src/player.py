import pygame
import math
import time
import random
from src.constants import WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(350, 550, 100, 15)
        self.speed = 20
        self.original_width = self.rect.width
        
        # Couleurs néon
        self.base_color = (102, 204, 255)      # Bleu néon
        self.glow_color = (0, 255, 255)        # Cyan
        self.strong_base_color = (255, 215, 0)  # Or
        self.strong_glow_color = (255, 255, 0)  # Jaune vif
        
        # Variables d'animation
        self.animation_time = 0
        self.pulse_speed = 4.0
        self.glow_intensity = 1.0
        
        # Effets de traînée
        self.trail_positions = []
        self.max_trail_length = 5
        self.last_pos = self.rect.centerx
        
        # État du bonus
        self.is_strong = False
        self.strong_time = 0
        
        # Particules
        self.particles = []
        self.particle_spawn_timer = 0
        self.particle_spawn_delay = 0.05

    def create_particle(self):
        """Crée une particule décorative"""
        x = self.rect.centerx + random.uniform(-self.rect.width/2, self.rect.width/2)
        return {
            'pos': [x, self.rect.top],
            'vel': [random.uniform(-20, 20), random.uniform(-50, -30)],
            'size': random.uniform(1, 3),
            'lifetime': random.uniform(0.3, 0.6),
            'birth_time': time.time(),
            'color': self.strong_glow_color if self.is_strong else self.glow_color
        }

    def update_particles(self, dt):
        """Met à jour les particules décoratives"""
        current_time = time.time()
        
        # Mettre à jour les particules existantes
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0] * dt
            particle['pos'][1] += particle['vel'][1] * dt
            particle['vel'][1] += 100 * dt  # Légère gravité
            
            # Supprimer les particules expirées
            if current_time - particle['birth_time'] > particle['lifetime']:
                self.particles.remove(particle)
        
        # Créer de nouvelles particules
        self.particle_spawn_timer += dt
        if self.particle_spawn_timer >= self.particle_spawn_delay:
            self.particles.append(self.create_particle())
            self.particle_spawn_timer = 0

    def move(self):
        """Gère le mouvement du joueur"""
        old_x = self.rect.x
        
        # Mouvement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Limites de l'écran
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        
        # Mettre à jour la traînée si déplacement
        if abs(old_x - self.rect.x) > 0:
            self.trail_positions.append((self.rect.centerx, self.rect.centery))
            if len(self.trail_positions) > self.max_trail_length:
                self.trail_positions.pop(0)

    def update(self):
        """Met à jour l'état et les animations"""
        self.animation_time += 0.05
        dt = 1/60  # Delta time approximatif
        
        # Pulsation de la lueur
        self.glow_intensity = 0.8 + math.sin(self.animation_time * self.pulse_speed) * 0.2
        
        # Mise à jour des particules
        self.update_particles(dt)
        
        # Vérifier la durée du bonus strong
        if self.is_strong and time.time() - self.strong_time > 10:
            self.is_strong = False

    def draw_glow(self, surface, color, alpha):
        """Dessine l'effet de lueur"""
        for i in range(3):
            glow_rect = self.rect.inflate(i * 6, i * 4)
            glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            current_alpha = alpha // (i + 1)
            pygame.draw.rect(glow_surf, (*color, current_alpha), 
                           glow_surf.get_rect(), border_radius=5)
            surface.blit(glow_surf, glow_rect)

    def draw_trail(self, surface):
        """Dessine la traînée lors du mouvement"""
        if not self.trail_positions:
            return
            
        for i, (x, y) in enumerate(self.trail_positions):
            alpha = int(255 * (i / len(self.trail_positions)) * 0.3)
            color = self.strong_base_color if self.is_strong else self.base_color
            
            trail_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(trail_surf, (*color, alpha), 
                           (0, 0, self.rect.width, self.rect.height), 
                           border_radius=5)
            
            trail_rect = trail_surf.get_rect(center=(x, y))
            surface.blit(trail_surf, trail_rect)

    def draw_particles(self, surface):
        """Dessine les particules décoratives"""
        current_time = time.time()
        
        for particle in self.particles:
            lifetime_ratio = 1 - (current_time - particle['birth_time']) / particle['lifetime']
            if lifetime_ratio <= 0:
                continue
                
            alpha = int(255 * lifetime_ratio)
            size = particle['size'] * lifetime_ratio * 2
            
            particle_surf = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
            
            # Lueur externe
            pygame.draw.circle(particle_surf, (*particle['color'], alpha//4), 
                             (size * 2, size * 2), size * 2)
            pygame.draw.circle(particle_surf, (*particle['color'], alpha//2), 
                             (size * 2, size * 2), size * 1.5)
            
            # Cœur de la particule
            pygame.draw.circle(particle_surf, (*particle['color'], alpha), 
                             (size * 2, size * 2), size)
            
            surface.blit(particle_surf, 
                        (particle['pos'][0] - size * 2, 
                         particle['pos'][1] - size * 2))

    def draw(self, screen):
        """Dessine le joueur normal"""
        # Dessiner la traînée
        self.draw_trail(screen)
        
        # Effet de lueur
        glow_alpha = int(160 * self.glow_intensity)
        self.draw_glow(screen, self.glow_color, glow_alpha)
        
        # Rectangle principal avec gradient
        gradient_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        for i in range(self.rect.height):
            progress = i / self.rect.height
            color = [
                int(self.base_color[0] * (0.8 + 0.2 * progress)),
                int(self.base_color[1] * (0.8 + 0.2 * progress)),
                int(self.base_color[2] * (0.8 + 0.2 * progress))
            ]
            pygame.draw.line(gradient_surf, (*color, 255),
                           (0, i), (self.rect.width, i))
        
        screen.blit(gradient_surf, self.rect)
        
        # Contour lumineux
        pygame.draw.rect(screen, self.base_color, self.rect, 2, border_radius=5)
        
        # Reflet brillant
        highlight_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 2)
        pygame.draw.rect(screen, (255, 255, 255, int(100 * self.glow_intensity)), 
                        highlight_rect)
        
        # Dessiner les particules
        self.draw_particles(screen)

    def draw_strong(self, screen):
        """Dessine le joueur en mode 'strong'"""
        # Identique à draw() mais avec les couleurs strong
        old_base_color = self.base_color
        old_glow_color = self.glow_color
        
        self.base_color = self.strong_base_color
        self.glow_color = self.strong_glow_color
        
        self.draw(screen)
        
        # Restaurer les couleurs originales
        self.base_color = old_base_color
        self.glow_color = old_glow_color