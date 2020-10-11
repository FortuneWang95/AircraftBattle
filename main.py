import traceback
import sys
from pygame.locals import *

from AirCraft import *
from Bullet import Bullet
from Enemy import *
from Supply import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 690
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Battle")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.1)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        enemy = SmallEnemy(bg_size, 'images/enemy1.png')
        group1.add(enemy)
        group2.add(enemy)


def add_moderate_enemies(group1, group2, num):
    for i in range(num):
        enemy = ModerateEnemy(bg_size, 'images/enemy2.png')
        group1.add(enemy)
        group2.add(enemy)


def add_large_enemies(group1, group2, num):
    for i in range(num):
        enemy = LargeEnemy(bg_size, 'images/enemy3_n1.png')
        group1.add(enemy)
        group2.add(enemy)


def increase_speed(targets, speed_increment):
    for target in targets:
        target.speed += speed_increment


def paint_health_line(enemy, total_lives):
    # 绘制血槽
    pygame.draw.line(screen, BLACK, (enemy.rect.left, enemy.rect.top - 5),
                     (enemy.rect.right, enemy.rect.top - 5), 2)

    # 剩余血量
    lives_remain = enemy.lives / total_lives

    if lives_remain > 0.2:
        pygame.draw.line(screen, GREEN, (enemy.rect.left, enemy.rect.top - 5),
                         (enemy.rect.left + int(enemy.rect.width * lives_remain), enemy.rect.top - 5), 2)
    else:
        pygame.draw.line(screen, RED, (enemy.rect.left, enemy.rect.top - 5),
                         (enemy.rect.left + int(enemy.rect.width * lives_remain), enemy.rect.top - 5), 2)


def upgrade_level(level, score, small_enemies, moderate_enemies, large_enemies, enemies):
    # 根据得分增加难度
    if level == 1 and score > 5e4:
        level += 1
        upgrade_sound.play()
        # 增加3个小敌机 2个中型敌机 1个大敌机
        add_small_enemies(small_enemies, enemies, 3)
        add_moderate_enemies(moderate_enemies, enemies, 2)
        add_large_enemies(large_enemies, enemies, 1)
        # 小敌机提速
        increase_speed(small_enemies, 1)
    elif level == 2 and score > 3e5:
        level += 1
        upgrade_sound.play()
        add_small_enemies(small_enemies, enemies, 3)
        add_moderate_enemies(moderate_enemies, enemies, 2)
        add_large_enemies(large_enemies, enemies, 1)

        increase_speed(small_enemies, 1)
        increase_speed(moderate_enemies, 1)
    elif level == 3 and score > 6e5:
        level += 1
        upgrade_sound.play()
        add_small_enemies(small_enemies, enemies, 5)
        add_moderate_enemies(moderate_enemies, enemies, 3)
        add_large_enemies(large_enemies, enemies, 2)
        increase_speed(small_enemies, 1)
        increase_speed(moderate_enemies, 1)

    elif level == 4 and score > 1e6:
        level += 1
        upgrade_sound.play()
        add_small_enemies(small_enemies, enemies, 5)
        add_moderate_enemies(moderate_enemies, enemies, 3)
        add_large_enemies(large_enemies, enemies, 2)
        increase_speed(small_enemies, 1)
        increase_speed(moderate_enemies, 1)
    return level


def main():
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    running = True
    # 我方飞机
    aircraft = AirCraft(bg_size)

    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)

    # 暂停游戏
    pause = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    pause_image = pause_nor_image

    # game over
    game_over_image = pygame.image.load('images/gameover.png').convert_alpha()
    game_again_image = pygame.image.load('images/again.png').convert_alpha()
    game_over_rect = game_over_image.get_rect()
    game_over_rect.left, game_over_rect.top = (
        int(width / 2 - game_over_image.get_rect().width / 2),
        int(height / 2 - game_over_image.get_rect().height / 2))

    game_again_rect = game_again_image.get_rect()
    game_again_rect.left, game_again_rect.top = (
        int(width / 2 - game_again_image.get_rect().width / 2),
        int(height / 2 + game_again_image.get_rect().height))

    # 难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left, bomb_rect.top = 10, height - bomb_rect.height - 10
    bomb_font = pygame.font.Font('font/font.ttf', 36)
    bomb_num = 3

    # 我方飞机剩余血量
    live_font = pygame.font.Font('font/font.ttf', 24)

    # 生成敌方飞机
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    moderate_enemies = pygame.sprite.Group()
    add_moderate_enemies(moderate_enemies, enemies, 1)

    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 3)

    # 普通子弹
    bullets = []
    bullet_num = 4
    bullet_index = 0
    for i in range(bullet_num):
        bullets.append(Bullet('images/bullet1.png', aircraft.rect.midtop))

    super_bullets = []
    super_bullet_num = 8
    super_bullet_index = 0
    for i in range(super_bullet_num // 2):
        super_bullets.append(Bullet('images/bullet2.png', (aircraft.rect.centerx - 33, aircraft.rect.centery)))
        super_bullets.append(Bullet('images/bullet2.png', (aircraft.rect.centerx + 30, aircraft.rect.centery)))

    # 超级子弹定时器 只能使用指定时间
    super_bullet_time = USEREVENT + 1
    use_super_bullet = False

    # 重生无敌计时器
    invincible_time = USEREVENT + 2

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    aircraft_destroy_index = 0

    # 切换图片延迟参数
    delay = 100

    # provide a supply every 30 seconds
    bomb_supply = BombSupply(bg_size, 'images/bomb_supply.png')
    bullet_supply = BulletSupply(bg_size, 'images/bullet_supply.png')
    supply_time = USEREVENT
    pygame.time.set_timer(supply_time, 20 * 1000)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_rect.collidepoint(event.pos):
                        pause = not pause
                        if pause:
                            pygame.time.set_timer(supply_time, 0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            pygame.time.set_timer(supply_time, 20 * 1000)
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                    elif game_over_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif game_again_rect.collidepoint(event.pos):
                        aircraft.reborn()
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # 全屏炸弹
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.alive = False
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if pause:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image
            elif event.type == supply_time:
                # either bomb supply or bullet supply.
                if choice((True, False)):
                    bomb_supply.active = True
                else:
                    bullet_supply.active = True
                supply_sound.play()
            elif event.type == super_bullet_time:
                use_super_bullet = False
                pygame.time.set_timer(super_bullet_time, 0)
            elif event.type == invincible_time:
                aircraft.invincible = False
                pygame.time.set_timer(invincible_time, 0)

        level = upgrade_level(level, score, small_enemies, moderate_enemies, large_enemies, enemies)

        screen.blit(background, (0, 0))

        if aircraft.lives > 0:
            if not pause:
                # 检测用户的键盘操作
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_w] or key_pressed[K_UP]:
                    aircraft.move_up()
                elif key_pressed[K_s] or key_pressed[K_DOWN]:
                    aircraft.move_down()
                elif key_pressed[K_a] or key_pressed[K_LEFT]:
                    aircraft.move_left()
                elif key_pressed[K_d] or key_pressed[K_RIGHT]:
                    aircraft.move_right()

                # shot
                if not (delay % 10):
                    bullet_sound.play()
                    if use_super_bullet:
                        super_bullets[super_bullet_index].reset((aircraft.rect.centerx - 33, aircraft.rect.centery))
                        super_bullets[super_bullet_index + 1].reset((aircraft.rect.centerx + 30, aircraft.rect.centery))
                        super_bullet_index = (super_bullet_index + 2) % super_bullet_num
                    else:
                        bullets[bullet_index].reset(aircraft.rect.midtop)
                        bullet_index = (bullet_index + 1) % bullet_num

                # paint the bullets
                if use_super_bullet:
                    for bullet in super_bullets:
                        if bullet.active:
                            bullet.move()
                            screen.blit(bullet.image, bullet.rect)
                            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False,
                                                                      pygame.sprite.collide_mask)
                            if hit_enemies:
                                bullet.active = False
                                for enemy in hit_enemies:
                                    enemy.lives -= 1
                                    enemy.hit = True
                                    if enemy.lives == 0:
                                        enemy.alive = False
                else:
                    for bullet in bullets:
                        if bullet.active:
                            bullet.move()
                            screen.blit(bullet.image, bullet.rect)
                            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False,
                                                                      pygame.sprite.collide_mask)
                            if hit_enemies:
                                bullet.active = False
                                for enemy in hit_enemies:
                                    enemy.lives -= 1
                                    enemy.hit = True
                                    if enemy.lives == 0:
                                        enemy.alive = False

                # paint large enemies
                for each in large_enemies:
                    if each.alive:
                        each.move()
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                            each.hit = False
                        else:
                            if not delay % 5:
                                screen.blit(each.image, each.rect)
                            else:
                                screen.blit(each.other_image, each.rect)

                        paint_health_line(each, LargeEnemy.lives)

                        if -10 <= each.rect.bottom <= height:
                            enemy3_fly_sound.play(-1)
                        else:
                            enemy3_fly_sound.stop()
                    else:
                        # 毁灭
                        if not (delay % 3):
                            if e3_destroy_index == 0:
                                enemy3_down_sound.play()
                            screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                            e3_destroy_index = (e3_destroy_index + 1) % len(each.destroy_images)
                            if e3_destroy_index == 0:
                                score += 10000
                                enemy3_fly_sound.stop()
                                each.reset()

                # paint moderate enemies
                for each in moderate_enemies:
                    if each.alive:
                        each.move()
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image, each.rect)
                        # 绘制血槽
                        paint_health_line(each, ModerateEnemy.lives)
                    else:
                        if not (delay % 3):
                            if e2_destroy_index == 0:
                                enemy2_down_sound.play()
                            screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                            e2_destroy_index = (e2_destroy_index + 1) % len(each.destroy_images)
                            if e2_destroy_index == 0:
                                score += 6000
                                each.reset()

                # paint small enemies
                for each in small_enemies:
                    if each.alive:
                        each.move()
                        screen.blit(each.image, each.rect)
                    else:
                        if not (delay % 3):
                            if e1_destroy_index == 0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                            e1_destroy_index = (e1_destroy_index + 1) % len(each.destroy_images)
                            if e1_destroy_index == 0:
                                score += 1000
                                each.reset()

                # check if the aircraft was collided by any enemy
                enemies_down = pygame.sprite.spritecollide(aircraft, enemies, False, pygame.sprite.collide_mask)
                if enemies_down and not aircraft.invincible:
                    aircraft.alive = False
                    for enemy in enemies_down:
                        enemy.alive = False

                # 绘制我方飞机
                if aircraft.alive:
                    if not (delay % 5):
                        screen.blit(aircraft.image1, aircraft.rect)
                    else:
                        screen.blit(aircraft.image2, aircraft.rect)
                else:
                    if not (delay % 5):
                        if aircraft_destroy_index == 0:
                            me_down_sound.play()
                        screen.blit(aircraft.destroy_images[aircraft_destroy_index], aircraft.rect)
                        aircraft_destroy_index = (aircraft_destroy_index + 1) % len(aircraft.destroy_images)
                        if aircraft_destroy_index == 0:
                            aircraft.lives -= 1
                            aircraft.reset()
                            # 重生后给我方飞机3秒钟的无敌
                            pygame.time.set_timer(invincible_time, 3 * 1000)

                # 绘制补给
                if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image, bomb_supply.rect)
                    if pygame.sprite.collide_mask(bomb_supply, aircraft):
                        get_bomb_sound.play()
                        if bomb_num < 3:
                            bomb_num += 1
                        bomb_supply.reset()

                if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image, bullet_supply.rect)
                    if pygame.sprite.collide_mask(bullet_supply, aircraft):
                        get_bullet_sound.play()
                        use_super_bullet = True
                        pygame.time.set_timer(super_bullet_time, 5 * 1000)
                        bullet_supply.reset()

                # 绘制全屏炸弹
                screen.blit(bomb_image, bomb_rect)
                bomb_text = bomb_font.render('×%d' % bomb_num, True, WHITE)
                screen.blit(bomb_text, (10 + bomb_rect.right, bomb_rect.top + 5))

                # 绘制我方飞机生命
                if aircraft.lives:
                    screen.blit(aircraft.life_image, (
                        width - aircraft.life_image.get_rect().width - 30,
                        height - 10 - aircraft.life_image.get_rect().height))
                    live_text = live_font.render('×%d' % aircraft.lives, True, WHITE)
                    screen.blit(live_text, (width - 30, height - aircraft.life_image.get_rect().height))

                # 每次递减1，到0回到100
                delay -= 1
                if not delay:
                    delay = 100
            # 绘制暂停键
            screen.blit(pause_image, pause_rect)
        else:
            # game over
            screen.blit(game_over_image, game_over_rect)

            screen.blit(game_again_image, game_again_rect)

            pygame.mixer.music.pause()
            pygame.mixer.pause()

        # 绘制得分
        score_text = score_font.render('Score : %s' % str(score), True, WHITE)
        screen.blit(score_text, (10, 5))

        pygame.display.flip()
        # 限定最大帧率60帧
        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    else:
        traceback.print_exc()
        pygame.quit()
