import pygame
import random
import math
from pygame import mixer

# Initialisation_of_pygame
pygame.init()

# creation_of_Screen
screen = pygame.display.set_mode((800, 600))

# Background
BG = pygame.image.load('Background.jpg')
# Credits: Photo by Free Nature Stock: https://www.pexels.com/photo/stars-during-nighttime-127577/

# BG Music
mixer.music.load('Back.wav')
mixer.music.play(-1)
# credits:Music track: Adventures Begin by Pufino(Source: https://freetouse.com/music)

# Title and Icon
pygame.display.set_caption("PokéRush")
icon = pygame.image.load('pokemon.png')
# Credits: Darius Dan(<a href="https://www.flaticon.com/free-icons/pokeball" title="pokeball icons">Pokeball icons created by Darius Dan - Flaticon</a>)
pygame.display.set_icon(icon)
# Player
playerImg = pygame.image.load('1.png')
playerX = 350
playerY = 450
playerX_alter = 0

# Antas
antaImg = []
antaX = []
antaY = []
antaX_alter = []
antaY_alter = []
num_antas = 6

for i in range(num_antas):
    antaImg.append(pygame.image.load('2.png'))
    antaX.append(random.randint(0, 800))
    antaY.append(random.randint(50, 150))
    antaX_alter.append(0.2)
    antaY_alter.append(30)

# Fireball
FireImg = pygame.image.load('fireball.png')
# Credit: <a href="https://www.flaticon.com/free-icons/fireball" title="fireball icons">Fireball icons created by Freepik - Flaticon</a>
FireX = 0
FireY = 450
FireX_alter = 0
FireY_alter = 1
# Ready state-Can't see the fireball on screen
Fire_state = "ready"

# Fire state-Fireball is moving


# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

Over_Font = pygame.font.Font('freesansbold.ttf', 90)

#Restart
restart_button = pygame.image.load('Reset.png')
restart_button_rect = restart_button.get_rect()
restart_button_rect.center = (400,350)

def restart():
    global game_over, score_val
    game_over = False
    score_val = 0
    reset()
def reset():
    global playerX, score_val
    playerX = 350
    score_val = 0


def game():
    games = Over_Font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(games, (200, 250))


def Show_Score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def anta(x, y, i):
    screen.blit(antaImg[i], (x, y))


def fire(x, y):
    global Fire_state
    Fire_state = "Fire"
    screen.blit(FireImg, (x + 16, y + 10))


def isCollision(antaX, antaY, FireX, FireY):
    distance = math.sqrt((math.pow(antaX - FireX, 2) + math.pow(antaY - FireY, 2)))
    if distance < 27:
        return True
    else:
        return False


# GameLoop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_alter = -0.2
                if event.key == pygame.K_RIGHT:
                    playerX_alter = +0.2
                if event.key == pygame.K_SPACE:
                    if Fire_state == "ready":
                        Fire_sound = mixer.Sound('Fireball.wav')
                        Fire_sound.play()
                        FireX = playerX
                        fire(FireX, FireY)

    screen.fill((255, 239, 213))
    # background Image
    screen.blit(BG, (0, 0))
    if not game_over:
        playerX += playerX_alter

        # addition of boundaries
        if playerX <= 0:
            playerX = 0
        elif playerX >= 724:
            playerX = 724

    for i in range(num_antas):

        # Game Over
        if antaY[i] > 440:
            for j in range(num_antas):
                antaY[j] = 2000
            game()
            break
        antaX[i] += antaX_alter[i]
        if antaX[i] <= 0:
            antaX_alter[i] = 0.2
            antaY[i] += antaY_alter[i]

        elif antaX[i] >= 724:
            antaX_alter[i] = -0.2
            antaY[i] += antaY_alter[i]

        # Collision
        collision = isCollision(antaX[i], antaY[i], FireX, FireY)
        if collision:
            EXP_sound = mixer.Sound('Explosion.wav')
            EXP_sound.play()
            FireY = 450
            Fire_state = "ready"
            score_val += 1
            antaX[i] = random.randint(0, 730)
            antaY[i] = random.randint(50, 150)

        anta(antaX[i], antaY[i], i)
    if game_over:
        game()
        reset()

    # Fireball Movement
    if FireY <= 0:
        FireY = 480
        Fire_state = "ready"
    if Fire_state == "Fire":
        fire(FireX, FireY)
        FireY -= FireY_alter
        # Reset the fireball when it goes off the screen
        if FireY <= 0:
            Fire_state = "ready"
            FireY = 450

    else:
        if event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
            reset()


    player(playerX, playerY)
    Show_Score(textX, textY)
    pygame.display.update()
