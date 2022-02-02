import pygame, sys

# Создаём окно
width_screen, height_screen = 400, 440
window = pygame.display.set_mode([400, 400])
pygame.display.set_caption('MINIGAME')

screen = pygame.Surface([width_screen, height_screen])
score = pygame.Surface([400, 40])

mouse = pygame.mouse.get_pos()


# добавим минюшку
def load_menu():
    items = [(160, 140, 'Open', (0, 0, 0), (255, 0, 0), 0),
             (160, 210, 'Quit', (0, 0, 0), (255, 0, 0), 1)]

    pygame.key.set_repeat(0, 0)
    pygame.mouse.set_visible(True)

    done = False
    item = 0
    while not done:
        screen.fill([131, 35, 35])
        score.fill([131, 35, 35])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if item == 0:
                    done = True
                elif item == 1:
                    pygame.quit()
                    sys.exit()

        pointer = pygame.mouse.get_pos()
        for i in items:
            if i[0] < pointer[0] < i[0] + 155 and i[1] < pointer[1] < i[1] + 50:
                item = i[5]

        for i in items:
            if item == i[5]:
                screen.blit(myFont.render(i[2], True, i[4]), [i[0], i[1] - 40])
            else:
                screen.blit(myFont.render(i[2], True, i[3]), [i[0], i[1] - 40])

        window.blit(score, [0, 0])
        window.blit(screen, [0, 40])
        pygame.display.flip()


def shooter_button():
    """Вызывается при нажатии ЛКМ и коллизии курсора с кнопкой"""
    # TODO функционал копки Shooter
    print(1)
    import main.py
def snake_button():
    """Вызывается при нажатии ЛКМ и коллизии курсора с кнопкой"""
    # TODO функционал копки Shooter
    import zmei.py
    print(2)
def arcanoid_button():
    """Вызывается при нажатии ЛКМ и коллизии курсора с кнопкой"""
    # TODO функционал копки Shooter
    import arcanoid.py
    print(3)

pygame.font.init()
myFont = pygame.font.Font('murderer.ttf', 38)
boomFont = pygame.font.Font('murderer.ttf', 48)
scaleFont = pygame.font.Font(None, 12)

pygame.mixer.init()
# sound = pygame.mixer.Sound('boom.wav')
load_menu()
running = True
pygame.key.set_repeat(1, 1)
counter = 0
button_text_color = (0, 0, 0)  # Изменить на нужный
buttons = [
    (pygame.Rect(width_screen // 4, 50, width_screen // 2, 40), (255, 0, 0), 'Book', shooter_button),
    (pygame.Rect(width_screen // 4, 100, width_screen // 2, 40), (255, 0, 0), 'Snake', snake_button),
    (pygame.Rect(width_screen // 4, 150, width_screen // 2, 40), (255, 0, 0), 'Arcanoid', arcanoid_button)
]  # В buttons: (Rect(тело кнопки), color, button_text, button_function)

# pygame.Rect(left, top, width, height) left и top - координаты левого верхнего угла кнопки
# координаты лучше указывать пропорционально размерам экрана(делить параметр ширины/высоты)
# так код будет понятней и можно будет легко изменить размер окна при необходимости

while running:

    # обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # Если было нажатие ЛКМ
            mouse_pos = pygame.mouse.get_pos()  # получение позиции курсора
            for rect, _, _, func in buttons:
                if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    # Если положение курсора внутри кнопки(есть коллизия)
                    func()  # Вызываем функцию кнопки

    # задайте фоновый цвет
    screen.fill([131, 35, 35])
    score.fill([51, 0, 51])

    text = myFont.render("MINIGAME", True, [255, 0, 0])
    # Вместо [255, 0, 0](list) лучше использовать (255, 0, 0)(tuple), меньше памяти жрет
    score.blit(text, [160, 0])

    # отображение окна

    window.blit(score, [0, 0])
    window.blit(screen, [0, 40])
    for rect, color, text, _ in buttons:  # Отображение кнопок
        i = pygame.Surface(rect.size)
        # Rect отображать нельзя, создаем Surface и заполняем color
        i.fill(color)
        window.blit(i, rect)
        window.blit(myFont.render(text, True, button_text_color), rect)
    pygame.display.flip()
    pygame.time.delay(5)

pygame.quit()