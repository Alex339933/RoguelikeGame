import pygame as pg
from pygame.math import Vector2
from settings import *

class SpriteSheet:
    """Класс для создания раскадровки"""
    def __init__(self, fp, scale=1):
        """Метод для загрузки изображения по полученному пути"""
        sheet = pg.image.load(fp).convert_alpha()
        self.sheet = pg.transform.scale_by(sheet, scale)
        self.w, self.h = self.sheet.get_size()

    def get_image(self, x, y, width, height):
        """Метод для возвращения части изображения"""
        return self.sheet.subsurface(x, y, width, height)


class Player(pg.sprite.Sprite):
    """Класс для создания игрока"""
    speed = 5

    def __init__(self, game, sprite_sheet, pos):
        """Метод для загрузки изображения игрока"""
        super().__init__(game.all_sprites)
        self._layer = PLAYER_LAYER
        self.game = game
        sprite_sheet = SpriteSheet(sprite_sheet, 2)
        self.animation_len = 4
        self._load_images(sprite_sheet)
        self.frame = 0
        self.last_time = 0
        self.velocity = Vector2(0, 0)
        self.image = self.move_right[0]
        self.rect = self.image.get_rect(center=pos)
        self.phys_body = pg.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.25)
        self.phys_body.midbottom = self.rect.midbottom
        self.animation_cycle = self.move_right

    def _collide(self):
        """Проверяет столкновение со стенами"""
        target_rect = self.phys_body.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        return False

    def update(self):
        """Метод для обновления позиции игрока"""
        self._move()
        self._animate_images()

    def _move(self):
        """Метод для управления игроком"""
        self.velocity.update(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity.y = -1
        if keys[pg.K_s]:
            self.velocity.y = 1
        if keys[pg.K_a]:
            self.velocity.x = -1
        if keys[pg.K_d]:
            self.velocity.x = 1

        if self.velocity.length() > 1:
            self.velocity.x = 0

        self.velocity *= self.speed
        if not self._collide():
            self.rect.center += self.velocity
            self.phys_body.center += self.velocity

    def _load_images(self, sheet):
        """Движение игрока"""
        w, h = sheet.w // self.animation_len, sheet.h // self.animation_len
        self.move_up = [sheet.get_image(i * w, 0, w, h) for i in range(4)]
        self.move_left = [sheet.get_image(i * w, 1 * h, w, h) for i in range(4)]
        self.move_right = [sheet.get_image(i * w, 2 * h, w, h) for i in range(4)]
        self.move_down = [sheet.get_image(i * w, 3 * h, w, h) for i in range(4)]

    def _animate_images(self, _len=100):
        """Анимация движения"""
        now = pg.time.get_ticks()
        if now - self.last_time > _len and self.velocity.length() > 0:
            self.last_time = now
            if self.velocity.y < 0:
                self.animation_cycle = self.move_down
            elif self.velocity.y > 0:
                self.animation_cycle = self.move_up
            elif self.velocity.x > 0:
                self.animation_cycle = self.move_right
            elif self.velocity.x < 0:
                self.animation_cycle = self.move_left
            self.frame += 1
            if self.frame == 4:
                self.frame = 0
            self.image = self.animation_cycle[self.frame]