import random

import pygame

WIDTH, HEIGHT = 850, 500
WHITE = (255, 255, 255)
WHITE2 = (200, 200, 200)
BGCOLOR = (255, 0, 0)
GRAY = (127, 127, 127)

score = 0
balls_count = 3


class Ball(pygame.sprite.Sprite):
    size = (15, 15)
    speed = 4  # скорость передвижения

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, WHITE, self.rect, self.size[0] // 2)
        self.image.set_colorkey((0, 0, 0))
        self.rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        self.mask = pygame.mask.from_surface(self.image)  # Для правильной коллизии с шаром
        self.velocity = pygame.Vector2(self.speed * random.choice((1, -1)), -self.speed)  # Для передвижения

    def update(self):
        global score, pltf, balls_count, ball
        if self.rect.bottom + self.speed >= HEIGHT:  # Если столкнулся с нижней границей
            self.kill()
            all_sprites.remove(self)
            balls_count -= 1
            if balls_count > 0:
                ball = Ball()
            return
        if self.rect.top - self.speed <= 0:
            self.velocity.y *= -1

        if self.rect.right + self.speed >= WIDTH or self.rect.left - self.speed <= 0:
            self.velocity.x *= -1

        # Коллизия с кирпичиками
        self.rect.centerx += self.velocity.x
        # Если столкнулся справа или слева
        if pygame.sprite.spritecollide(self, Brick.bricks_group, True, pygame.sprite.collide_mask):
            self.velocity.x *= -1
            score += 1
        self.rect.centery += self.velocity.y
        # Если столкнулся сверху или снизу
        if pygame.sprite.spritecollide(self, Brick.bricks_group, True, pygame.sprite.collide_mask):
            self.velocity.y *= -1
            score += 1


class Brick(pygame.sprite.Sprite):
    bricks_group = pygame.sprite.Group()
    size = (100, 20)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, all_sprites, self.bricks_group)
        self.image = pygame.Surface(self.size)
        self.image.fill((random.randint(15, 255), random.randint(15, 255),
                         random.randint(15, 255)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    size = (70, 10)
    speed = 9

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        x, y = WIDTH // 2, HEIGHT - (self.size[0] - 20)
        self.image = pygame.Surface(self.size)
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.move = 0

    def update(self):
        global ball
        if self.rect.right + self.move < WIDTH and self.rect.left + self.move > 0:
            self.rect.x += self.move

        if self.rect.colliderect(ball.rect):  # Если была коллизия с шаром
            # Вычисляем в какую часть платформу(правую или левую)
            dx = ball.rect.centerx - self.rect.centerx
            if dx > (self.size[0] // 4):
                ball.velocity.x = ball.speed
            elif dx < -(self.size[0] // 4):
                ball.velocity.x = -ball.speed
            else:
                ball.velocity.x *= -1
            ball.velocity.y = -ball.speed


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
score_font = pygame.font.Font(pygame.font.match_font('arial'), 20)
# --- Инициализация обьектов
for y in range(5, HEIGHT // 3, Brick.size[1] + 2):
    for x in range(5, WIDTH - Brick.size[0], Brick.size[0] + 3):
        Brick(x, y)
ball = Ball()
pltf = Platform()
running = True

while running:
    clock.tick(60)  # FPS
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT:
                pltf.move = pltf.speed
            elif e.key == pygame.K_LEFT:
                pltf.move = -pltf.speed
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_RIGHT and pltf.move == pltf.speed:
                # Перестать двигаться, если до этого была зажата ВПРАВО
                pltf.move = 0
            elif e.key == pygame.K_LEFT and pltf.move == -pltf.speed:
                # Перестать двигаться, если до этого была зажата ВЛЕВО
                pltf.move = 0

    # --- Отрисовка
    screen.fill(BGCOLOR)
    all_sprites.draw(screen)
    if balls_count == 0:  # Если шары закончились
        text = score_font.render(f'GAME OVER', True, (255, 0, 0))
        for y in range(0, HEIGHT, text.get_height() + 5):
            for x in range(0, WIDTH, text.get_width() + 5):
                screen.blit(text, (x, y))
    else:
        all_sprites.update()
        screen.blit(score_font.render(f'Score: {score}', True, (60, 60, 60)), (1, HEIGHT - 30))
        for i in range(1, balls_count):  # Отрисовка оставшихся щаров
            pygame.draw.ellipse(screen, WHITE2, (WIDTH - (ball.size[0] * i + 5),
                                                 HEIGHT - ball.size[1], *ball.size))
    pygame.display.flip()