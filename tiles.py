import pygame, csv, os
from enemy import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles, self.enemy_list = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def update(self, camera,player):
        for enemy in self.enemy_list:
            enemy.update(camera, self.tiles,player,self.enemy_list)

    def draw_map(self, surface, camera):
        surface.blit(self.map_surface, (0 - camera.offset.x, 0 - camera.offset.y))

    def draw_enemies(self, surface, camera):
        for enemy in self.enemy_list:
            enemy.draw(surface, camera)

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        enemy_list = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '-2':
                    self.start_x = x * self.tile_size
                    self.start_y = y * self.tile_size
                elif tile == '-3':
                    enemy_list.append(Enemy(x * self.tile_size, y * self.tile_size))
                
                elif tile == '0':
                    tiles.append(Tile('dirt1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '1':
                    tiles.append(Tile('dirt2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('dirt3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '12':
                    tiles.append(Tile('dirt4.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '13':
                    tiles.append(Tile('dirt5.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '14':
                    tiles.append(Tile('dirt6.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '24':
                    tiles.append(Tile('dirt7.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '25':
                    tiles.append(Tile('dirt8.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '26':
                    tiles.append(Tile('dirt9.png', x * self.tile_size, y * self.tile_size, self.spritesheet))

                elif tile == '3':
                    tiles.append(Tile('idirt1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('idirt2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('idirt3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '15':
                    tiles.append(Tile('idirt4.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '16':
                    tiles.append(Tile('idirt5.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '17':
                    tiles.append(Tile('idirt6.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '27':
                    tiles.append(Tile('idirt7.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '28':
                    tiles.append(Tile('idirt8.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '29':
                    tiles.append(Tile('idirt9.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1
            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        print(enemy_list)
        return tiles, enemy_list
