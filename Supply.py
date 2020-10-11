import pygame
from random import *


class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size, image_file, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width = bg_size[0]
        self.bg_height = bg_size[1]
        self.rect.left, self.rect.top = randint(0, self.bg_width - self.rect.width), - 50
        self.speed = speed
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.bg_width - self.rect.width), - 50
        self.active = False


class BombSupply(Supply):
    pass


class BulletSupply(Supply):
    pass
