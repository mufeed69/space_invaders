import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Music
mixer.music.load("music.mp3")
mixer.music.play(-1)
# Tittle and Logo
pygame.display.set_caption(" Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load("space-invaders.png")
playerX = 360
playerY = 480
playerX_change = 0

# Enemy 1
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 4  # This is also equal to number of aliens.

# Enemy 2 -> alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []

# list of enemies for i is each enemy
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# list of aliens for a is each alien
for a in range(num_of_enemies):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(20, 150))
    alienX_change.append(3)
    alienY_change.append(40)

# BULLET
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score Text
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_X = 10
text_Y = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

font_name = pygame.font.Font("freesansbold.ttf", 24)


# My Name
def My_Name():
    name = font_name.render("By->Abdul Mufeed", True, (255, 255, 255))
    screen.blit(name, (10, 50))


def game_over_text():
    game_over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


def showscore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def alien(x, y, a):
    screen.blit(alienImg[a], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # Player Movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # GAME OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy Movment
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 150)

        enemy(enemyX[i], enemyY[i], i)

    for a in range(num_of_enemies):

        # GAME OVER
        if alienY[a] > 440:
            for b in range(num_of_enemies):
                alienY[b] = 2000
            game_over_text()
            break

        # alien Movement
        alienX[a] += alienX_change[a]
        if alienX[a] <= 0:
            alienX_change[a] = 3
            alienY[a] += alienY_change[a]
        elif alienX[a] >= 736:
            alienX_change[a] = -3
            alienY[a] += alienY_change[a]

        # Collision
        collision = isCollision(alienX[a], alienY[a], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[a] = random.randint(0, 735)
            alienY[a] = random.randint(20, 150)

        alien(alienX[a], alienY[a], a)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    showscore(text_X, text_Y)

    My_Name()

    pygame.display.update()
