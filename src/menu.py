import pygame
import math
from src.constants import WIDTH, HEIGHT, BACKGROUND_IMAGE

class MainMenu:
    def __init__(self):
        # Polices réduites
        self.title_font = pygame.font.Font(None, 80)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Couleurs synthwave
        self.title_color = (255, 51, 102)  # Rose néon
        self.text_color = (102, 204, 255)  # Bleu clair néon
        self.highlight_color = (255, 51, 153)  # Rose vif
        
        # Options du menu
        self.menu_options = ['JOUER', 'PB (TODO)', 'QUITTER']
        self.selected_option = 0
        
        # Animation
        self.animation_time = 0
        self.title_offset = 0
        
        # Boutons
        self.buttons = []
        self.create_buttons()

        # Charger l'image de fond
        self.background_image = pygame.image.load(BACKGROUND_IMAGE)
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

    def create_buttons(self):
        button_width = 160
        button_height = 40
        spacing = 20
        
        # Position le menu plus haut dans l'écran
        start_y = HEIGHT // 2 - 30
        
        for i, option in enumerate(self.menu_options):
            button_rect = pygame.Rect(
                WIDTH // 2 - button_width // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.buttons.append((button_rect, option))

    def draw_title(self, screen):
        """Dessine le titre avec effet synthwave"""
        # Effet de dédoublement (glitch)
        offset = math.sin(self.animation_time * 5) * 2
        title = "NEON PULSE"
        
        # Ombre cyan
        cyan_shadow = self.title_font.render(title, True, (0, 255, 255))
        shadow_rect = cyan_shadow.get_rect(center=(WIDTH // 2 + offset, HEIGHT // 3 + 2))
        
        # Ombre magenta
        magenta_shadow = self.title_font.render(title, True, (255, 0, 255))
        magenta_rect = magenta_shadow.get_rect(center=(WIDTH // 2 - offset, HEIGHT // 3 - 2))
        
        # Texte principal
        title_text = self.title_font.render(title, True, self.title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Dessiner les effets
        screen.blit(cyan_shadow, shadow_rect)
        screen.blit(magenta_shadow, magenta_rect)
        screen.blit(title_text, title_rect)
        
        # Ligne décorative sous le titre
        line_y = title_rect.bottom + 10
        pygame.draw.line(screen, self.title_color, 
                        (WIDTH//4, line_y), (WIDTH*3//4, line_y), 2)

    def draw_button(self, screen, button_rect, text, is_selected):
        color = self.highlight_color if is_selected else self.text_color
        alpha = 160 if is_selected else 100
        
        # Fond du bouton avec effet de grille
        button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*color[:3], alpha), 
                        button_surface.get_rect(), border_radius=2)
        screen.blit(button_surface, button_rect)
        
        # Effet de ligne horizontale si sélectionné
        if is_selected:
            line_pos = button_rect.centery
            pygame.draw.line(screen, color, 
                           (button_rect.left - 20, line_pos),
                           (button_rect.right + 20, line_pos), 1)
        
        # Texte avec effet de glitch si sélectionné
        text_surface = self.menu_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        if is_selected:
            offset = math.sin(self.animation_time * 5) * 2
            screen.blit(text_surface, text_rect.move(offset, 0))
            screen.blit(text_surface, text_rect.move(-offset, 0))
        else:
            screen.blit(text_surface, text_rect)

    def update(self):
        self.animation_time += 0.02
        self.title_offset = math.sin(self.animation_time) * 5

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, (rect, _) in enumerate(self.buttons):
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for rect, option in self.buttons:
                if rect.collidepoint(mouse_pos):
                    return option
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                return self.menu_options[self.selected_option]
        
        return None

    def draw(self, screen):
        # Fond
        screen.blit(self.background_image, (0, 0))
        
        # Overlay dégradé subtil
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)
        screen.blit(overlay, (0, 0))
        
        # Éléments du menu
        self.draw_title(screen)
        
        for i, (button_rect, option) in enumerate(self.buttons):
            self.draw_button(screen, button_rect, option, i == self.selected_option)
        
        # Version avec effet néon
        version_text = self.menu_font.render("v1.0", True, (255, 51, 102))
        version_rect = version_text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
        screen.blit(version_text, version_rect)