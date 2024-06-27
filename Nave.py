import pygame
import sys
import random

# Inicialização do pygame
pygame.init()

# Configurações da janela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixelgames")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Fonte
font = pygame.font.SysFont(None, 36)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.max_health = 100
        self.health = 100
        self.max_shield = 50
        self.shield = 50

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

    def draw_health_bar(self, surface):
        bar_length = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        outline_rect = pygame.Rect(10, 10, bar_length, bar_height)
        fill_rect = pygame.Rect(10, 10, fill, bar_height)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, RED, outline_rect, 2)

    def draw_shield_bar(self, surface):
        bar_length = 100
        bar_height = 10
        fill = (self.shield / self.max_shield) * bar_length
        outline_rect = pygame.Rect(10, 30, bar_length, bar_height)
        fill_rect = pygame.Rect(10, 30, fill, bar_height)
        pygame.draw.rect(surface, CYAN, fill_rect)
        pygame.draw.rect(surface, BLUE, outline_rect, 2)

# Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)
        self.shoot_delay = random.randint(30, 100)
        self.shoot_timer = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        enemy_projectile = EnemyProjectile(self.rect.centerx, self.rect.bottom)
        all_sprites.add(enemy_projectile)
        enemy_projectiles.add(enemy_projectile)

# Classe do projétil do jogador
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Classe do projétil do inimigo
class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

# Instância do jogador
player = Player()

# Grupo de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()

all_sprites.add(player)

# Criar inimigos
for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Pontuação
score = 0

# Loop principal do jogo
def main():
    global score
    running = True

    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(player.rect.centerx, player.rect.top)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)

        # Lógica do jogo
        all_sprites.update()

        # Verificar colisões entre projéteis e inimigos
        for projectile in projectiles:
            hits = pygame.sprite.spritecollide(projectile, enemies, True)
            if hits:
                score += 10
                projectile.kill()
                for hit in hits:
                    new_enemy = Enemy()
                    all_sprites.add(new_enemy)
                    enemies.add(new_enemy)

        # Verificar colisões entre projéteis dos inimigos e o jogador
        if pygame.sprite.spritecollideany(player, enemy_projectiles):
            player.health -= 1  # Exemplo de dano simples
            for projectile in pygame.sprite.spritecollide(player, enemy_projectiles, True):
                projectile.kill()

        # Verificar colisões entre jogador e inimigos
        if pygame.sprite.spritecollideany(player, enemies):
            player.health -= 1  # Exemplo de dano simples

        # Renderização
        screen.fill(WHITE)
        all_sprites.draw(screen)
        player.draw_health_bar(screen)
        player.draw_shield_bar(screen)

        # Exibir pontuação
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (screen_width - 150, 10))

        # Atualiza a tela
        pygame.display.flip()

if __name__ == "__main__":
    main()
