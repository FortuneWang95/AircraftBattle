import pygame


class AirCraft(pygame.sprite.Sprite):
    LIVES = 5

    def __init__(self, bg_size, speed=10, lives=5):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('images/me1.png').convert_alpha()
        self.image2 = pygame.image.load('images/me2.png').convert_alpha()

        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect = self.image1.get_rect()
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width) // 2, self.bg_height - self.rect.height - 60
        self.speed = speed
        self.lives = lives
        self.alive = True
        self.invincible = False
        self.life_image = pygame.image.load('images/life.png').convert_alpha()
        self.destroy_images = [
            pygame.image.load('images/me_destroy_1.png').convert_alpha(),
            pygame.image.load('images/me_destroy_2.png').convert_alpha(),
            pygame.image.load('images/me_destroy_3.png').convert_alpha(),
            pygame.image.load('images/me_destroy_4.png').convert_alpha()
        ]
        self.mask = pygame.mask.from_surface(self.image1)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.bg_height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.bg_height

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.bg_width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.bg_width

    def reset(self):
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width) // 2, self.bg_height - self.rect.height - 60
        self.alive = True
        self.invincible = True

    def reborn(self):
        self.lives = AirCraft.LIVES
