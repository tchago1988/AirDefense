#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Cons import WIN_WIDTH, WINDOW_HEIGHT
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIN_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Coastal Air Defense')

    def run(self):
        level = Level(self.window)
        level.run()