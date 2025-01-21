import pygame
import math
from src.constants import WIDTH, HEIGHT, BACKGROUND_IMAGE_GAME, MUSIC_BACKGROUND_1, MUSIC_BACKGROUND_2

class GameRenderer:
    def __init__(self, game):
        self.game = game
        
        # Interface
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        
        # Couleurs néon
        self.neon_pink = (255, 51, 102)
        self.neon_blue = (102, 204, 255)
        self.neon_green = (57, 255, 20)
        self.neon_yellow = (255, 255, 102)
        
        # Charger et redimensionner l'image de fond
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_GAME)
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
        # Dimensions des boutons
        self.button_width = 200
        self.button_height = 50
        self.level_button_size = 80
        
        # Position des boutons
        button_y = HEIGHT//2 + 50
        self.next_level_button = pygame.Rect((WIDTH - self.button_width)//2, 
                                           button_y, 
                                           self.button_width, 
                                           self.button_height)
        
        # Boutons du menu pause
        base_y = HEIGHT//2 - 20
        self.level_selector_button = pygame.Rect((WIDTH - self.button_width)//2, 
                                               base_y,
                                               self.button_width, 
                                               self.button_height)
        
        self.music_selector_button = pygame.Rect((WIDTH - self.button_width)//2, 
                                               base_y + 70,
                                               self.button_width, 
                                               self.button_height)
                                               
        self.menu_button = pygame.Rect((WIDTH - self.button_width)//2,
                                     base_y + 140,
                                     self.button_width,
                                     self.button_height)
        
        # Grille de boutons de niveau
        self.level_buttons = []
        grid_width = 3 * (self.level_button_size + 20) - 20
        start_x = (WIDTH - grid_width) // 2
        start_y = HEIGHT//2 - 30
        
        for i in range(9):
            row = i // 3
            col = i % 3
            x = start_x + col * (self.level_button_size + 20)
            y = start_y + row * (self.level_button_size + 20)
            self.level_buttons.append(pygame.Rect(x, y, self.level_button_size, self.level_button_size))
        
        # Boutons de musique
        self.music_buttons = [
            pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 30, 200, 50),  # Musique 1
            pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 40, 200, 50)   # Musique 2
        ]

    def draw_neon_text(self, text, color, pos, font, glow_radius=2):
        glow_surface = font.render(text, True, color)
        text_rect = glow_surface.get_rect(center=pos)
        alpha_surface = pygame.Surface((text_rect.width + glow_radius*2, 
                                      text_rect.height + glow_radius*2), pygame.SRCALPHA)
        
        for offset in range(glow_radius):
            alpha = 255 - (offset * 50)
            if alpha <= 0:
                continue
            for dx in [-offset, offset]:
                for dy in [-offset, offset]:
                    alpha_surface.blit(glow_surface, 
                                     (glow_radius + dx, glow_radius + dy), 
                                     special_flags=pygame.BLEND_RGBA_ADD)
        
        alpha_surface.blit(glow_surface, (glow_radius, glow_radius))
        dest_rect = alpha_surface.get_rect(center=pos)
        return alpha_surface, dest_rect.x, dest_rect.y

    def draw_neon_button(self, rect, color, hover=False, text="", font=None):
        glow = 3 if hover else 2
        for i in range(glow):
            expanded_rect = rect.inflate(i*4, i*4)
            alpha = 150 - (i * 50)
            s = pygame.Surface((expanded_rect.width, expanded_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color[:3], alpha), s.get_rect(), border_radius=5)
            self.game.screen.blit(s, expanded_rect)
        
        pygame.draw.rect(self.game.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.game.screen, (255, 255, 255), rect, 2, border_radius=5)
        
        if text and font:
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            self.game.screen.blit(text_surf, text_rect)

    def draw_pause(self):
        """Dessine l'écran de pause"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.game.screen.blit(overlay, (0, 0))
        
        if self.game.showing_music_selector:
            self.draw_music_selector()
        elif self.game.showing_level_selector:
            self.draw_level_selector()
        else:
            # Message pour quitter
            quit_text = "ESC to return to main menu"
            quit_pos = (WIDTH//2, HEIGHT//2 - 170)
            quit_surface, qx, qy = self.draw_neon_text(quit_text,
                                                      self.neon_yellow,
                                                      quit_pos,
                                                      self.small_font)
            self.game.screen.blit(quit_surface, (qx, qy))
            
            # Texte PAUSE
            pause_pos = (WIDTH//2, HEIGHT//2 - 100)
            text_surface, x, y = self.draw_neon_text('PAUSE',
                                                    self.neon_blue,
                                                    pause_pos,
                                                    self.font)
            self.game.screen.blit(text_surface, (x, y))
            
            mouse_pos = pygame.mouse.get_pos()
            # Position verticale des boutons
            button_spacing = 70
            base_y = HEIGHT//2 - 20

            # Bouton de niveau
            self.level_selector_button.y = base_y
            hover = self.level_selector_button.collidepoint(mouse_pos)
            self.draw_neon_button(self.level_selector_button,
                                self.neon_green,
                                hover,
                                'Niveau',
                                self.small_font)

            # Bouton de musique
            self.music_selector_button.y = base_y + button_spacing
            hover = self.music_selector_button.collidepoint(mouse_pos)
            self.draw_neon_button(self.music_selector_button,
                                self.neon_blue,
                                hover,
                                'Musique',
                                self.small_font)
            
            # Bouton menu principal
            self.menu_button.y = base_y + button_spacing * 2
            hover = self.menu_button.collidepoint(mouse_pos)
            self.draw_neon_button(self.menu_button,
                                self.neon_pink,
                                hover,
                                'Menu Principal',
                                self.small_font)

    def draw_level_selector(self):
        title_pos = (WIDTH//2, HEIGHT//2 - 160)
        text_surface, x, y = self.draw_neon_text('Choisir un niveau',
                                                self.neon_pink,
                                                title_pos,
                                                self.font)
        self.game.screen.blit(text_surface, (x, y))
        
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.level_buttons, 1):
            hover = button.collidepoint(mouse_pos)
            self.draw_neon_button(button,
                                self.neon_blue,
                                hover,
                                str(i),
                                self.button_font)
        
        # Bouton retour
        back_pos = (WIDTH//2, HEIGHT//2 + 160)
        back_surface, bx, by = self.draw_neon_text('Retour',
                                                  self.neon_yellow,
                                                  back_pos,
                                                  self.small_font)
        self.game.screen.blit(back_surface, (bx, by))

    def draw_music_selector(self):
        title_pos = (WIDTH//2, HEIGHT//2 - 100)
        text_surface, x, y = self.draw_neon_text('Sélection de la musique',
                                                self.neon_pink,
                                                title_pos,
                                                self.font)
        self.game.screen.blit(text_surface, (x, y))
        
        mouse_pos = pygame.mouse.get_pos()
        
        hover = self.music_buttons[0].collidepoint(mouse_pos)
        self.draw_neon_button(self.music_buttons[0],
                            self.neon_blue,
                            hover,
                            'Musique 1',
                            self.button_font)
        
        hover = self.music_buttons[1].collidepoint(mouse_pos)
        self.draw_neon_button(self.music_buttons[1],
                            self.neon_green,
                            hover,
                            'Musique 2',
                            self.button_font)
        
        back_pos = (WIDTH//2, HEIGHT//2 + 120)
        back_surface, bx, by = self.draw_neon_text('Retour',
                                                  self.neon_yellow,
                                                  back_pos,
                                                  self.small_font)
        self.game.screen.blit(back_surface, (bx, by))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.game.screen.blit(overlay, (0, 0))
        
        title_pos = (WIDTH//2, HEIGHT//2 - 100)
        text_surface, x, y = self.draw_neon_text('Game Over',
                                                self.neon_pink,
                                                title_pos,
                                                self.font)
        self.game.screen.blit(text_surface, (x, y))
        
        restart_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 10, 300, 50)
        menu_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 60, 300, 50)
        
        mouse_pos = pygame.mouse.get_pos()
        hover = restart_button.collidepoint(mouse_pos)
        self.draw_neon_button(restart_button,
                            self.neon_blue,
                            hover,
                            'Press SPACE or R to restart',
                            self.button_font)
        
        hover = menu_button.collidepoint(mouse_pos)
        self.draw_neon_button(menu_button,
                            self.neon_green,
                            hover,
                            'ESC to back to menu',
                            self.button_font)

    def draw_victory(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.game.screen.blit(overlay, (0, 0))
        
        title_pos = (WIDTH//2, HEIGHT//2 - 100)
        pulse = abs(math.sin(self.game.animation_time * 3)) * 0.3 + 0.7
        color = tuple(int(c * pulse) for c in self.neon_green)
        
        text_surface, x, y = self.draw_neon_text(
            f'Niveau {self.game.level} Terminé !',
            color,
            title_pos,
            self.font
        )
        self.game.screen.blit(text_surface, (x, y))
        
        mouse_pos = pygame.mouse.get_pos()
        hover = self.next_level_button.collidepoint(mouse_pos)
        self.draw_neon_button(self.next_level_button, self.neon_green, hover,
                            'Next Level', self.button_font)

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))
        self._draw_scanlines()
        
        for brick in self.game.bricks:
            brick.draw(self.game.screen)
        
        for ball in self.game.balls:
            ball.draw(self.game.screen)
        
        for bonus in self.game.bonus_malus_list:
            bonus.draw(self.game.screen)
        
        if self.game.player.is_strong:
            self.game.player.draw_strong(self.game.screen)
        else:
            self.game.player.draw(self.game.screen)
        
        self.game.score_display.draw(self.game.screen,
                                   self.game.score,
                                   self.game.level,
                                   self.game.lives,
                                   self.game.high_score,
                                   self.game.score_multiplier)
        
        if self.game.game_over:
            self.draw_game_over()
        elif self.game.victory:
            self.draw_victory()
        elif self.game.paused:
            self.draw_pause()
        
        pygame.display.flip()

    def _draw_scanlines(self):
        scanlines = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 2):
            pygame.draw.line(scanlines, (0, 0, 0, 30), (0, y), (WIDTH, y))
        self.game.screen.blit(scanlines, (0, 0))

    def handle_click(self, mouse_pos):
        if self.game.victory and self.next_level_button.collidepoint(mouse_pos):
            self.game.start_next_level()
        elif self.game.paused:
            if self.game.showing_music_selector:
                # Gestion des clics sur les boutons de musique
                if self.music_buttons[0].collidepoint(mouse_pos):
                    self.game.change_music(MUSIC_BACKGROUND_1)
                elif self.music_buttons[1].collidepoint(mouse_pos):
                    self.game.change_music(MUSIC_BACKGROUND_2)
                
                # Bouton retour
                back_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 100, 100, 40)
                if back_rect.collidepoint(mouse_pos):
                    self.game.showing_music_selector = False
            
            elif self.game.showing_level_selector:
                # Gestion des clics sur les boutons de niveau
                for i, button in enumerate(self.level_buttons, 1):
                    if button.collidepoint(mouse_pos):
                        self.game.jump_to_level(i)
                        self.game.showing_level_selector = False
                        self.game.paused = False
                        return
                
                # Gestion du clic sur le bouton retour
                back_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 140, 100, 40)
                if back_rect.collidepoint(mouse_pos):
                    self.game.showing_level_selector = False
            
            else:
                # Menu pause principal
                if self.level_selector_button.collidepoint(mouse_pos):
                    self.game.showing_level_selector = True
                elif self.music_selector_button.collidepoint(mouse_pos):
                    self.game.showing_music_selector = True
                elif self.menu_button.collidepoint(mouse_pos):
                    return "menu"  # Signal pour retourner au menu principal