import pygame
import sys
import random
from player import Player
from enemy import Enemy
from powerup import PowerUp

# Inicialização do pygame
pygame.init()

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

# Instância do jogador
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, '/home/professor/nave_jogo/teste/player.png', GREEN, RED, CYAN)

# Grupo de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
power_ups = pygame.sprite.Group()

all_sprites.add(player)

# Criar inimigos
for i in range(5):
    enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, '/home/professor/nave_jogo/teste/inimigo.png')
    all_sprites.add(enemy)
    enemies.add(enemy)

# Pontuação
score = 0

# Função para aumentar a dificuldade
def increase_difficulty():
    global score
    if score % 50 == 0:
        enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, '/home/professor/nave_jogo/teste/inimigo.png')
        all_sprites.add(enemy)
        enemies.add(enemy)

# Função para criar power-ups
def create_power_up():
    power_up_types = ["health", "shield"]
    power_up = PowerUp(random.choice(power_up_types), SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, CYAN)
    all_sprites.add(power_up)
    power_ups.add(power_up)

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
                    projectile = player.shoot(YELLOW)
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
                    new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, '/home/professor/nave_jogo/teste/inimigo.png')
                    all_sprites.add(new_enemy)
                    enemies.add(new_enemy)
                increase_difficulty()

        # Verificar colisões entre projéteis dos inimigos e o jogador
        for projectile in pygame.sprite.spritecollide(player, enemy_projectiles, True):
            if player.shield > 0:
                player.shield -= 10
            else:
                player.health -= 10
            projectile.kill()

        # Verificar colisões entre jogador e inimigos
        for enemy in pygame.sprite.spritecollide(player, enemies, True):
            if player.shield > 0:
                player.shield -= 20
            else:
                player.health -= 20

        # Verificar colisões entre jogador e power-ups
        for power_up in pygame.sprite.spritecollide(player, power_ups, True):
            if power_up.type == "health":
                player.health = min(player.health + 20, player.max_health)
            elif power_up.type == "shield":
                player.shield = min(player.shield + 20, player.max_shield)

        # Criar power-ups aleatoriamente
        if random.random() < 0.01:
            create_power_up()

        # Renderização
        screen.fill(WHITE)
        all_sprites.draw(screen)
        player.draw_health_bar(screen)
        player.draw_shield_bar(screen)

        # Exibir pontuação
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        # Atualiza a tela
        pygame.display.flip()

if __name__ == "__main__":
    main()
