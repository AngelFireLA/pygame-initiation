import pygame
import sys
from pygame.locals import *
from random import randint
import time

pygame.init()
fenetre = pygame.display.set_mode((640, 480))

perso = pygame.image.load("perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.center = (320, 240)

score = 0

topchrono = time.time()
delai = 2

start = True


def place_text(x, y, text):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text = font.render(text, True, (0, 0, 0))
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


def reset_position():
    position_perso.topleft = (randint(0, 540), randint(0, 380))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if position_perso.collidepoint(pygame.mouse.get_pos()) and start:
                score += 1
                reset_position()
                topchrono = time.time()
                if score % 5 == 0:
                    if delai > 1.0:
                        delai = round(delai - 0.1, 2)
                    else:
                        delai = round(delai - 0.05, 2)
            print(delai)
    fenetre.fill([10, 186, 181])
    if start:
      place_text(440, 20, "Score : " + str(score))
      fenetre.blit(perso, position_perso)

    if time.time() - topchrono > delai:
        topchrono = time.time()
        if score > 0:
            score -= 1
            if score % 5 == 0:
                delai = round(delai + 0.02, 1)
                print(delai)
        reset_position()
    pygame.draw.circle(fenetre, get_difficulty(), (20, 20), 20)
    pygame.display.flip()
