import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image_path, health_color, shield_color, bar_outline_color):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 2
        self.max_health = 100
        self.health = 100
        self.max_shield = 50
        self.shield = 50
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.health_color = health_color
        self.shield_color = shield_color
        self.bar_outline_color = bar_outline_color

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def draw_health_bar(self, surface):
        bar_length = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        outline_rect = pygame.Rect(10, 10, bar_length, bar_height)
        fill_rect = pygame.Rect(10, 10, fill, bar_height)
        pygame.draw.rect(surface, self.health_color, fill_rect)
        pygame.draw.rect(surface, self.bar_outline_color, outline_rect, 2)

    def draw_shield_bar(self, surface):
        bar_length = 100
        bar_height = 10
        fill = (self.shield / self.max_shield) * bar_length
        outline_rect = pygame.Rect(10, 30, bar_length, bar_height)
        fill_rect = pygame.Rect(10, 30, fill, bar_height)
        pygame.draw.rect(surface, self.shield_color, fill_rect)
        pygame.draw.rect(surface, self.bar_outline_color, outline_rect, 2)

    def shoot(self, color):
        projectile = Projectile(self.rect.centerx, self.rect.top, self.screen_height, color)
        return projectile

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height, color):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -5
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
