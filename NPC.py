import pygame as pg
from messages import Message
from settings import *


class NPC(pg.sprite.Sprite):
    def __init__(self, image, pos, game):
        self._layer = GROUND_LAYER
        groups = game.all_sprites, game.walls
        super().__init__(*groups)
        self.game = game
        self.image = image
        self.rect = image.get_rect(center=pos)
        self.message = Message(game, pos, "бла бла бла")

    def update(self):
        if self.rect.colliderect(self.game.player):
            if not self.message.groups():
                self.message.add(self.game.all_sprites)
                self.message.print()
        elif self.message.groups():
            self.message.kill()