import os
import pygame
from pygame.locals import *
from pygame import mixer
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.init()

clock = pygame.time.Clock()
fps = 60

screenWidth = 600
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")

fontSize30 = pygame.font.SysFont("Constantia", 30)
fontSize40 = pygame.font.SysFont("Constantia", 40)

playerSpeed = 8
playerCoolDown = 150
playerBulletSpeed = 6

baseAlienCoolDown = 1000
baseAlienBulletSpeed = 3
baseRows = 4
baseColumns = 5

rows = baseRows
columns = baseColumns
alienCoolDown = baseAlienCoolDown
alienBulletSpeed = baseAlienBulletSpeed
maxAlienBullets = 3

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

backgroundImage = pygame.image.load("assets/background.jpg")

explosion1Sound = mixer.Sound("assets/explosion1.wav")
explosion2Sound = mixer.Sound("assets/explosion2.wav")
laserSound = mixer.Sound("assets/laser.wav")

for sound in (explosion1Sound, explosion2Sound, laserSound):
    sound.set_volume(0.25)

explosionImages = []
for i in range(1, 6):
    explosionImages.append(pygame.image.load(f"assets/explosion{i}.png"))

scoreFilePath = "assets/highestscore.txt"
if not os.path.exists(scoreFilePath):
    with open(scoreFilePath, "w") as f:
        f.write("0")

with open(scoreFilePath, "r") as f:
    highestScore = int(f.read().strip())

def drawText(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

def applyLevelSettings():
    global alienCoolDown, alienBulletSpeed, rows, columns, maxAlienBullets
    alienCoolDown = max(300, baseAlienCoolDown - (level - 1) * 120)
    alienBulletSpeed = baseAlienBulletSpeed + (level - 1)
    rows = baseRows + level - 1
    columns = baseColumns
    maxAlienBullets = min(10, 3 + level)

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.initialHealth = health
        self.healthRemaining = health
        self.lastShot = 0

    def update(self, bulletGroup):
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.rect.left > 0:
            self.rect.x -= playerSpeed
        if key[K_RIGHT] and self.rect.right < screenWidth:
            self.rect.x += playerSpeed
        if key[K_UP] and self.rect.top > 0:
            self.rect.y -= playerSpeed
        if key[K_DOWN] and self.rect.bottom < screenHeight - 20:
            self.rect.y += playerSpeed

        timeNow = pygame.time.get_ticks()
        if key[K_SPACE] and timeNow - self.lastShot > playerCoolDown:
            laserSound.play()
            bulletGroup.add(Bullets(self.rect.centerx, self.rect.top))
            self.lastShot = timeNow

        return self.healthRemaining <= 0

    def drawHealth(self):
        pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom + 5, self.rect.width, 10))
        if self.healthRemaining > 0:
            ratio = self.healthRemaining / self.initialHealth
            pygame.draw.rect(
                screen,
                green,
                (self.rect.x, self.rect.bottom + 5, int(self.rect.width * ratio), 10),
            )

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, alienGroup, explosionGroup):
        global score
        self.rect.y -= playerBulletSpeed
        if self.rect.bottom < 0:
            self.kill()
            return
        hit = pygame.sprite.spritecollide(self, alienGroup, True)
        if hit:
            score += 10 * level
            explosion1Sound.play()
            explosionGroup.add(Explosion(self.rect.centerx, self.rect.centery, 2))
            self.kill()

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, column):
        super().__init__()
        self.image = pygame.image.load(f"assets/alien{random.randint(1,5)}.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.movementDirection = 1
        self.movementCounter = 0
        self.speed = min(4, 1 + (level - 1) * 0.3)
        self.column = column

    def update(self):
        self.rect.x += self.movementDirection * self.speed
        self.movementCounter += 1
        if self.movementCounter >= 75:
            self.movementDirection *= -1
            self.movementCounter = 0

class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.image.load("assets/alien_bullet.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.target = target

    def update(self, explosionGroup):
        self.rect.y += alienBulletSpeed
        if self.rect.top > screenHeight:
            self.kill()
            return
        if pygame.sprite.collide_mask(self, self.target):
            self.target.healthRemaining -= 1
            explosion2Sound.play()
            explosionGroup.add(Explosion(self.rect.centerx, self.rect.centery, 1))
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.frames = []
        for img in explosionImages:
            if size == 1:
                img = pygame.transform.scale(img, (32, 32))
            elif size == 2:
                img = pygame.transform.scale(img, (64, 64))
            else:
                img = pygame.transform.scale(img, (192, 192))
            self.frames.append(img)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= 3:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]

def createAliens():
    for row in range(rows):
        for col in range(columns):
            alienGroup.add(Aliens(80 + col * 90, 100 + row * 70, col))

def getSmartShooter():
    columnAliens = {}
    for alien in alienGroup:
        if alien.column not in columnAliens or alien.rect.y > columnAliens[alien.column].rect.y:
            columnAliens[alien.column] = alien
    if columnAliens:
        return random.choice(list(columnAliens.values()))
    return None

def resetGame():
    global level, score
    level = 1
    score = 0
    applyLevelSettings()
    alienGroup.empty()
    bulletGroup.empty()
    alienBulletGroup.empty()
    explosionGroup.empty()
    createAliens()
    spaceShipe.healthRemaining = spaceShipe.initialHealth
    spaceShipe.rect.center = (screenWidth // 2, screenHeight - 100)
    return "COUNTDOWN", 3, pygame.time.get_ticks()

level = 1
score = 0
applyLevelSettings()

spaceShipe = SpaceShip(screenWidth // 2, screenHeight - 100, 3)
spaceShipeGroup = pygame.sprite.Group(spaceShipe)
bulletGroup = pygame.sprite.Group()
alienGroup = pygame.sprite.Group()
alienBulletGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()

createAliens()

gameState = "COUNTDOWN"
countDown = 3
lastCount = pygame.time.get_ticks()
alienLastShot = pygame.time.get_ticks()

run = True
while run:
    clock.tick(fps)
    screen.blit(backgroundImage, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_r and gameState == "GAME_OVER":
                gameState, countDown, lastCount = resetGame()
            if event.key == K_q and gameState == "GAME_OVER":
                run = False
            if event.key == K_RETURN and gameState == "LEVEL_COMPLETE":
                level += 1
                applyLevelSettings()
                alienGroup.empty()
                alienBulletGroup.empty()
                explosionGroup.empty()
                createAliens()
                gameState = "PLAYING"

    drawText(f"Score: {score}", fontSize30, white, 10, 10)
    drawText(f"Level: {level}", fontSize30, white, screenWidth - 120, 10)

    if gameState == "COUNTDOWN":
        drawText("GET READY!", fontSize40, white, screenWidth // 2 - 110, screenHeight // 2)
        drawText(str(countDown), fontSize40, white, screenWidth // 2 - 10, screenHeight // 2 + 50)
        if pygame.time.get_ticks() - lastCount > 1000:
            countDown -= 1
            lastCount = pygame.time.get_ticks()
            if countDown == 0:
                gameState = "PLAYING"

    elif gameState == "PLAYING":
        if pygame.time.get_ticks() - alienLastShot > alienCoolDown and len(alienBulletGroup) < maxAlienBullets:
            shooter = getSmartShooter()
            if shooter:
                alienBulletGroup.add(AlienBullets(shooter.rect.centerx, shooter.rect.bottom, spaceShipe))
                alienLastShot = pygame.time.get_ticks()

        if spaceShipe.update(bulletGroup):
            explosionGroup.add(Explosion(spaceShipe.rect.centerx, spaceShipe.rect.centery, 3))
            gameState = "GAME_OVER"

        bulletGroup.update(alienGroup, explosionGroup)
        alienGroup.update()
        alienBulletGroup.update(explosionGroup)
        explosionGroup.update()

        if not alienGroup:
            gameState = "LEVEL_COMPLETE"

    elif gameState == "LEVEL_COMPLETE":
        drawText(f"LEVEL {level} CLEARED", fontSize40, white, screenWidth // 2 - 150, screenHeight // 2)
        drawText("Press ENTER to continue", fontSize30, white, screenWidth // 2 - 180, screenHeight // 2 + 60)

    else:
        if score > highestScore:
            highestScore = score
            with open(scoreFilePath, "w") as f:
                f.write(str(highestScore))

        drawText("GAME OVER!", fontSize40, white, screenWidth // 2 - 110, screenHeight // 2 - 40)
        drawText(f"Score: {score}", fontSize30, white, screenWidth // 2 - 60, screenHeight // 2 + 10)
        drawText(f"Highest: {highestScore}", fontSize30, white, screenWidth // 2 - 80, screenHeight // 2 + 40)
        drawText("R - Restart | Q - Quit", fontSize30, white, screenWidth // 2 - 150, screenHeight // 2 + 80)

    spaceShipeGroup.draw(screen)
    bulletGroup.draw(screen)
    alienGroup.draw(screen)
    alienBulletGroup.draw(screen)
    explosionGroup.draw(screen)
    spaceShipe.drawHealth()

    pygame.display.update()

pygame.quit()