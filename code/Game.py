#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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

            if game_mode == 'EXIT':
                pygame.quit()
                sys.exit()

            stage_number = 1

            while True:
                level = Level(self.window, game_mode, stage_number)
                level_result = level.run()

                if level_result == 'win':
                    if level.stage_manager.has_next_stage():
                        stage_number = level.stage_manager.get_next_stage()
                    else:
                        break

                else:
                    break