import pygame
import sys
from src.game import Game
from src.menu import MainMenu
from src.constants import WIDTH, HEIGHT

class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        
        self.game = None
        self.menu = MainMenu()
        self.current_state = "menu"  # "menu" ou "game"
        self.running = True
        self.frame_rate = 60

    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            if self.current_state == "menu":
                self.run_menu()
            elif self.current_state == "game":
                result = self.run_game()
                if result == "menu":
                    self.transition_to_menu()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

        self.cleanup()

    def run_menu(self):
        """Gestion du menu principal"""
        self.menu.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
            
            action = self.menu.handle_event(event)
            if action == "JOUER":
                self.transition_to_game()
            elif action == "QUITTER":
                self.running = False
                return
            elif action == "PB":
                # TODO: Implémenter l'écran des meilleurs scores
                pass

        self.menu.draw(self.screen)

    def run_game(self):
        """Gestion du jeu"""
        if not self.game:
            self.game = Game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game.game_over:
                        return "menu"
                    else:
                        self.game.paused = not self.game.paused
                elif event.key == pygame.K_SPACE:
                    if self.game.game_over:
                        self.game.reset_game()
                elif event.key == pygame.K_r and self.game.game_over:
                    self.game.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game.game_over:
                    # Gestion des clics pendant le game over
                    pass
                elif self.game.paused:
                    self.game.renderer.handle_click(mouse_pos)
                elif self.game.victory:
                    if self.game.renderer.next_level_button.collidepoint(mouse_pos):
                        self.game.start_next_level()

        if not self.game.paused and not self.game.game_over:
            self.game.update()
        
        self.game.renderer.draw()
        return None

    def transition_to_game(self):
        """Transition vers le jeu"""
        self.current_state = "game"
        self.game = Game()
        pygame.mixer.music.stop()  # Arrête la musique du menu

    def transition_to_menu(self):
        """Transition vers le menu"""
        self.current_state = "menu"
        if self.game:
            pygame.mixer.music.stop()  # Arrête la musique du jeu
            self.game = None
        self.menu = MainMenu()

    def cleanup(self):
        """Nettoyage avant de quitter"""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


# Point d'entrée principal
if __name__ == "__main__":
    try:
        game_controller = GameController()
        game_controller.run()
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")
        pygame.quit()
        sys.exit(1)


        