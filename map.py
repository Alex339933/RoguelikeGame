import csv
import pygame as pg
import pygame.transform

from settings import *


class TileMap:
    """Класс для карты"""
    WALL_IDS = [4, 5, 6, 10, 11, 12, 13, 14, 15, 21, 22, 23, 27, 28, 29, 30, 31, 32, 33,
                38, 39, 40, 44, 45, 46, 53, 56, 57, 61, 64, 65, 66, 67, 70, 78, 81, 82, 91, 92, 93, 94, 95,
                96, 97, 98, 99, 100, 101, 111, 112, 113, 114, 115, 116, 119, 120, 121, 122, 123, 124, 125,
                130, 131, 132, 131, 135]

    def __init__(self, game, csv_path, img_path, img_tile_size, spacing=0):
        data_list = self._csv_to_list(csv_path)
        self.image_list = self._parse_images(img_path, img_tile_size, spacing)
        self._load_tiles(game, data_list, self.image_list)
        self.width = len(data_list[0]) * TILE_SIZE
        self.height = len(data_list) * TILE_SIZE

    def _csv_to_list(self, path):
        """Преобразовывает csv в список"""
        with open(path, "r") as f:
            read = csv.reader(f)
            data = list(read)
        return data
    def _parse_images(self, path, img_tile_size, spacing):
        """Возвращает список картинок"""
        images_list = []
        image = pg.image.load(path).convert()

        if img_tile_size != TILE_SIZE:
            scale = TILE_SIZE // img_tile_size
            spacing *= scale
            image = pygame.transform.scale_by(image, scale)

        width, height = image.get_size()
        for y in range(0, height, TILE_SIZE):
            for x in range(0, width, TILE_SIZE):
                tile = image.subsurface(x, y, TILE_SIZE, TILE_SIZE)
                images_list.append(tile)
        return images_list

    def _load_tiles(self, game, data_list, image_list):
        """Загрузка тайлов"""
        for y, row in enumerate(data_list):
            for x, square in enumerate(row):
                is_wall = int(square) in self.WALL_IDS
                Tile(game, x, y, image_list[int(square)], is_wall)


class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, image, is_wall=False):
        self._layer = GROUND_LAYER
        if is_wall:
            groups = game.all_sprites, game.walls
        else:
            groups = game.all_sprites
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Camera:
    """Cоздание умной камеры"""
    def __init__(self, map_w, map_h):
        self.offset = (0, 0)
        self.map_w = map_w
        self.map_h = map_h

    def apply(self, _rect):
        """возвращает прямоугольник существа"""
        return _rect.move(self.offset)

    def update(self, target):
        """Обновление камеры"""
        x = -target.rect.x + SIZE[0] // 2
        y = -target.rect.y + SIZE[1] // 2

        x = min(x, 0)
        y = min(y, 0)

        x = max(x, -self.map_w + SIZE[0])
        y = max(y, -self.map_h + SIZE[1])

        self.offset = x, y