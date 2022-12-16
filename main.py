import pygame
from pygame import mixer
import sys
from pygame.locals import *
from random import randint
import time

pygame.init()
HEIGHT = 480
WIDTH = 640
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

mixer.init()


background = pygame.image.load("Capture.PNG").convert_alpha()

perso = pygame.image.load("perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.center = (320, 240)

easy = pygame.image.load("easy.png").convert_alpha()
position_easy = easy.get_rect()
normal = pygame.image.load("normal.png").convert_alpha()
position_normal = normal.get_rect()
hard = pygame.image.load("hard.png").convert_alpha()
position_hard = hard.get_rect()
impossible = pygame.image.load("impossible.png").convert_alpha()
position_impossible = impossible.get_rect()

score = 0
streak = 0

topchrono = time.time()
delai = 2

chronometre = 0
secondes = 0

start = False

def play_sound(name, volume):
    mixer.music.load(name)
    mixer.music.set_volume(volume)
    mixer.music.play()
def place_text(x, y, text):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text = font.render(text, True, (150, 150, 150))
    fenetre.blit(text, dest=(x, y))

def get_difficulty() -> tuple:
    if score < 25:
        return 0, 255, 0
    elif score < 50:
        return 255, 155, 55
    elif score < 100:
      return 255, 0, 0
    else:
        return 0, 0, 0


def show_difficulty():
    if score < 25:
        fenetre.blit(easy, (20, 20))
    elif score < 50:
        fenetre.blit(normal, (20, 20))
    elif score < 100:
        fenetre.blit(hard, (20, 20))
    else:
        fenetre.blit(impossible, (20, 20))


def reset_position():
    position_perso.topleft = (randint(0, WIDTH - 100), randint(0, HEIGHT - 100))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if position_perso.collidepoint(pygame.mouse.get_pos()) and start:
                score += 1
                play_sound("shot.mp3", 0.3)
                reset_position()
                topchrono = time.time()
                if score % 5 == 0:
                    if delai > 1.0:
                        delai = round(delai - 0.1, 3)
                    elif delai > 0.5:
                        delai = round(delai - 0.05, 3)
                    else:
                        delai = round(delai - 0.025, 3)
            if not start:
                pygame.time.wait(500)
                play_sound("game-start.mp3", 0.7)
                start = True
    fenetre.blit(background, (0, 0))
    if start:
        place_text(440, 20, "Score : " + str(score))
        place_text(10, 440, "Délai : " + str(delai) + "s")
        show_difficulty()
        pygame.draw.circle(fenetre, get_difficulty(), (150, 60), 25)
        fenetre.blit(perso, position_perso)
        if time.time() - topchrono > delai:
            topchrono = time.time()
            if score > 0:
                score -= 1
                streak += 1
                if streak == 5:
                    streak = 0
                    if delai > 1.0:
                        delai = round(delai + 0.1, 3)
                    elif delai > 0.5:
                        delai = round(delai + 0.05, 3)
                    else:
                        delai = round(delai + 0.025, 3)
            reset_position()
        if time.time() - chronometre > 1:
            secondes+=1
            chronometre = time.time()
        place_text(WIDTH - 180, HEIGHT - 40, "Temps : " + str(secondes))
    else:
        place_text(10, HEIGHT / 2 - 40, "Cliquez ici pour commencer le test.")
    pygame.display.flip()
