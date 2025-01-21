import pygame
import random
import math
from src.constants import WIDTH, HEIGHT, SOUND_PADDLE, SOUND_BRICK, SOUND_WALL
from src.bonus_malus import BonusMalus

class Ball:
    def __init__(self, interface_height):
        self.BASE_SPEED = 5
        self.MIN_SPEED = 4
        self.MAX_SPEED = 15
        self.interface_height = interface_height
        
        self.initial_position()
        
        # Couleurs néon
        self.core_color = (255, 51, 102)  # Rose néon
        self.glow_color = (255, 182, 193)  # Rose plus clair pour la lueur
        self.trail_color = (255, 20, 147)  # Rose foncé pour la traînée
        self.radius = 8
        
        # Variables d'animation
        self.animation_time = 0
        self.pulse_speed = 0.1
        
        # Sons
        self.paddle_sound = pygame.mixer.Sound(SOUND_PADDLE)
        self.brick_sound = pygame.mixer.Sound(SOUND_BRICK)
        self.wall_sound = pygame.mixer.Sound(SOUND_WALL)
        self.paddle_sound.set_volume(0.3)
        self.brick_sound.set_volume(0.1)
        self.wall_sound.set_volume(0.09)

    def initial_position(self):
        """Positionne la balle au centre de l'écran"""
        self.rect = pygame.Rect(WIDTH // 2 - 10, self.interface_height + 100, 20, 20)
        self.speed_x = self.BASE_SPEED
        self.speed_y = -self.BASE_SPEED
        if random.random() < 0.5:
            self.speed_x *= -1

    def check_collision(self, player, bricks):
        """Vérifie les collisions"""
        points = 0
        bonus_malus = None
        
        # Collision avec la raquette
        if self.rect.colliderect(player.rect):
            # Calcul de l'angle de rebond basé sur le point d'impact
            relative_x = (self.rect.centerx - player.rect.left) / player.rect.width
            angle = relative_x * 60 - 30  # Angle entre -30 et +30 degrés
            
            # Ajustement de la vitesse
            current_speed = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
            self.speed_y = -abs(current_speed * 0.9)
            self.speed_x = current_speed * 0.7 * (relative_x - 0.5) * 2
            
            self.rect.bottom = player.rect.top
            self.paddle_sound.play()

            # Effet de particules lors de la collision
            self.create_collision_particles()

        # Collisions avec les briques
        for brick in bricks:
            if brick.active and self.rect.colliderect(brick.rect):
                # Détermine de quel côté la collision s'est produite
                overlap_left = self.rect.right - brick.rect.left
                overlap_right = brick.rect.right - self.rect.left
                overlap_top = self.rect.bottom - brick.rect.top
                overlap_bottom = brick.rect.bottom - self.rect.top

                # Trouve la plus petite superposition
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                # Applique le rebond approprié
                if min_overlap == overlap_left or min_overlap == overlap_right:
                    self.speed_x *= -1
                    # Ajuste la position pour éviter les collisions multiples
                    if min_overlap == overlap_left:
                        self.rect.right = brick.rect.left
                    else:
                        self.rect.left = brick.rect.right
                else:
                    self.speed_y *= -1
                    # Ajuste la position pour éviter les collisions multiples
                    if min_overlap == overlap_top:
                        self.rect.bottom = brick.rect.top
                    else:
                        self.rect.top = brick.rect.bottom

                brick.start_flash()
                points += brick.points
                self.brick_sound.play()
                
                if random.random() < 0.15:  # 15% de chance de bonus
                    bonus_malus = BonusMalus(brick.rect.centerx, brick.rect.bottom)
                break

        return points, bonus_malus

    def create_collision_particles(self):
        """Crée des particules lors des collisions (à implémenter si désiré)"""
        pass  # Cette méthode peut être développée pour ajouter des effets de particules

    def move(self):
        """Déplace la balle"""
        # Animation du temps
        self.animation_time += self.pulse_speed
        
        # Déplacement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collisions avec les murs
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)
            self.wall_sound.play()
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.speed_x = -abs(self.speed_x)
            self.wall_sound.play()

        if self.rect.top <= self.interface_height:
            self.rect.top = self.interface_height
            self.speed_y = abs(self.speed_y)
            self.wall_sound.play()

        # Limite de vitesse
        current_speed = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
        if current_speed > self.MAX_SPEED:
            factor = self.MAX_SPEED / current_speed
            self.speed_x *= factor
            self.speed_y *= factor
        elif current_speed < self.MIN_SPEED:
            factor = self.MIN_SPEED / current_speed
            self.speed_x *= factor
            self.speed_y *= factor

    def is_out(self):
        """Vérifie si la balle est sortie de l'écran"""
        return self.rect.top >= HEIGHT

    def draw(self, screen):
        """Dessine la balle avec effet néon"""
        # Calcul de la pulsation pour l'effet de brillance
        pulse = abs(math.sin(self.animation_time)) * 0.3 + 0.7
        
        # Effet de traînée luminescente
        for i in range(3):
            trail_pos = (
                self.rect.centerx - int(self.speed_x * i * 0.5),
                self.rect.centery - int(self.speed_y * i * 0.5)
            )
            # Lueur externe
            glow_radius = self.radius + (3 - i) * 2
            glow_alpha = int((100 - i * 30) * pulse)
            glow = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.glow_color, glow_alpha), 
                             (glow_radius, glow_radius), glow_radius)
            screen.blit(glow, (trail_pos[0] - glow_radius, trail_pos[1] - glow_radius))
            
            # Traînée principale
            trail_alpha = int((150 - i * 50) * pulse)
            trail = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail, (*self.trail_color, trail_alpha),
                             (self.radius, self.radius), self.radius - i)
            screen.blit(trail, (trail_pos[0] - self.radius, trail_pos[1] - self.radius))
        
        # Effet de lueur principal
        glow_size = int(self.radius * 3)
        glow = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        
        # Multiple cercles pour créer l'effet de lueur
        for i in range(3):
            alpha = int((60 - i * 20) * pulse)
            pygame.draw.circle(glow, (*self.core_color, alpha),
                             (glow_size, glow_size),
                             self.radius + i * 2)
        
        screen.blit(glow, (self.rect.centerx - glow_size,
                          self.rect.centery - glow_size))
        
        # Noyau brillant
        pygame.draw.circle(screen, self.core_color, self.rect.center, self.radius)
        
        # Point central plus brillant
        bright_center = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(bright_center, (255, 255, 255, int(200 * pulse)),
                          (2, 2), 2)
        screen.blit(bright_center, (self.rect.centerx - 2, self.rect.centery - 2))