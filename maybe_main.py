import pygame
from random import shuffle
import os
import sys


chips = []
def load_image(name, *folder, color_key=None):
    if folder == ():
        folder = 'bj_pics'
    else:
        folder = folder[0]
    fullname = os.path.join(folder, name)
    try:
        #print(fullname, folder)
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


def definding_all_the_counters():
    global WE_PLAY, COUNTER
    WE_PLAY = False #счетчик идет ли игра
    COUNTER = 0 #счетчик карт на столе, не в колоде
    diler_counter = diler_points = player_counter = player_points = 0
    #дилер и плеер каунтеры - счетчики количества карт


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
        ButtonsOnMain('deal_btn.png', 325, 675)
        ButtonsOnMain('card_back.png', 895, 102)
        ButtonsOnMain('hit_btn.png', 790, 675)
        ButtonsOnMain('stand_btn.png', 950, 650)


class ButtonsOnMain(Sprite):
    def __init__(self, photo, pos_x, pos_y):
        super().__init__(button_group)
        self.image = load_image(photo)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.movable = False
        if photo == '10chip.png' or photo == '50chip.png' or \
                photo == '100chip.png' or photo == '500chip.png':
            self.movable = True
            chips.append((pos_x, pos_y, self.image.get_size(), self.rect))  # начальные координаты
            # + размер для определения местоположения фишек в виде кортежа


def click(x, y):
    global lst, WE_PLAY
    if 325 <= x <= 444 and 675 <= y <= 794 and not WE_PLAY:
        lst = os.listdir('cards')
        shuffle(lst)
        Card([-10, 6])
    elif 790 <= x <= 910 and 675 <= y <= 795 and WE_PLAY:
        Card(player_speeds[player_counter]).hit()
    elif 950 <= x <= 1070 and 650 <= y <= 770 and WE_PLAY:
        Card(diler_speeds[diler_counter]).hit()


class Card(Sprite): #класс карт, возможно и самой игры
    def __init__(self, speed):
        super().__init__(sprite_group)
        self.card_back_x = 895 #изображение карты на колоде
        self.card_back_y = 102
        self.image = load_image('card_back.png')
        self.speed = speed
        self.rect = self.image.get_rect().move(self.card_back_x, self.card_back_y)

    def update(self, *args):
        global WE_PLAY, player_counter, diler_counter, hit_or_stand, condition
        hit_or_stand = args[0]
        if type(args[-1]) == int:
            condition = args[-1]
            print(condition)
        self.rect = self.rect.move(*self.speed)
        if self.rect.top == 402 and COUNTER == 0 and hit_or_stand == None:
            self.change() #если удовлетворяет условиям, запускается следующая карта
            Card([-10, 7])
        elif self.speed[1] == 7 and self.rect.top == 403 and hit_or_stand == None:
            self.change()
            Card([-12, 1])
        elif self.speed[0] == -12 and self.rect.left < 402 and hit_or_stand == None:
            self.change()
            player_counter = 2
            diler_counter = 1
            WE_PLAY = True
        elif hit_or_stand and condition + 50 > self.rect.left > condition and self.rect.top >= 400:
            hit_or_stand = None
            self.change()


    def change(self):
        global COUNTER
        self.speed = [0, 0] #переворачивание карты
        self.image = load_image(lst[COUNTER - 1], 'cards')
        if self.rect.left == 685:
            self.pic_rect = self.image.get_rect().move(self.rect.left + 10, self.rect.top)
        else:
            self.pic_rect = self.image.get_rect().move(self.rect.left, self.rect.top)
        COUNTER += 1
    
    def hit(self):
        global player_counter
        self.update(True, player_counter * 50 + 400)
        player_counter += 1

    def stand(self):
        global diler_counter
        self.update(False)
        diler_counter += 1


pygame.init()
screen_size = (1200, 800)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 60
definding_all_the_counters() #функция, в которой определяются все переменные, используемые в процессе игры
running = True
start_running = True
sprite_group = SpriteGroup()
button_group = SpriteGroup()
motion = False  # показатель движения фишки
diler_speeds = [[-12, 1]] #скорости/направления, с которыми дложны двигаться карты, чтобы оказаться там, где надо
player_speeds = [(-10, 6), [-10, 7], [-12, 10], [-12, 12], [-10, 12], [-7, 10], [-6, 12]] #вообще скоростей надо больше, но очень редко нужно больше чем 7. так что надеюсь, out of range'a не случится :)
index = None  # номер фишки
bet = 0  # ставка игрока
hit_or_stand = None

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
        if event.type == pygame.MOUSEBUTTONDOWN and motion:
            print(event.pos, bet)
            if 470 <= event.pos[0] <= 750 and 700 <= event.pos[1] <= 780:  # место для ставок
                if index == 0:
                    bet += 10
                elif index == 1:
                    bet += 50
                elif index == 2:
                    bet += 100
                elif index == 3:
                    bet += 500
            motion = False
            chips[index][3].top = chips[index][1]
            chips[index][3].left = chips[index][0]
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(*event.pos)
            for chip in chips:
                if chip[0] <= event.pos[0] <= chip[0] + chip[2][0] and \
                        chip[1] <= event.pos[1] <= chip[1] + chip[2][1]:
                    index = chips.index(chip)  # 0 - 10, 1 - 50, 2 - 100, 3 - 500
                    # номера в списке соответсенно фишкам
                    # узнаем на какую фишку попал игрок
                    motion = True  # двигаем
        if event.type == pygame.MOUSEMOTION and motion:
            chips[index][3].top += event.rel[1]
            chips[index][3].left += event.rel[0]
    sprite_group.update(hit_or_stand)
    sprite_group.draw(screen)
    button_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()