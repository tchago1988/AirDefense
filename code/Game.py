#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Cons import WIN_WIDTH, WINDOW_HEIGHT
from code.Menu import Menu
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIN_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Coastal Air Defense')

    def run(self):
        while True:
            menu = Menu(self.window)
            game_mode = menu.run()

            level = Level(self.window, game_mode)
            level.run()