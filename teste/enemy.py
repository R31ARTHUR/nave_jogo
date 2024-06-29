import pygame
import random
from enemy_projectile import EnemyProjectile

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1,1)
        self.shoot_delay = random.randint(30, 100)
        self.shoot_timer = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1,1)

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        enemy_projectile = EnemyProjectile(self.rect.centerx, self.rect.bottom, self.screen_height)
        self.groups()[0].add(enemy_projectile)
