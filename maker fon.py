import os
import sys
import pygame
import pyganim
from pygame import *

from player_animations import ANIMATION_IDLE, ANIMATION_GO, ANIMATION_GO_BACK
from player_animations import ANIMATION_GO_RUN, ANIMATION_GO_BACK_RUN
from more_space_for_code import starting


platforms = []
tile_width = tile_height = 50


pygame.init()
WIDTH = 1200
HEIGHT = 600
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 59

all_sprites = pygame.sprite.Group()

tile_images = {
    'fon': image.load('data/FONS/fon_right.png')
}


class Obj(sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


def generate_level(level):
    for x in range(len(level)):
        for y in range(len(level[x])):
            if level[x][y] == '*':
                Obj('fon', y, x)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


generate_level(load_level('data/ROOMS/teset.txt'))
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
