"""Bullet Hell Game
    None of the sprites or art is mine
    Written by: James Wang
    Date Last Edited: August 17, 2019
    5 waves of enemies. Use the mouse to control your ship and defeat them all.
    There are 4 classes of enemy ships, and they each have different qualities.
    You start with a 50 hp shield. Once the shield is gone you will take damage.
    When your health drops to 0 you lose and will return to the start screen.
    Not very fancy UI and not very polished.
    Pressing Q with enough energy (10) will activate the laser, which does damage per tick,
    and destroys enemy bullets. Each enemy that you kill gives you 1 energy.
"""
import pygame
import bhClasses as bhc
import math
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,30)
pygame.init()

# GLOBALS
VOLUME = 0.3
SCREENSIZE = (520, 720)
SCREEN = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Bullet Hell')
CLOCK = pygame.time.Clock()
CURSOR = bhc.Cursor()
pygame.mouse.set_visible(False)

# Backgrounds
BG1 = pygame.image.load("Images/backgrounds/bg_1.png")
BG2 = pygame.image.load("Images/backgrounds/bg_2.png")

# Lasers
# Image, duration (ticks), damage per tick for lasers
LASER_0 = (pygame.image.load("Images/player/laser_0.png"), 240, 1)

# Image, damage, speed, cd for bullets
BULLET_0 = (pygame.image.load("Images/player/bullet_0.png"), 1, 0, -4)
BULLET_1 = (pygame.image.load("Images/player/bullet_1.png"), 2, 0, -5)
BULLET_2 = (pygame.image.load("Images/player/bullet_2.png"), 4, 0, -6)
BULLET_3 = (pygame.image.load("Images/player/bullet_3.png"), 6, 0, -7)
BULLET_4 = (pygame.image.load("Images/player/bullet_4.png"), 10, 0, -7)
P_BULLETS = [BULLET_0, BULLET_1, BULLET_2, BULLET_3, BULLET_4]

# Image, damage, speed, cd for enemy bullets
EN_BULLET_0 = (pygame.image.load("Images/enemy/en_bul_0.png"), 1, 0, 2)
EN_BULLET_1 = (pygame.image.load("Images/enemy/en_bul_1.png"), 5, 0, 3)
EN_BULLET_2 = (pygame.image.load("Images/enemy/en_bul_2.png"), 15, 0, 0)
EN_BULLET_3 = (pygame.image.load("Images/enemy/en_bul_3.png"), 25, 0, 2)
EN_BULLETS = [EN_BULLET_0, EN_BULLET_1, EN_BULLET_2, EN_BULLET_3]
# STAGE 1 WAVE 1
S_1_W_1 = [bhc.Hawk(240, -50, -180), bhc.Hawk(240, -100, 0), bhc.Hawk(240, -50, 180)]
# STAGE 1 WAVE 2
S_1_W_2 = [bhc.Fighter(240, -150, -135), bhc.Fighter(240, -150, 135), bhc.Fighter(240, -200, 0),
           bhc.Hawk(240, -50, -180), bhc.Hawk(240, -25, 0), bhc.Hawk(240, -50, 180),
           bhc.Hawk(240, -75, -90), bhc.Hawk(240, -75, 90)]
# STAGE 1 WAVE 3
S_1_W_3 = [bhc.Falcon(240, -300, 0), bhc.Fighter(240, -150, 90), bhc.Fighter(240, -200, 0),
           bhc.Fighter(240, -150, -90), bhc.Hawk(240, -50, -180), bhc.Hawk(240, -25, 0),
           bhc.Hawk(240, -50, 180), bhc.Hawk(240, -100, -120), bhc.Hawk(240, -75, -60),
           bhc.Hawk(240, -75, 60), bhc.Hawk(240, -100, 120)]
# STAGE 1 WAVE 4
S_1_W_4 = [bhc.Falcon(160, -350, 0), bhc.Falcon(320, -350, 0), bhc.Fighter(240, -200, -150),
           bhc.Fighter(240, -150, -90), bhc.Fighter(240, -250, 0), bhc.Fighter(240, -150, 90),
           bhc.Fighter(240, -200, 150), bhc.Hawk(240, -50, -180), bhc.Hawk(240, -25, 0),
           bhc.Hawk(240, -50, 180), bhc.Hawk(240, -100, -120), bhc.Hawk(240, -75, -60),
           bhc.Hawk(240, -75, 60), bhc.Hawk(240, -100, 120)]
# STAGE 1 WAVE 5
S_1_W_5 = [bhc.Destroyer(), bhc.Falcon(120, -350, 0), bhc.Falcon(240, -350, -135),
           bhc.Falcon(360, -350, 135),  bhc.Fighter(240, -250, -150), bhc.Fighter(240, -300, -100),
           bhc.Fighter(240, -200, -50), bhc.Fighter(240, -250, 0), bhc.Fighter(240, -200, 50),
           bhc.Fighter(240, -300, 100), bhc.Fighter(240, -250, 150), bhc.Hawk(240, -50, -180),
           bhc.Hawk(240, -25, 0), bhc.Hawk(240, -50, 180), bhc.Hawk(240, -100, -120),
           bhc.Hawk(240, -75, -60), bhc.Hawk(240, -75, 60), bhc.Hawk(240, -100, 120),
           bhc.Hawk(240, -125, 90), bhc.Hawk(240, -125, -90)]

STAGE_1 = [S_1_W_1, S_1_W_2, S_1_W_3, S_1_W_4, S_1_W_5]


def main():
    # Title screen
    bg = pygame.image.load("Images/backgrounds/title_screen_bg.png")
    # button
    start = bhc.Start()
    startGroup = pygame.sprite.Group(start)
    allSprites = pygame.sprite.OrderedUpdates(start, CURSOR)
    # Assign
    run = True
    SCREEN.blit(bg, (0, 0))

    while run:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(CURSOR, startGroup, False, pygame.sprite.collide_mask):
                    run = game()
                    SCREEN.blit(bg,(0,0))
            elif event.type == pygame.MOUSEMOTION:
                start.changeImage(CURSOR)

        allSprites.clear(SCREEN, bg)
        allSprites.update()
        allSprites.draw(SCREEN)
        pygame.display.flip()
    pygame.quit()


def game():
    SCREEN.blit(BG2, (0, 0))
    # Entities
    player = bhc.PlayerShip(SCREEN)
    # Enemies
    enemyGroup = pygame.sprite.Group()
    # Bullets
    enemyBullets = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    # player score and hp
    scoreKeeper = bhc.ScoreKeeper()
    healthBar = bhc.HealthBar(SCREEN)
    pointGroup = pygame.sprite.Group()
    # AllSprites
    allSprites = pygame.sprite.OrderedUpdates(player, pointGroup, enemyBullets, enemyGroup,
                                              bulletGroup, scoreKeeper, healthBar)
    # Assign
    run = True
    energy = 0
    shootingLaser = False
    bulletCd = 0
    game_wave = 0
    p_bul_num = 0
    bulletReloadTime = 20

    # Game loop
    while run:
        CLOCK.tick(60)

        if not enemyGroup:
            game_wave += 1
            if game_wave > 5:
                return True
            else:
                wave = STAGE_1[game_wave - 1]
            enemyGroup.add(wave)
            allSprites.add(wave)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_p]:
            run = pause()
            SCREEN.blit(BG2, (0, 0))
            pygame.time.delay(300)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_down()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        if keys[pygame.K_q] and not shootingLaser and energy >= 10:
            energy -= 10
            if energy < 10:
                player.make_glow(False)
            shootingLaser = True
            laser = bhc.Laser(SCREEN, player.rect.centerx, player.rect.top, LASER_0)
            bulletGroup.add(laser)
            allSprites.add(laser)

        # player shooting
        if not bulletCd and not shootingLaser:
            bullet = bhc.Bullet(SCREEN, P_BULLETS[int(p_bul_num)], player.rect.center)
            bulletGroup.add(bullet)
            allSprites.add(bullet)
            bulletCd = bulletReloadTime
        elif bulletCd > 0:
            bulletCd -= 1

        # Enemy ship shooting
        for enemy in enemyGroup:
            if not enemy.bulletCd:
                bullets = get_bullets(enemy)
                for bullet in bullets:
                    bullet.rotate(180)
                enemyBullets.add(bullets)
                allSprites.add(bullets)

        # player bullet and enemy ship collision, enemy ship death point drop
        hit = pygame.sprite.groupcollide(enemyGroup, bulletGroup, False, False, pygame.sprite.collide_mask)
        for enemy in hit:
            if hit[enemy][0].__class__.__name__ == 'Bullet':
                hit[enemy][0].kill()
            if enemy.rect.centery >= 0:
                enemy.lose_hp(hit[enemy][0].damage)
                if enemy.health <= 0:
                    enemy.kill()
                    energy += enemy.point_value // 50
                    if p_bul_num < 4:
                        p_bul_num += 0.5
                    x, y = enemy.rect.center
                    points = [bhc.Point(enemy.point_value//2, (x + 30, y + 30)),
                              bhc.Point(enemy.point_value//2, (x - 30, y + 30))]
                    pointGroup.add(points)
                    allSprites.add(points)

        # indicate the player can shoot a laser if they have more than 10 energy
        if energy >= 10:
            player.make_glow(True)

        try:
            hit = pygame.sprite.spritecollide(laser, enemyBullets, False, pygame.sprite.collide_mask)
            for bullet in hit:
                bullet.kill()
            if not laser.duration:
                shootingLaser = False
        except UnboundLocalError:
            pass

        for shot in pygame.sprite.spritecollide(player, enemyBullets, True, pygame.sprite.collide_mask):
            healthBar.take_dmg(shot.damage)
        if healthBar.hp <= 0:
            return True

        # point drop collision
        if pointGroup:
            for point in pygame.sprite.spritecollide(player, pointGroup, True, pygame.sprite.collide_mask):
                scoreKeeper.set_score(point.value)

        allSprites.clear(SCREEN, BG2)
        allSprites.update()
        allSprites.draw(SCREEN)
        healthBar.draw(SCREEN)
        pygame.display.flip()


def pause():
    # Assign
    run = True

    SCREEN.blit(BG1, (0, 0))
    # button
    resume = bhc.Resume()
    resumeGroup = pygame.sprite.Group(resume)
    allSprites = pygame.sprite.OrderedUpdates(resume, CURSOR)

    while run:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(CURSOR, resumeGroup, False, pygame.sprite.collide_mask):
                    return True
            elif event.type == pygame.MOUSEMOTION:
                resume.changeImage(CURSOR)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        allSprites.clear(SCREEN, BG1)
        allSprites.update()
        allSprites.draw(SCREEN)
        pygame.display.flip()


def get_bullets(enemy):
    if enemy.model == 0:
        return [bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.centerx+25, enemy.rect.centery)),
                bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.centerx-25, enemy.rect.centery))]
    elif enemy.model == 1:
        return [bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.centerx, enemy.rect.centery + 10))]
    elif enemy.model == 2:
        mx, my = pygame.mouse.get_pos()
        radians = math.atan2(my - enemy.rect.centery, mx - enemy.rect.centerx)
        dx, dy = math.cos(radians) * 3, math.sin(radians) * 3
        return [bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.centerx, enemy.rect.centery + 20), (dx, dy))]
    elif enemy.model == 3:
        return [bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.left + 9, enemy.rect.bottom - 9)),
                bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.left + 100, enemy.rect.bottom)),
                bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.centerx, enemy.rect.bottom - 36)),
                bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.right - 100, enemy.rect.bottom)),
                bhc.Bullet(SCREEN, EN_BULLETS[enemy.model], (enemy.rect.right + 9, enemy.rect.bottom - 9))]


main()
