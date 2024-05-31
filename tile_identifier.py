import pygame as pg
from pygame import freetype
from settings import *

pg.init()
screen = pg.display.set_mode((544, 256))

image = pg.image.load("res/map/tilemap_packed.png")
image = pg.transform.scale(image, (544, 256))

font = pg.freetype.Font(None, 16)


index = 0
for y in range(0, 256, TILE_SIZE):
    for x in range(0, 544, TILE_SIZE):
        font.render_to(image, (x + 8, y + 10), str(index))
        pg.draw.rect(image, pg.Color("Black"), (x, y, TILE_SIZE, TILE_SIZE), width=1)
        index += 1

is_running = True

while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
    screen.blit(image, (0, 0))
    pg.display.update()