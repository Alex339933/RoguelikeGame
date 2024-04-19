import pygame as pg
from pygame.math import Vector2


class SpriteSheet:
    """Класс для создания раскадровки"""
    def __init__(self, fp):
        """Метод для загрузки изображения по полученному пути"""
        self.sheet = pg.image.load(fp).convert_alpha()

    def get_image(self, x, y, width, height):
        """Метод для возвращения части изображения"""
        return self.sheet.subsurface(x, y, width, height)


class Player(pg.sprite.Sprite):
    """Класс для создания игрока"""
    speed = 5

    def __init__(self, sprite_sheet, pos):
        """Метод для загрузки изображения игрока"""
        super().__init__()
        self.sprite_sheet = SpriteSheet(sprite_sheet)
        self.image = self.sprite_sheet.get_image(0, 0, 32,32)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """Метод для обновления позиции игрока"""
        self._move()

    def _move(self):
        """Метод для управления игроком"""
        self.velocity = Vector2(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity.y = -1
        if keys[pg.K_s]:
            self.velocity.y = 1
        if keys[pg.K_a]:
            self.velocity.x = -1
        if keys[pg.K_d]:
            self.velocity.x = 1

        self.rect.center /= self.velocity