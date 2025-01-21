import pygame

# Configuration de la fenêtre
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid - Niveaux")

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)
VIOLET = (255, 0, 255)

# Chemins des fichiers audio
SOUND_PADDLE = "assets/sounds/paddle.wav"
SOUND_BRICK = "assets/sounds/brick.wav"
SOUND_WALL = "assets/sounds/wall.wav"
MUSIC_BACKGROUND_1 = "assets/sounds/bg_music_1.wav"
MUSIC_BACKGROUND_2 = "assets/sounds/bg_music_1.wav"

# Chemin de l'image de fond
BACKGROUND_IMAGE = "assets/images/bg_menu.jpg"
BACKGROUND_IMAGE_GAME = "assets/images/bg_game.jpg"

