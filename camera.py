import pygame
vec = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 480, 270

    def scroll(self):
        self.offset_float.x += (self.player.rect.x - self.offset_float.x - 108)/20
        self.offset_float.y += (self.player.rect.y - self.offset_float.y - 88)/20
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)