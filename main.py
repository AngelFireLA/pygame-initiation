import sys
import time
from random import randint

import pygame
from pygame import mixer
from pygame.locals import *
import json


# Setup la fenêtre Pygame
pygame.init()
WIDTH = 640
HEIGHT = 480
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Démarre le système audio de pygame
mixer.init()

# Charge différentes images et leur rectangle si besoin
background = pygame.image.load("Capture.PNG").convert_alpha()

perso = pygame.image.load("perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.center = (320, 240)

perso_rouge = pygame.image.load("perso_rouge.png")
position_perso_rouge = perso_rouge.get_rect()

easy = pygame.image.load("easy.png").convert_alpha()
position_easy = easy.get_rect()
normal = pygame.image.load("normal.png").convert_alpha()
position_normal = normal.get_rect()
hard = pygame.image.load("hard.png").convert_alpha()
position_hard = hard.get_rect()
impossible = pygame.image.load("impossible.png").convert_alpha()
position_impossible = impossible.get_rect()

souris = pygame.image.load("cursor.png").convert_alpha()
souris_rect = souris.get_rect()

button = pygame.image.load("button.png").convert_alpha()
pressed_button = pygame.image.load("button_pressed.png").convert_alpha()
cross_button = pygame.image.load("button_croix.svg").convert_alpha()

heart = pygame.image.load("heart.png").convert_alpha()
heart = pygame.transform.scale(heart, (heart.get_width()/10, heart.get_height()/10))
heart_pos = heart.get_rect()
heart_pos.midright = (WIDTH - 40, HEIGHT - 40)


class Button:
    def __init__(self, x, y, taille, texte, couleur_texte=None, taille_texte=36, btype=button):
        self.largeur = btype.get_width()
        self.hauteur = btype.get_height()
        self.image = pygame.transform.scale(btype, (int(self.largeur * taille), int(self.hauteur * taille)))
        self.pressed_image = pygame.transform.scale(pressed_button, (int(self.largeur * taille), int(self.hauteur * taille)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.texte = texte
        self.couleur_texte = couleur_texte
        self.taille_texte = taille_texte
        self.btype = btype

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                if self.btype == button:
                    fenetre.blit(self.pressed_image, (self.rect.x, self.rect.y + 5))
                    place_text(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte, (0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(100)
                    fenetre.blit(self.image, (self.rect.x, self.rect.y))
                    place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, (0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(100)
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        fenetre.blit(self.image, (self.rect.x, self.rect.y))
        if self.btype == button:
            place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, (0, 0, 0))

        return action

    def initier_click(self):
        fenetre.blit(self.pressed_image, (self.rect.x, self.rect.y + 5))
        place_text(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte, (0, 0, 0))
        pygame.display.update()
        pygame.time.delay(1000)
        fenetre.blit(self.image, (self.rect.x, self.rect.y))
        place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, (0, 0, 0))
        pygame.display.update()
        return True


score = 0
high_score = 0
clicks = 0
cible_touchee = 0
fail_streak = 0

# Variables pour le temps
topchrono = time.time()
delai = 2
chronometre = 0
secondes = 0

# Variable pour l'état du jeux
game_state = {"main_menu": True, "playing": False, "pause": False, "perdu": False, "instructions": False}
gamemode = {"normal": True, "invisible": False, "chrono": False, "survie": False}
vies = 3
chrono = 5
# La valeur de chrono c'est le temps en seconde et la valeur de survivre c'est le nom de vies

restart_button = Button(WIDTH / 2, HEIGHT - 80, 2, "Recommencer", taille_texte=40)
normal_button = Button(WIDTH / 2, 120, 1.8, "Normal", taille_texte=40)
invisible_button = Button(WIDTH / 2, 220, 1.8, "Souris Invisible", taille_texte=40)
survie_button = Button(WIDTH / 2, 320, 1.8, "Survivre", taille_texte=40)
chrono_button = Button(WIDTH / 2, 420, 1.8, "Temps Limité", taille_texte=40)
menu_button = Button(50, 50, 0.25, "", btype=cross_button)
instructions_button = Button(565, 445, 0.7, "Instructions", taille_texte=15)


def play_sound(name, volume):
    mixer.music.load(name)
    mixer.music.set_volume(volume)
    mixer.music.play()


def place_text(x, y, text, size, color=None):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    if color:
        text = font.render(text, True, color)
    else:
        text = font.render(text, True, (150, 150, 150))
    fenetre.blit(text, text.get_rect(center=(x, y)))


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


def restart():
    global score, fail_streak, delai, secondes, game_state, high_score, clicks, cible_touchee
    score = 0
    high_score = 0
    clicks = 0
    cible_touchee = 0
    fail_streak = 0
    delai = 2
    secondes = 0
    reset_lives()
    reset_chrono()
    reset_position()


def player_attacked(temps):
    global perso
    fenetre.blit(perso_rouge, (position_perso.x, position_perso.y))
    show_mouse()
    pygame.display.flip()
    while not time.time() - temps > 0.08 :
        pass
    fenetre.blit(perso, (position_perso.x, position_perso.y))
    show_mouse()
    pygame.display.flip()


def event_manager():
    global score, delai, topchrono, game_state, high_score, perso, cible_touchee, clicks, vies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if game_state["playing"]:
                clicks += 1
                if position_perso.collidepoint(pygame.mouse.get_pos()):
                    score += 1
                    cible_touchee += 1
                    if score > high_score:
                        high_score = score
                    play_sound("slash.wav", 0.2)
                    player_attacked(time.time())
                    reset_position()
                    topchrono = time.time()
                    if score % 5 == 0:
                        if delai > 1.0:
                            delai = round(delai - 0.1, 3)
                        elif delai >= 0.5:
                            delai = round(delai - 0.05, 3)
                        else:
                            delai = round(delai - 0.025, 3)
                else:
                    if gamemode["survie"]:
                        vies -= 1
                        if vies == 0:
                            game_state = {key: False if key != "perdu" else True for key in game_state}

        if event.type == pygame.KEYDOWN:
            if game_state["playing"]:
                if event.key == pygame.K_ESCAPE:
                    game_state = {key: False if key != 'pause' else True for key in game_state}
                if event.key == pygame.K_q:
                    game_state = {key: False if key != 'perdu' else True for key in game_state}


def reset_chrono():
    global chrono
    with open('config.json') as f:
        data = json.load(f)
        chrono = data["chrono"] + 1


def reset_lives():
    global vies
    with open('config.json') as f:
        data = json.load(f)
        vies = data["vies"]


def show_mouse():
    if not gamemode["invisible"]:
        souris_rect.center = pygame.mouse.get_pos()
        fenetre.blit(souris, souris_rect)


while True:
    event_manager()
    fenetre.blit(background, (0, 0))
    if game_state["playing"]:
        pygame.mouse.set_visible(False)
        place_text(530, 40, "Score : " + str(score), 36)

        show_difficulty()
        pygame.draw.circle(fenetre, get_difficulty(), (150, 60), 25)
        if not gamemode["chrono"]:
            place_text(100, 440, "Délai : " + str(delai) + "s", 36)
            if time.time() - topchrono > delai:
                topchrono = time.time()
                if score > 0:
                    score -= 1
                    fail_streak += 1
                    if fail_streak == 5:
                        fail_streak = 0
                        if delai > 1.0:
                            delai = round(delai + 0.1, 3)
                        elif delai >= 0.5:
                            delai = round(delai + 0.05, 3)
                        elif delai < 0.5:
                            delai = round(delai + 0.025, 3)
                reset_position()
            # Chronomètre
            if time.time() - chronometre > 1:
                secondes += 1
                chronometre = time.time()
        else:
            place_text(WIDTH - 110, HEIGHT - 40, "Temps : " + str(chrono), 36)
            if time.time() - chronometre > 1:
                chrono -= 1
                if chrono == 0:
                    game_state = {key: False if key != 'perdu' else True for key in game_state}
                chronometre = time.time()
        if gamemode["survie"]:
            fenetre.blit(heart, heart_pos)
            place_text(WIDTH - 30, HEIGHT - 40, str(vies), 60)
        fenetre.blit(perso, position_perso)
        show_mouse()
    elif game_state["pause"]:
        pygame.mouse.set_visible(True)
        place_text(WIDTH / 2, HEIGHT / 2.2, "Pause", 50)
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = {key: False if key != 'playing' else True for key in game_state}
                        pygame.mouse.set_visible(False)
                        loop = False
                        reset_position()
                        topchrono = time.time()
            if menu_button.draw():
                restart()
                game_state = {key: False if key != 'main_menu' else True for key in game_state}
                loop = False
            if restart_button.draw():
                restart()
                game_state = {key: False if key != 'playing' else True for key in game_state}
                loop = False
            pygame.display.flip()
    elif game_state["perdu"]:
        if clicks == 0:
            clicks = 1
        place_text(WIDTH / 2, 50, "Terminer !", 50)
        place_text(WIDTH / 2, 50+87.5, f"Score Final : {score} cibles", 36)
        place_text(WIDTH / 2, 50+87.5+60, f"Précision : {int(cible_touchee/clicks*100)}%", 36)
        if gamemode["chrono"]:
            reset_chrono()
            place_text(WIDTH / 2, 400-87.5-60, f"Temps Initial : {chrono-1} secondes", 36)
        else:
            place_text(WIDTH / 2, 400 - 87.5 - 60, f"Temps : {secondes} secondes", 36)
            place_text(WIDTH / 2, 400 - 87.5, f"Highscore : {cible_touchee} cibles", 36)
        if menu_button.draw():
            restart()
            game_state = {key: False if key != 'main_menu' else True for key in game_state}
        if restart_button.draw():
            restart()
            game_state = {key: False if key != 'playing' else True for key in game_state}
    elif game_state["main_menu"]:
        place_text(WIDTH / 2, 30, "Choisir le mode de jeux :", 36)
        if normal_button.draw():
            restart()
            game_state = {key: False if key != 'playing' else True for key in game_state}
            gamemode = {key: False if key != 'normal' else True for key in gamemode}
            play_sound("game-start.mp3", 0.7)
        if invisible_button.draw():
            restart()
            game_state = {key: False if key != 'playing' else True for key in game_state}
            gamemode = {key: False if key != 'invisible' else True for key in gamemode}
            play_sound("game-start.mp3", 0.7)
        if chrono_button.draw():
            restart()
            game_state = {key: False if key != 'playing' else True for key in game_state}
            gamemode = {key: False if key != 'chrono' else True for key in gamemode}
            play_sound("game-start.mp3", 0.7)
            reset_chrono()
        if survie_button.draw():
            restart()
            game_state = {key: False if key != 'playing' else True for key in game_state}
            gamemode = {key: False if key != 'survie' else True for key in gamemode}
            play_sound("game-start.mp3", 0.7)
            reset_lives()
        if instructions_button.draw():
            game_state = {key: False if key != 'instructions' else True for key in game_state}
    elif game_state["instructions"]:
        place_text(WIDTH / 2, 30, "Instructions :", 50)
        place_text(WIDTH / 2, 150, "Echap : Pauser ou résumer une partie", 33)
        place_text(200, 230, "Q : Terminer une partie", 33)
        place_text(330, 310, "config.js : Changer certains paramètres.", 30)
        if menu_button.draw():
            restart()
            game_state = {key: False if key != 'main_menu' else True for key in game_state}
    if not game_state["playing"]:
        pygame.mouse.set_visible(True)
    pygame.display.flip()
