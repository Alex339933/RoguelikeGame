import pygame as pg
from player import Player
from settings import *
import sys
from pathlib import Path

res = Path(sys.argv[0]).parent/"res"

pg.init()

screen = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
pg.display.set_caption(GAME_TITLE)
player = Player(res/"sprites"/"player_sheet.png", (100, 100))
all_sprites = pg.sprite.Group()
all_sprites.add(player)
is_running = True

"""Игровой цикл"""
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
    screen.fill(pg.Color("white"))

    all_sprites.draw(screen)
    all_sprites.update()

    clock.tick(FPS)
    pg.display.update()
