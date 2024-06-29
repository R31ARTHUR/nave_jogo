import pygame

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()
