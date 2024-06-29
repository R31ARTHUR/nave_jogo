import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type, screen_width, screen_height, health_color, shield_color):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        if self.type == "health":
            self.image.fill(health_color)
        elif self.type == "shield":
            self.image.fill(shield_color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-1000, -500)
        self.speed = random.randint(1, 3)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-1000, -500)

