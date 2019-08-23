import pygame
import math
import random
pygame.init()

# point images
HEX = pygame.image.load("Images/other/hex.png")
HEX_W = HEX.get_width()
HEX_H = HEX.get_height()


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.default = pygame.image.load("Images/player/basic_ship.png")
        self.glow = pygame.image.load("Images/player/glow.png")
        self.image = self.default
        self.rect = self.image.get_rect()
        self.screen = screen
        self.rect.center = (screen.get_width()//2, 550)
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = 6

    def move_up(self):
        if self.rect.centery > 0:
            self.rect.centery -= self.vel

    def move_down(self):
        if self.rect.centery < self.screen.get_height():
            self.rect.centery += self.vel

    def move_left(self):
        if self.rect.centerx > 0:
            self.rect.centerx -= self.vel

    def move_right(self):
        if self.rect.centerx < 480:
            self.rect.centerx += self.vel

    def make_glow(self, isGlow):
        if isGlow:
            self.image = self.glow
        else:
            self.image = self.default

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        if self.rect.right > 480:
            self.rect.right = 480
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720
        elif self.rect.top < 0:
            self.rect.top = 0


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, value, modelNum, moveCount):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = x, y
        self.health = hp
        self.point_value = value
        self.model = modelNum
        self.moveCount, self.bulletCd = moveCount, 0
        self.move = 0

    def lose_hp(self, dmg):
        self.health -= dmg

        
class Hawk(Ship):
    def __init__(self, x, y, moveCount):
        self.image = pygame.image.load("Images/enemy/hawk.png")
        Ship.__init__(self, x, y, 10, 50, 0, moveCount)
        
    def update(self):
        self.moveCount += 1
        if self.moveCount % 9:
            if not self.move:
                self.rect.centery += 1
                if self.rect.centery == 125:
                    self.move = 1
                    self.offset = self.moveCount
            else:
                self.rect.centery = 100 * math.sin(math.radians(self.moveCount - self.offset)) + 125
        if not self.bulletCd:
            self.bulletCd = 60
        else:
            self.bulletCd -= 1
        self.rect.centerx = 240 * math.sin(math.radians(self.moveCount//2))+240


class Fighter(Ship):
    def __init__(self, x, y, moveCount):
        self.image = pygame.image.load("Images/enemy/fighter.png")
        Ship.__init__(self, x, y, 100, 75, 1, moveCount)

    def update(self):
        self.moveCount += 1
        if self.moveCount % 9:
            if not self.move:
                self.rect.centery += 1
                if self.rect.centery == 125:
                    self.move = 1
                    self.offset = self.moveCount
            else:
                self.rect.centery = 100 * math.sin(math.radians(self.moveCount - self.offset)) + 125
        if not self.bulletCd:
            self.bulletCd = 30
        else:
            self.bulletCd -= 1
        self.rect.centerx = 240 * math.cos(math.radians(self.moveCount//2))+240


class Falcon(Ship):
    def __init__(self, x, y, moveCount):
        self.image = pygame.image.load("Images/enemy/falcon.png")
        Ship.__init__(self, x, y, 250, 200, 2, moveCount)

    def update(self):
        self.moveCount += 1
        if self.moveCount % 9:
            if self.rect.centery <= 80:
                self.rect.centery += 1
        if not self.bulletCd:
            self.bulletCd = 60
        else:
            self.bulletCd -= 1


class Destroyer(Ship):
    def __init__(self):
        self.image = pygame.image.load("Images/enemy/destroyer.png")
        Ship.__init__(self, 240, -500, 500, 1000, 3, 0)

    def update(self):
        self.moveCount += 1
        if self.moveCount % 15:
            if self.rect.centery <= 50:
                self.rect.centery += 1
        if not self.bulletCd:
            self.bulletCd = 45
        else:
            self.bulletCd -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, bullet_info, pos, dir=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image, self.damage, self.xdir, self.ydir = bullet_info
        if dir is not None:
            self.xdir, self.ydir = dir
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect.centerx += self.xdir
        self.rect.centery += self.ydir
        if self.rect.right <= 0 or self.rect.left >= 480 \
                or self.rect.bottom >= self.screen.get_height() or self.rect.bottom <= 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, laser_info):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = laser_info[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.duration = laser_info[1]
        self.damage = laser_info[2]

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.bottom = pygame.mouse.get_pos()[1] - 10
        if self.duration > 0:
            self.duration -= 1
        elif not self.duration:
            self.kill()


class ScoreKeeper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("Fonts/moonhouse.ttf", 30)
        self.score = 0
        self.image = self.font.render(str(self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = 5,5

    def set_score(self, score):
        self.score += score
        self.image = self.font.render(str(self.score), True, (255, 255, 255))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, screen.get_height()))
        self.shield_icon = pygame.image.load("Images/player/shield.png")
        self.image.fill((0, 0, 0))
        self.empty_hp_bar = pygame.Surface((20, screen.get_height()-20))
        self.empty_hp_bar.fill((100, 100, 100))
        self.shield = 50
        self.shield_bar = pygame.Surface((20, self.shield*14))
        self.shield_bar.fill((0, 0, 255))
        self.hp = 100
        self.hp_bar = pygame.Surface((20, self.hp*7))
        self.r = 55
        self.g = 255
        self.b = 20
        self.hp_bar.fill((self.r, self.g, self.b))
        self.rect = self.image.get_rect()
        self.rect.left = 480
        self.image.blit(self.empty_hp_bar, (10, 10))
        self.image.blit(self.hp_bar, (10, 10))
        self.image.blit(self.shield_bar, (10, 10))
        self.image.blit(self.shield_icon, (0, 676))

    def take_dmg(self, dmg):
        if self.shield <= 0:
            self.hp -= dmg
            if self.r < 256: self.r += dmg*4
            if self.r > 255: self.r = 255
            if self.r == 255 and self.g > 0: self.g -= dmg*4
            if self.g < 0: self.g = 0
            if self.b > 0: self.b -= dmg
            if self.b < 0: self.b = 0
            if self.hp >= 0:
                self.hp_bar = pygame.Surface((20, self.hp*7))
        else:
            self.shield -= dmg
            if self.shield >= 0:
                self.shield_bar = pygame.Surface((20, self.shield*14))
                self.shield_bar.fill((0, 0, 255))
            if self.shield < 0:
                self.shield_bar = pygame.Surface((20, 0))
                self.hp -= abs(self.shield)
        self.image.fill((0,0,0))
        self.hp_bar.fill((self.r, self.g, self.b))
        self.image.blit(self.empty_hp_bar, (10, 10))
        self.image.blit(self.hp_bar, (10, 710-self.hp*7))
        self.image.blit(self.shield_bar, (10, 710-self.shield*14))
        if self.shield > 0:
            self.image.blit(self.shield_icon, (0, 676))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Point(pygame.sprite.Sprite):
    def __init__(self, value, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(HEX, (HEX_W*value//100, HEX_H*value//100))
        self.value = value
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if self.rect.right > 480:
            self.rect.right = 480
        elif self.rect.left < 0:
            self.rect.left = 0
        self.rotateDir = [1, -1][random.randrange(2)]
        self.mask = pygame.mask.from_surface(self.image)
        self.fallCount = 0

    def update(self):
        if self.rect.right <= 0 or self.rect.left >= 480 or self.rect.top >= 720:
            self.kill()
        else:
            self.fallCount += 0.5
            if not self.fallCount % 1:
                self.rect.centery += 3
            self.mask = pygame.mask.from_surface(self.image)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/ui/c2.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.mask = pygame.mask.from_surface(self.image)


class Start(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("Images/ui/start_1.png"), pygame.image.load("Images/ui/start_2.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (260, 360)
        self.mask = pygame.mask.from_surface(self.image)

    def changeImage(self, cursor):
        if pygame.sprite.spritecollide(self, [cursor], False, pygame.sprite.collide_mask):
            self.image = self.images[1]
        else:
            self.image = self.images[0]


class Resume(Start):
    def __init__(self):
        Start.__init__(self)
        self.images = [pygame.image.load("Images/ui/resume_1.png"), pygame.image.load("Images/ui/resume_2.png")]
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
