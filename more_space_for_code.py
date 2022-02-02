import pygame
from pygame import *
import sys
import time
WIDTH = 1200
HEIGHT = 600
size = WIDTH, HEIGHT
tile_width = tile_height = 50

clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode(size, RESIZABLE)
flag_for_mouse = False

platforms = []
all_sprites = pygame.sprite.Group()
tile_images = {
    'platform': image.load('data/DECOR/platform.png'),
    'box': image.load('data/DECOR/box.png'),
    'platform2': image.load('data/DECOR/platform2.png'),
    'platform3': image.load('data/DECOR/platform2.png'),
    'wood_platform': image.load('data/DECOR/wood_platform.png'),
}


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["                                          Start"]

    fon = pygame.transform.scale(image.load('data/BG/bg1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('/home/aleksey/PycharmProjects/ProjectPG/data/SweetCheese.otf', 33)
    text_coord = 525
    string_rendered = font.render(intro_text[0], 1, (255, 25, 25))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.mouse.get_focused():
                mouse_pos = pygame.mouse.get_pos()
                if 550 < mouse_pos[0] < 680 and 520 < mouse_pos[1] < 580:
                    screen.blit(fon, (0, 0))
                    string_rendered = font.render(intro_text[0], 1, (225, 25, 25))
                    screen.blit(string_rendered, intro_rect)
                else:
                    screen.blit(fon, (0, 0))
                    string_rendered = font.render(intro_text[0], 1, (255, 255, 80))
                    screen.blit(string_rendered, intro_rect)
                if 550 < mouse_pos[0] < 680 and 520 < mouse_pos[1] < 580 and event.type == pygame.MOUSEBUTTONDOWN:
                    return
            if event.type == KEYDOWN and event.key == K_SPACE:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_animation():
    for i in range(1, 6, 1):
        fon = pygame.transform.smoothscale(image.load(f'data/BG/bg{i}.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
        time.sleep(1)


def starting():
    start_screen()
    pygame.mixer.music.load('data/SOUND/zastavka.ogg')
    pygame.mixer.music.play()
    start_animation()
    pygame.mixer.music.unload()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class Obj(sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'platform3':
            self.rect = self.image.get_rect().move(tile_width * x + 25, tile_height * y)
        else:
            self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


def generate_level(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            if level[x][y] == '*':
                continue
            if level[x][y] == '=':
                Obj('box', y, x)
                platforms.append(Obj('box', y, x))
            elif level[x][y] == '-':
                Obj('platform', y, x)
                platforms.append(Obj('platform', y, x))
            elif level[x][y] == ',':
                Obj('platform2', y, x)
                platforms.append(Obj('platform2', y, x))
            elif level[x][y] == '.':
                Obj('platform3', y, x)
                platforms.append(Obj('platform3', y, x))
            elif level[x][y] == '_':
                Obj('wood_platform', y, x)
                platforms.append(Obj('wood_platform', y, x))


class TimerError(Exception):
    """Пользовательское исключение, используемое для сообщения об ошибках при использовании класса Timer"""


class Timer:
    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = time.perf_counter()

        return float(f"{elapsed_time:0.1f}")