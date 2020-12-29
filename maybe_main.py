import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('bj_pics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Игра',
                  'Настройки',
                  'что-то еще']

    screen.fill(pygame.Color(0, 100, 0))
    ButtonsOnStart('button1.png', 500, 200)
    ButtonsOnStart('button2.png', 500, 300)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class ButtonsOnStart(Sprite):
    def __init__(self, photo, x, y):
        super().__init__(sprite_group)
        self.image = load_image(photo)
        self.rect = self.image.get_rect().move(x, y)
    
    def click(x, y):
        global start_running
        if 500 <= x <= 649 and 200 <= y <= 262:
            start_running = False
            Main(0, -10)
        elif 500 <= x <= 649 and 300 <= y <= 362:
            print('stan jihyo')
            
    
class Main(Sprite):
    def __init__(self, x, y):
        super().__init__(sprite_group)
        self.image = load_image('main_pic.png')
        self.rect = self.image.get_rect().move(x, y)
        ButtonsOnMain('10chip.png', 1085, 103)
        ButtonsOnMain('50chip.png', 1085, 203)
        ButtonsOnMain('100chip.png', 1085, 303)
        ButtonsOnMain('500chip.png', 1085, 403)


class ButtonsOnMain(Sprite):
    def __init__(self, photo, pos_x, pos_y):
        super().__init__(button_group)
        self.image = load_image(photo)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

pygame.init()
screen_size = (1200, 800)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 50
running = True
start_running = True
sprite_group = SpriteGroup()
button_group = SpriteGroup()

while start_running:
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ButtonsOnStart.click(*event.pos)
    sprite_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    sprite_group.draw(screen)
    button_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()