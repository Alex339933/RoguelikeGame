import pygame as pg
from player import Player
from NPC import NPC
from settings import *
import sys
from pathlib import Path
from map import TileMap, Camera

res = Path(sys.argv[0]).parent/"res"

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(GAME_TITLE)
        self.is_running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.map = TileMap(self, res / "map" / "map.csv", res / "map" / "tilemap_packed.png", 16)
        self.player = Player(self, res / "sprites" / "player_sheet.png", (100, 100))
        self.camera = Camera(self.map.width, self.map.height)
        self.npc = NPC(self.map.image_list[119], (100, 200), self)

    def __events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def __update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def __draw(self):
        self.screen.fill(pg.Color("white"))
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))
        pg.display.flip()

    def run(self):
        while self.is_running:
            self.clock.tick(FPS)
            pg.display.update()
            self.__events()
            self.__update()
            self.__draw()

if __name__ == "__main__":
    app = Game()
    app.new()
    app.run()
