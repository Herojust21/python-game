# Space-Dodge

import pygame
import random
import sys

##################################################################


class ship(pygame.sprite.Sprite):
    # constructor
    def __init__(self, path, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.lives = pygame.image.load("lives.png")
        self.health = 3
        self.coins = 0

    # updates the position based on the mouse
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.border()
        self.showHealth()

    # shows the current lives on screen
    def showHealth(self):
        for index, x in enumerate(range(self.health)):
            screen.blit(self.lives, (index * 35, 10))

    # applies damage to lives
    def getDamage(self, damage):
        self.health -= damage

    # updates coin count
    def updateCoin(self, value):
        self.coins += value

        if self.coins == 30:
            self.health += self.health
            self.coins = 0

    # border limits for the ship
    def border(self):
        if self.rect.right >= 1300:
            self.rect.right = 1300

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= 700:
            self.rect.bottom = 700

##################################################################


class asteroid(pygame.sprite.Sprite):
    # constructor
    def __init__(self, path, xPos, yPos, xSpeed, ySpeed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

    # updating position based on the parameters passed in
    def update(self):
        self.rect.centerx += self.xSpeed
        self.rect.centery += self.ySpeed

        # destroying the asteroid if out of range
        if self.rect.centery >= 800:
            self.kill()

##################################################################


class coin(pygame.sprite.Sprite):
    # constructor
    def __init__(self, path, xPos, yPos, xSpeed, ySpeed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

    # updating position based on the parameters passed in
    def update(self):
        self.rect.centerx += self.xSpeed
        self.rect.centery += self.ySpeed

        # destroying the coin if out of range
        if self.rect.centery >= 800:
            self.kill()

##################################################################


class laser(pygame.sprite.Sprite):
    # constructor
    def __init__(self, path, yPos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=yPos)
        self.speed = speed

    # laser movement going up
    def update(self):
        self.rect.centery -= self.speed

        # deleting laser if out of range
        if self.rect.centery <= -50:
            self.kill()


##################################################################


def gamePlay():

    # laser
    laserGroup.draw(screen)
    # ship
    spaceShipGroup.draw(screen)
    # asteroids
    asteroidGroup.draw(screen)
    # coin
    coinGroup.draw(screen)
    # updating
    laserGroup.update()
    spaceShipGroup.update()
    asteroidGroup.update()
    coinGroup.update()

    # coin count
    coinsMessage = font.render(f"Coins {spaceShipGroup.sprite.coins}", True, (255, 0, 0))
    rectCoinsMessage = coinsMessage.get_rect(center=(1130, 30))
    screen.blit(coinsMessage, rectCoinsMessage)

    # ship/asteroid collision check
    if pygame.sprite.spritecollide(spaceShipGroup.sprite, asteroidGroup, True):
        spaceShipGroup.sprite.getDamage(1)
    # ship/coin collision check
    if pygame.sprite.spritecollide(spaceShipGroup.sprite, coinGroup, True):
        spaceShipGroup.sprite.updateCoin(1)
    # laser/asteroid collision check
    for x in laserGroup:
        pygame.sprite.spritecollide(x, asteroidGroup, True)

    return 1

##################################################################


def gameOver():

    screen.blit(fin, (450, 70))

    screen.blit(redo, (500, 300))

    restartMessage = font.render("PRESS ANY KEY TO RESTART", True, (255, 0, 0))
    rectRestartMessage = restartMessage.get_rect(center=(640, 550))
    screen.blit(restartMessage, rectRestartMessage)

    scoreMessage = font.render(f"Score {score}", True, (255, 255, 255))
    rectScoreMessage = scoreMessage.get_rect(center=(640, 600))
    screen.blit(scoreMessage, rectScoreMessage)

    coinsMessage = font.render(f"Coins collected {spaceShipGroup.sprite.coins}", True, (255, 255, 255))
    rectCoinsMessage = coinsMessage.get_rect(center=(640, 650))
    screen.blit(coinsMessage, rectCoinsMessage)


##################################################################


# creates game instance
pygame.init()
# does not display mouse cursor
pygame.mouse.set_visible(False)
# displays name of game in screen
pygame.display.set_caption("Space Dodge")
# sets the size of the screen (x, y)
screen = pygame.display.set_mode((1300, 700))
# uses the clock method
clock = pygame.time.Clock()
# font
font = pygame.font.Font("8-BIT WONDER.TTF", 40)


# planets
planet1 = pygame.image.load('planet1.png')
# ship
spaceShip = ship('ship.png', 50, 50)
spaceShipGroup = pygame.sprite.GroupSingle()
spaceShipGroup.add(spaceShip)
# asteroids
asteroidGroup = pygame.sprite.Group()
# created a event
asteroidEvent = pygame.USEREVENT
pygame.time.set_timer(asteroidEvent, 50)
# coin
coinGroup = pygame.sprite.Group()
# coin event
coinEvent = pygame.USEREVENT
pygame.time.set_timer(coinEvent, 50)
# lasers
laserGroup = pygame.sprite.Group()
# score
score = 0
# fin
fin = pygame.image.load("fin.png")
# redo
redo = pygame.image.load("redo.png")


# menu
# sd logo
sd = pygame.image.load("sd.png")
# start button
startMessage = font.render("PRESS ANY KEY TO START", True, (255, 0, 0))
rectStartMessage = startMessage.get_rect(center=(500, 350))
# menu trigger
trigger = 0


# sets the background color and fills with color
black = [0, 0, 0]
pygame.display.flip()

##################################################################

# main game loop
while True:

    # checks all events in the game
    for event in pygame.event.get():

        # game quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # random asteroid generation event
        if event.type == asteroidEvent:
            asteroidPath = random.choice(('asteroid (1).png', 'asteroid (2).png', 'asteroid (3).png', 'asteroid (4).png', 'asteroid (5).png'))
            asteroidRandX = random.randrange(0, 1280)
            asteroidRandY = random.randrange(-500, -50)
            asteroidRandSpeedX = random.randrange(-1, 1)
            asteroidRandSpeedY = random.randrange(4, 10)
            asteroidNew = asteroid(asteroidPath, asteroidRandX, asteroidRandY, asteroidRandSpeedX, asteroidRandSpeedY)
            asteroidGroup.add(asteroidNew)

        # random coin generation event
        if event.type == coinEvent:
            coinPath = "coin.png"
            coinRandX = random.randrange(0, 1280)
            coinRandY = random.randrange(-500, -50)
            coinRandSpeedX = random.randrange(-1, 1)
            coinRandSpeedY = random.randrange(4, 10)
            coinNew = coin(coinPath, coinRandX, coinRandY, coinRandSpeedX, coinRandSpeedY)
            coinGroup.add(coinNew)

        # laser event
        if event.type == pygame.MOUSEBUTTONDOWN:
            laserNew = laser("laser.png", event.pos, 12)
            laserGroup.add(laserNew)

        # restart event
        if event.type == pygame.KEYUP and spaceShipGroup.sprite.health <= 0:
            spaceShipGroup.sprite.health = 3
            asteroidGroup.empty()
            coinGroup.empty()
            score = 0
            spaceShipGroup.sprite.coins = 0

        if event.type == pygame.KEYUP and trigger == 0:
            trigger = 1

##################################################################

    # background
    screen.fill(black)
    screen.blit(planet1, (1000, 50))

    if trigger == 0:
        pygame.mouse.set_visible(True)
        screen.blit(sd, (210, 80))

        screen.blit(startMessage, rectStartMessage)

    elif trigger == 1:
        if spaceShipGroup.sprite.health > 0:
            # gameplay call
            score += gamePlay()
        else:
            # game over call
            gameOver()

    pygame.display.update()     # displays all content to the screen at 120fps
    clock.tick(120)

##################################################################
