import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_file, position, speed=12):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.left, self.rect.top = position
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class SuperBullet(pygame.sprite.Sprite):
    pass
