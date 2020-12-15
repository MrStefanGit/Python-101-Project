#!/usr/bin/env python3

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 204, 0)

WIDTH = 1000
HEIGHT = 1000

class GameObject:
    def __init__(self, game, position, velocity):
        self.game = game
        self.position = position
        self.velocity = velocity
        self.max_velocity = 5

class Smiley(GameObject):
    def __init__(self, game, position, velocity):
        super().__init__(game, position, velocity)

    def input(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.velocity[0] = -self.max_velocity
                if event.key == K_d:
                    self.velocity[0] = self.max_velocity
            if event.type == KEYUP:
                if event.key == K_a:
                    self.velocity[0] = 0
                if event.key == K_d:
                    self.velocity[0] = 0


    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] < 0:
            self.position[0] = WIDTH
        if self.position[0] > WIDTH:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = HEIGHT
        if self.position[1] > HEIGHT:
            self.position[1] = 0

    def draw(self):
        size = 128
        eye_position = size // 2
        eye_size = size // 8
        center = [int(self.position[0]), int(self.position[1])]
        pygame.draw.circle(self.game.window, YELLOW, center, size)
        pygame.draw.circle(self.game.window, BLACK, [center[0] - eye_position, center[1] - eye_position], eye_size)
        pygame.draw.circle(self.game.window, BLACK, [center[0] + eye_position, center[1] - eye_position], eye_size)
        
        pygame.draw.ellipse(self.game.window, BLACK, [center[0], center[1], 110, 64])
    

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My first game")

        self.gameObjects = []

        self.gameObjects += [Smiley(self, [400, 400], [0, 0])]
        self.gameObjects += [Smiley(self, [800, 400], [0, 0])]
        self.gameObjects += [Smiley(self, [400, 800], [0, 0])]

    def input(self):
        events = pygame.event.get()
        for obj in self.gameObjects:
            obj.input(events)

    def update(self):
        for obj in self.gameObjects:
            obj.update()

    def draw(self):
        self.window.fill(BLACK)

        for obj in self.gameObjects:
            obj.draw()

        # Poate aparea la examen
        pygame.display.update()

        pygame.time.Clock().tick(30)

    def run(self):
        while True:
            self.input()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
