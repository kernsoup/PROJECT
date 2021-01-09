import pygame
from random import shuffle
import os
import sys
import time
import pickle

chips = []
rules = False

def load_image(name, *folder, color_key=None):
    if folder == ():
        folder = 'bj_pics'
    else:
        folder = folder[0]
    fullname = os.path.join(folder, name)
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


def definding_all_the_stuff():
    global WE_PLAY, COUNTER, diler_counter, diler_points, player_counter, player_points
    global diler_cards, player_cards, index, bet, hit_or_stand, loses, wins, pushes
    WE_PLAY = False  # счетчик идет ли игра
    COUNTER = 0  # счетчик карт на столе, не в колоде
    diler_counter = diler_points = player_counter = player_points = 0
    # дилер и плеер каунтеры - счетчики количества карт
    diler_cards = []
    player_cards = []


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


class StartScreen(Sprite):
    def __init__(self):
        global start_boms
        super().__init__(sprite_group)
        self.image = load_image('ss_bg.png')
        self.rect = self.image.get_rect().move(0, 0)
        start_boms = [ButtonsOnMain('ss_bg.png', 0, 0),
                      ButtonsOnMain('button1.png', 700, 250),
                      ButtonsOnMain('button2.png', 700, 350),
                      ButtonsOnMain('button3.png', 700, 450)]
        if pygame.mixer.music.get_busy():
            start_boms.append(ButtonsOnMain('sound.png', 700, 530))
        else:
            start_boms.append(ButtonsOnMain('no_sound.png', 700, 530))

    def click(x, y):
        global start_running, main, manual
        if 700 <= x <= 878 and 250 <= y <= 316:
            start_running = False
            button_group.empty()
            main = Main(0, -10)
        elif 700 <= x <= 898 and 350 <= y <= 416:
            start_running = False
            button_group.empty()
            Rules()
        elif 700 <= x <= 935 and 450 <= y <= 516:
            print('loses:', loses)
            print('я сделаю кнопку там ок для статистики...')
        elif 700 <= x <= 750 and 530 <= y <= 580:
            if pygame.mixer.music.get_busy():
                ButtonsOnMain('no_sound.png', 700, 530)
                pygame.mixer.music.stop()
            else:
                ButtonsOnMain('sound.png', 700, 530)
                load_the_playlist()


class Main(Sprite):
    def __init__(self, x, y):
        global boms
        super().__init__(sprite_group)
        self.image = load_image('main_pic.png')
        self.rect = self.image.get_rect().move(x, y)
        boms = [ButtonsOnMain('back_btn.png', 0, 0),
                ButtonsOnMain('card_back.png', 895, 102),
                ButtonsOnMain('10chip.png', 1085, 103),
                ButtonsOnMain('50chip.png', 1085, 203),
                ButtonsOnMain('100chip.png', 1085, 303),
                ButtonsOnMain('500chip.png', 1085, 403),
                ButtonsOnMain('deal_btn.png', 165, 650),
                ButtonsOnMain('hit_btn.png', 790, 675),
                ButtonsOnMain('stand_btn.png', 950, 650),
                ButtonsOnMain('Double.png', 325, 675)]


class ButtonsOnMain(Sprite):
    def __init__(self, photo, pos_x, pos_y):
        super().__init__(button_group)
        self.image = load_image(photo)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        #self.movable = False
        if photo == '10chip.png' or photo == '50chip.png' or \
                photo == '100chip.png' or photo == '500chip.png':
        #    self.movable = True
            chips.append((pos_x, pos_y, self.image.get_size(), self.rect))  # начальные координаты
            # + размер для определения местоположения фишек в виде кортежа


def click(x, y):
    global lst, WE_PLAY, you_can, main, boms, start_running, sets_working, chips, rules, diler_points, player_points
    global balance, bet
    if rules:
        if x <= 62 and y <= 62:
            rules = False
            start_running = True
            StartScreen()
            start_main()
    elif 165 <= x <= 284 and 650 <= y <= 769 and not WE_PLAY:
        if bet == 0:
            print('no <3')
        else:
            line_group.empty()
            card_group.empty()
            definding_all_the_stuff()
            lst = os.listdir('cards')
            shuffle(lst)
            Card([-10, 6])
    elif 790 <= x <= 910 and 675 <= y <= 795 and WE_PLAY:
        Card(player_speeds[player_counter]).hit()
    elif 950 <= x <= 1070 and 650 <= y <= 770 and WE_PLAY:
        Card(diler_speeds[diler_counter]).stand()
    elif 325 <= x <= 445 and 675 <= y <= 795 and WE_PLAY and balance - bet >= 0 and player_counter == 2:
        Card(player_speeds[player_counter]).double()
    elif x <= 62 and y <= 62:
        line_group.empty()
        card_group.empty()
        diler_points = 0
        player_points = 0
        balance += bet
        bet = 0
        chips = []
        start_running = True
        main.kill()
        for elem in boms:
            elem.kill()
        StartScreen()
        start_main()


def write_the_points():
    font = pygame.font.Font(None, 50)
    text = font.render(str(diler_points), True, (54, 39, 38))
    text1 = font.render(str(player_points), True, (54, 39, 38))
    screen.blit(text, (50, 100))
    screen.blit(text1, (50, 600))


def write_bet_and_balance():
    global bet, balance
    font = pygame.font.Font(None, 40)
    new_bet = font.render(f'{bet}$', True, (54, 39, 38))
    screen.blit(new_bet, (575, 700))
    new_balance = font.render(f'{balance}$', True, (54, 39, 38))
    screen.blit(new_balance, (590, 15))


def load_the_playlist():
    pygame.mixer.music.load('bj_music/at.mp3')
    pygame.mixer.music.play()
    for elem in os.listdir('bj_music')[1:]:
        pygame.mixer.music.queue('bj_music/' + elem)


class Game():
    def there_are_aces(self, lst):
        counter = 0
        for card in lst:
            if 'A' in card:
                counter += 1
            else:
                counter += int(card.split('_')[0])
        return counter

    def lose(self):
        global WE_PLAY, bet, loses
        image = load_image("you_lose.png")
        line = pygame.sprite.Sprite(line_group)
        line.image = image
        line.rect = line.image.get_rect().move(0, 500)
        WE_PLAY = False
        loses += 1
        bet = 0

    def win(self):
        global WE_PLAY, balance, bet, wins
        image = load_image("you_win.png")
        line = pygame.sprite.Sprite(line_group)
        line.image = image
        line.rect = line.image.get_rect().move(0, 500)
        WE_PLAY = False
        balance += bet * 2
        wins += 1
        bet = 0

    def push(self):
        global WE_PLAY, balance, bet, pushes
        image = load_image("push.png")
        line = pygame.sprite.Sprite(line_group)
        line.image = image
        line.rect = line.image.get_rect().move(0, 500)
        WE_PLAY = False
        balance += bet
        pushes += 1
        bet = 0


class Card(Sprite):
    def __init__(self, speed):
        super().__init__(card_group)
        self.card_back_x = 895  # изображение карты на колоде
        self.card_back_y = 102
        self.stand_pressed = False
        self.end = False
        self.image = load_image('card_back.png')
        self.speed = speed
        self.rect = self.image.get_rect().move(self.card_back_x, self.card_back_y)

    def update(self, *args):
        global WE_PLAY, player_counter, diler_counter, hit_or_stand, condition, player_cards, diler_cards, can_kill
        hit_or_stand = args[0]
        if type(args[-1]) == int:
            condition = args[-1]
        self.rect = self.rect.move(*self.speed)
        if self.rect.top == 402 and COUNTER == 0 and hit_or_stand == None:
            self.change(player_cards)  # если удовлетворяет условиям, запускается следующая карта
            card_group.add(Card([-10, 7]))
        elif self.speed[1] == 7 and self.rect.top == 403 and hit_or_stand == None:
            self.change(player_cards)
            card_group.add(Card([-12, 1]))
        elif self.speed[0] == -12 and self.rect.left < 402 and hit_or_stand == None:
            self.change(diler_cards)
            player_counter = 2
            diler_counter = 1
            WE_PLAY = True
        elif hit_or_stand and condition + 50 > self.rect.left > condition and self.rect.top >= 400:
            hit_or_stand = None
            self.change(player_cards)
        elif hit_or_stand == False and condition < self.rect.left < condition + 30 and self.rect.top < 200:
            hit_or_stand = None
            self.change(diler_cards)


    def change(self, cards_list):
        global COUNTER, player_points, diler_points, player_cards, diler_cards
        self.speed = [0, 0]  # переворачивание карты
        self.image = load_image(lst[COUNTER - 1], 'cards')
        cards_list.append(lst[COUNTER - 1])
        if cards_list == player_cards:
            player_points += int(lst[COUNTER - 1].split('_')[0])
            if 'A' in ''.join(player_cards) and player_points > 21:
                player_points = game.there_are_aces(player_cards)
            if player_points > 21:
                self.end = True
                game.lose()
        else:
            diler_points += int(lst[COUNTER - 1].split('_')[0])
            if diler_points == 21 and player_points != 21:
                self.end = True
                game.lose()
            elif 'A' in ''.join(diler_cards) and diler_points > 21:
                diler_points = game.there_are_aces(diler_cards)
            if diler_points > 21:
                self.end = True
                game.win()
            elif diler_points < 17 and self.stand_pressed:
                Card(diler_speeds[diler_counter + 1]).stand()
            elif 17 <= diler_points <= 21 and 17 <= player_points <= 21:
                if diler_points < player_points:
                    self.end = True
                    game.win()
                elif diler_points > player_points:
                    self.end = True
                    game.lose()
                else:
                    self.end = True
                    game.push()
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
        self.stand_pressed = True
        self.update(False, diler_counter * 50 + 400)
        diler_counter += 1

    def double(self):
        global player_counter, bet, balance
        self.update(True, player_counter * 50 + 400)
        player_counter += 1
        balance -= bet
        bet *= 2


class Settings(Sprite):
    def __init__(self):
        global sets_working
        sets_working = True
        super().__init__(sprite_group)
        button_group.empty()
        self.image = load_image('main_pic.png', 'set_pics')
        self.rect = self.image.get_rect().move(0, 0)
        ButtonsOnMain('back_btn.png', 0, 0)
        if pygame.mixer.music.get_busy():
            ButtonsOnMain('checked.png', 500, 180)
        else:
            ButtonsOnMain('non_checked.png', 500, 180)


class Rules(Sprite):
    def __init__(self):
        global rules
        rules = True
        super().__init__(sprite_group)
        button_group.empty()
        self.image = load_image('Rules.png', 'set_pics')
        self.rect = self.image.get_rect().move(0, 0)
        ButtonsOnMain('back_btn.png', 0, 0)


pygame.init()
pygame.display.set_caption('Блэкджек')
screen_size = (1200, 800)
screen = pygame.display.set_mode(screen_size)
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
FPS = 60
# definding_all_the_stuff() #функция, в которой определяются все переменные, используемые в процессе игры
running = True
start_running = True
sprite_group = SpriteGroup()
button_group = SpriteGroup()
card_group = SpriteGroup()
line_group = SpriteGroup()
definding_all_the_stuff()
motion = False  # показатель движения фишки
index = None  # номер фишки
bet = 0  # ставка игрока
balance = 750  # СТАРТОВЫЙ БАЛАНС!!!
wins = loses = pushes = 0
with open('save.dat', 'rb') as file:
    balance, wins, loses, pushes = pickle.load(file)
hit_or_stand = None
can_kill = False
sets_working = False
TRANSPARENCY = 0
diler_speeds = [[-12, 1], [-10, 1], [-9, 1], [-8, 1], [-7, 1],
                [-6, 1]]  # скорости/направления, с которыми дложны двигаться карты, чтобы оказаться там, где надо
player_speeds = [(-10, 6), [-10, 7], [-12, 10], [-12, 12], [-10, 12], [-7, 10], [-6, 12]]
       # вообще скоростей надо больше, но очень редко нужно больше чем 7. так что надеюсь, out of range'a не случится :)
game = Game()
StartScreen()
#load_the_playlist()

def start_main():
    global start_running, running, TRANSPARENCY, start_boms
    while start_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save.dat', 'wb') as file:
                    pickle.dump([balance, wins, loses, pushes], file)
                    file.close()
                running = False
                start_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                StartScreen.click(*event.pos)
        if TRANSPARENCY < 255:
            TRANSPARENCY += 1
        screen2.set_alpha(TRANSPARENCY)
        sprite_group.draw(screen)
        button_group.draw(screen2)
        screen.blit(screen2, (0, 0))
        clock.tick(FPS)
        pygame.display.flip()

card_group = pygame.sprite.Group(Card([500, 0]))

def the_mainest():
    global running, motion, bet, balance, WE_PLAY
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save.dat', 'wb') as file:
                    pickle.dump([balance, wins, loses, pushes], file)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and motion:
                if 470 <= event.pos[0] <= 750 and 700 <= event.pos[1] <= 780:  # место для ставок
                    if index == 0 and balance >= 10:
                        bet += 10
                        balance -= 10
                    elif index == 1 and balance >= 50:
                        bet += 50
                        balance -= 50
                    elif index == 2 and balance >= 100:
                        bet += 100
                        balance -= 100
                    elif index == 3 and balance >= 500:
                        bet += 500
                        balance -= 500
                motion = False
                chips[index][3].top = chips[index][1]
                chips[index][3].left = chips[index][0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(*event.pos)
                for chip in chips:
                    if chip[0] <= event.pos[0] <= chip[0] + chip[2][0] and \
                            chip[1] <= event.pos[1] <= chip[1] + chip[2][1] and not WE_PLAY:
                        index = chips.index(chip)  # 0 - 10, 1 - 50, 2 - 100, 3 - 500
                        # номера в списке соответсенно фишкам
                        # узнаем на какую фишку попал игрок
                        motion = True  # двигаем
            if event.type == pygame.MOUSEMOTION and motion and not WE_PLAY:
                chips[index][3].top += event.rel[1]
                chips[index][3].left += event.rel[0]
        card_group.update(hit_or_stand)
        sprite_group.draw(screen)
        button_group.draw(screen)
        card_group.draw(screen)
        line_group.draw(screen)
        if not sets_working and not rules:
            write_the_points()
            write_bet_and_balance()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

start_main()
the_mainest()