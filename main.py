import pygame, random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.right_image = pygame.transform.scale(pygame.image.load('archer_right.png'), (128, 128))
        self.left_image = pygame.transform.scale(pygame.image.load('archer_left.png'), (128, 128))
        self.right_image.set_colorkey(white)
        self.left_image.set_colorkey(white)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - self.image.get_size()[1] // 2)


class Book(pygame.sprite.Sprite):
    speed = 1
    spawn_rate = 5.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        i = random.randint(1, 2)
        self.image = pygame.transform.scale(pygame.image.load(f'book{i}.png'), (45, 45))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, width - 30), random.randint(0, height // 2))

    def update(self):
        global score
        self.rect.y += Book.speed
        if self.rect.colliderect(pl.rect):
            score += 1
            if (5 * Book.speed ** 2 // 2) // score == 1:
                Book.speed += 1
                if Book.speed % 2 == 0:
                    Book.spawn_rate -= 1
            self.kill()


black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

width, height = 1000, 700
pygame.init()
screen = pygame.display.set_mode((850, 700))
clock = pygame.time.Clock()
book_sprites = pygame.sprite.Group()
book_sprites.add(Book())
pl = Player()
game = True
draw_small = False
move_right, move_left = False, False
score = 0
font = pygame.font.Font(pygame.font.match_font('arial'), 40)
bfont = pygame.font.Font(pygame.font.match_font('arial'), 80)
start_ticks=pygame.time.get_ticks()
bg = pygame.image.load(f'bg1.png')
level = 1
while game:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            move_left = True
            pl.image = pl.left_image
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            move_right = True
            pl.image = pl.right_image
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            move_left = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            move_right = False
    if move_left:
        pl.rect.x -= 5
    if move_right:
        pl.rect.x += 5
    if (pygame.time.get_ticks() - start_ticks) / 1000 > Book.spawn_rate:
        book_sprites.add(Book())
        start_ticks = pygame.time.get_ticks()

    screen.fill(black)
    screen.blit(bg, (0, 0))
    if score % 25 == 0:
        screen.blit(bfont.render(f'NEXT LEVEL', True, (random.randint(0, 255), random.randint(0, 255),
                                                       random.randint(0, 255))), (width // 4, height // 2))
    if score >= 25 and score // 25 + 1 != level:
        level += 1
        if level >= 5:
            bg = pygame.image.load(f'bglast.png')
        else:
            bg = pygame.image.load(f'bg{level}.png')

    screen.blit(font.render(f'Счет: {score}', True, gray), (0, 0))
    for i in list(book_sprites):
        screen.blit(i.image, i.rect)
    book_sprites.update()
    screen.blit(pl.image, pl.rect)
    pygame.display.flip()