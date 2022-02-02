import pygame
from random import randrange as rnd
pygame.init()

WIDTH, HEIGHT = 1200, 800
fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class GameObjectRect(pygame.sprite.Sprite):
    def __init__(self, w, h, *group):
        super().__init__(*group)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()


all_sprites = pygame.sprite.Group()


class PlayerStage(GameObjectRect):
    def __init__(self, w, h, *group):
        super().__init__(w, h, *group)
        self.stage_speed = 15
        self.rect.x = WIDTH // 2 - w // 2
        self.rect.y = HEIGHT - h - 10
        self.w = w

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.stage_speed
        if key[pygame.K_RIGHT] and self.rect.x < WIDTH - self.w:
            self.rect.x += self.stage_speed


stage = PlayerStage(330, 35, all_sprites)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = WIDTH // 2
        self.vy = HEIGHT // 2

my_ball = Ball(25, WIDTH // 2, HEIGHT // 2)


class Border(GameObjectRect):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)




    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx



class Block(GameObjectRect):
    def __init__(self, x, y,  w, h, color, *group):
        super().__init__(w, h, *group)
        self.image.fill(color)
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        pass


blocks_group = pygame.sprite.Group()
for i in range(10):
    for j in range(4):
        Block(10 + 120 * i, 10 + 70 * j, 100, 50, (rnd(30, 256), rnd(30, 256), rnd(30, 256)), blocks_group, all_sprites)

clock = pygame.time.Clock()
# фон
image = pygame.image.load('2.jpg').convert()
image = pygame.transform.scale(image, (WIDTH, HEIGHT))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(image, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()

    # экран
    pygame.display.flip()
    clock.tick(fps)