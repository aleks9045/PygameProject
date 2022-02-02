
import pygame
import pyganim
from pygame import *

from player_animations import ANIMATION_IDLE, ANIMATION_GO, ANIMATION_GO_BACK
from player_animations import ANIMATION_GO_RUN, ANIMATION_GO_BACK_RUN
from more_space_for_code import starting, load_level, Timer


platforms = []
t = Timer()
pygame.init()

MOVE_SPEED = 2
SPEED_RUN = 3
tile_width = tile_height = 50
JUMP_POWER = 6
GRAVITY = 0.21


pygame.init()
pygame.display.set_caption('Bi platformer')
WIDTH = 1200
HEIGHT = 600
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 59
left = right = up = ctrl = False
toright = toleft = False
inleft = inright = False
incenter = True
music_is_playing = False
pero = False
power = False
schet_of_jump = False
jump_counter = 0

all_sprites = pygame.sprite.Group()


fon_center_learn = image.load('data/FONS/fon_center_learn.png')
fon_center = image.load('data/FONS/fon_center.png')
fon_right = image.load('data/FONS/fon_right.png')
fon_left = image.load('data/FONS/fon_left.png')
fon_left_pero = image.load('data/FONS/fon_left_pero.png')
tile_images = {
    'platform': image.load('data/DECOR/platform.png'),
    'box': image.load('data/DECOR/box.png'),
    'platform2': image.load('data/DECOR/platform2.png'),
    'platform3': image.load('data/DECOR/platform2.png'),
    'wood_platform': image.load('data/DECOR/wood_platform.png'),
    'vorona': image.load('data/DECOR/Vorona.png'),
    'pero': image.load('data/pero.png'),
    'power': image.load('data/power.png')
}

viuchilsa = False


def clear_sprites():
    global platforms
    global all_sprites
    del all_sprites
    all_sprites = pygame.sprite.Group()
    platforms.clear()


def first_start():
    global inleft, inright, incenter, toright, toleft, viuchilsa
    if inleft:
        file = 'data/ROOMS/room1.txt'
        generate_level((load_level(file)))
        Player(0, 0)
        inleft = False
        incenter = True
    elif inright:
        file = 'data/ROOMS/room1.txt'
        generate_level((load_level(file)))
        Player(23, 0)
        inright = False
        incenter = True
    elif incenter:
        if toright:
            file = 'data/ROOMS/room1_right.txt'
            generate_level((load_level(file)))
            Player(0, 0)
            toright = False
            incenter = False
            inright = True
            viuchilsa = True
        elif toleft:
            file = 'data/ROOMS/room1_left.txt'
            generate_level((load_level(file)))
            Player(23, 0)
            toleft = False
            incenter = False
            inleft = True
            viuchilsa = True
        else:
            file = 'data/ROOMS/room1.txt'
            generate_level((load_level(file)))
            Player(12, -2)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = image.load('data/IDLE/1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width + 25
        self.rect.y = y * tile_height + 85
        self.xvec = 0
        self.yvec = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.animation_idle = pyganim.PygAnimation(ANIMATION_IDLE)
        self.animation_go = pyganim.PygAnimation(ANIMATION_GO)
        self.animation_go_back = pyganim.PygAnimation(ANIMATION_GO_BACK)
        self.animation_go_run = pyganim.PygAnimation(ANIMATION_GO_RUN)
        self.animation_go_back_run = pyganim.PygAnimation(ANIMATION_GO_BACK_RUN)

    def update(self, left, right, up, platforms, ctrl):
        global inleft, inright, toright, toleft, jump_counter, schet_of_jump

        if right:
            if self.rect.x > 1200:
                if incenter:
                    toright = True
                clear_sprites()
                first_start()
            elif self.rect.x < 1182 or 50 < self.rect.y < 100:
                if ctrl and pero:
                    self.xvec = SPEED_RUN
                else:
                    self.xvec = MOVE_SPEED
                if self.onGround:
                    if ctrl:
                        self.animation_go_run.play()
                        self.animation_go_run.blit(self.image, (0, 0))
                    else:
                        self.animation_go.play()
                        self.animation_go.blit(self.image, (0, 0))
            else:
                self.xvec = 0
        if left:
            if self.rect.x < 0:
                if incenter:
                    toleft = True
                clear_sprites()
                first_start()
            elif self.rect.x > 3 or 50 < self.rect.y < 100:
                if ctrl and pero:
                    self.xvec = -SPEED_RUN
                else:
                    self.xvec = -MOVE_SPEED
                if self.onGround:
                    if ctrl:
                        self.animation_go_back_run.play()
                        self.animation_go_back_run.blit(self.image, (0, 0))
                    else:
                        self.animation_go_back.play()
                        self.animation_go_back.blit(self.image, (0, 0))
            else:
                self.xvec = 0

        if not (left or right):
            self.xvec = 0
            if not up:
                self.animation_idle.play()
                self.animation_idle.blit(self.image, (0, 0))

        if self.onGround:
            jump_counter = 0

        if up:
            if self.onGround:
                schet_of_jump = True
                self.yvec = -JUMP_POWER

        if not self.onGround:
            self.yvec += GRAVITY
            if up and power and jump_counter > 30:
                self.yvec = -JUMP_POWER
                jump_counter = 0
                schet_of_jump = False
        self.onGround = False

        self.rect.y += self.yvec
        self.collide(0, self.yvec, platforms)

        self.rect.x += self.xvec
        self.collide(self.xvec, 0, platforms)

    def collide(self, xvec, yvec, platforms):
        global pero, power
        for num, pl in enumerate(platforms):
            for name, p in pl.items():
                if sprite.collide_rect(self, p):
                    if name == 'pero':
                        del platforms[num]
                        mixer.music.load('data/SOUND/pero.ogg')
                        mixer.music.play()
                        pero = True
                    if name == 'power':
                        del platforms[num]
                        mixer.music.load('data/SOUND/pero.ogg')
                        mixer.music.play()
                        power = True
                    if xvec > 0:
                        self.rect.right = p.rect.left

                    if xvec < 0:
                        self.rect.left = p.rect.right

                    if yvec > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvec = 0

                    if yvec < 0:
                        self.rect.top = p.rect.bottom
                        self.yvec = 2


class Obj(sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'platform3':
            self.rect = self.image.get_rect().move(tile_width * x + 25, tile_height * y)
        elif tile_type == 'vorona':
            self.rect = self.image.get_rect().move(tile_width * x, tile_height * y + 17)
        else:
            self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


def generate_level(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            if level[x][y] == '*':
                continue
            if level[x][y] == '=':
                Obj('box', y, x)
                platforms.append({'box': Obj('box', y, x)})
            elif level[x][y] == '-':
                Obj('platform', y, x)
                platforms.append({'platform': Obj('platform', y, x)})
            elif level[x][y] == ',':
                Obj('platform2', y, x)
                platforms.append({'platform2': Obj('platform2', y, x)})
            elif level[x][y] == '.':
                Obj('platform3', y, x)
                platforms.append({'platform3': Obj('platform3', y, x)})
            elif level[x][y] == '_':
                Obj('wood_platform', y, x)
                platforms.append({'wood_platform':Obj('wood_platform', y, x)})
            elif level[x][y] == '<':
                Obj('vorona', y, x)
            elif level[x][y] == '/':
                Obj('pero', y, x)
                platforms.append({'pero': Obj('pero', y, x)})
            elif level[x][y] == '|':
                Obj('power', y, x)
                platforms.append({'power': Obj('power', y, x)})


starting()
first_start()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == KEYDOWN and e.key == K_LEFT:
            left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            right = True

        if e.type == KEYUP and e.key == K_RIGHT:
            right = False
        if e.type == KEYUP and e.key == K_LEFT:
            left = False

        if e.type == KEYDOWN and e.key == K_SPACE:
            up = True
        if e.type == KEYUP and e.key == K_SPACE:
            up = False

        if e.type == KEYDOWN and e.key == K_LCTRL:
            ctrl = True
        if e.type == KEYUP and e.key == K_LCTRL:
            ctrl = False
    if inright:
        screen.blit(fon_right, (0, 0))

    elif incenter:
        if not music_is_playing:
            mixer.music.load('data/SOUND/wind.ogg')
            mixer.music.play()
            music_is_playing = True
        if viuchilsa:
            screen.blit(fon_center, (0, 0))
        else:
            screen.blit(fon_center_learn, (0, 0))
    elif inleft:
        if pero:
            screen.blit(fon_left_pero, (0, 0))
        else:
            screen.blit(fon_left, (0, 0))
    if schet_of_jump:
        jump_counter += 1
    print(jump_counter)
    all_sprites.update(left, right, up, platforms, ctrl)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
