import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, bg_size, image_file, speed, factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.factor = factor
        self.hit = False
        self.rect.left, self.rect.top = \
            randint(0, self.bg_width - self.rect.width), randint(-self.factor * self.bg_height, 0)
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.alive = True
        self.rect.left, self.rect.top = \
            randint(0, self.bg_width - self.rect.width), randint(-self.factor * self.bg_height, 0)


class SmallEnemy(Enemy):
    lives = 1

    def __init__(self, bg_size, image_file, speed=2, factor=3):
        self.destroy_images = [
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),
            pygame.image.load('images/enemy1_down4.png').convert_alpha()
        ]
        self.lives = SmallEnemy.lives
        super(SmallEnemy, self).__init__(bg_size, image_file, speed, factor)

    def reset(self):
        super(SmallEnemy, self).reset()
        self.lives = SmallEnemy.lives


class ModerateEnemy(Enemy):
    lives = 8

    def __init__(self, bg_size, image_file, speed=2, factor=5):
        self.destroy_images = [
            pygame.image.load('images/enemy2_down1.png').convert_alpha(),
            pygame.image.load('images/enemy2_down2.png').convert_alpha(),
            pygame.image.load('images/enemy2_down3.png').convert_alpha(),
            pygame.image.load('images/enemy2_down4.png').convert_alpha()
        ]
        self.hit_image = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.lives = ModerateEnemy.lives
        super(ModerateEnemy, self).__init__(bg_size, image_file, speed, factor)

    def reset(self):
        super(ModerateEnemy, self).reset()
        self.lives = ModerateEnemy.lives


class LargeEnemy(Enemy):
    lives = 20

    def __init__(self, bg_size, image_file, speed=1, factor=10):
        self.destroy_images = [
            pygame.image.load('images/enemy3_down1.png').convert_alpha(),
            pygame.image.load('images/enemy3_down2.png').convert_alpha(),
            pygame.image.load('images/enemy3_down3.png').convert_alpha(),
            pygame.image.load('images/enemy3_down4.png').convert_alpha(),
            pygame.image.load('images/enemy3_down5.png').convert_alpha(),
            pygame.image.load('images/enemy3_down6.png').convert_alpha()
        ]
        self.other_image = pygame.image.load('images/enemy3_n2.png').convert_alpha()
        self.hit_image = pygame.image.load('images/enemy3_hit.png').convert_alpha()
        self.lives = LargeEnemy.lives
        super(LargeEnemy, self).__init__(bg_size, image_file, speed, factor)

    def reset(self):
        super(LargeEnemy, self).reset()
        self.lives = LargeEnemy.lives
