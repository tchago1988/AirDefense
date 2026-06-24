#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import (
    WIN_WIDTH,
    WINDOW_HEIGHT,
    COLOR_WHITE,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_RED,
    MENU_OPTION
)


class Menu:
    def __init__(self, window):
        self.window = window
        self.option = 0

        self.background = pygame.image.load('./asset/MenuBackground.png').convert()
        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            self.window.blit(self.background, (0, 0))

            for i, option in enumerate(MENU_OPTION):
                if i == self.option:
                    color = COLOR_GREEN
                    text = f'> {option}'
                else:
                    color = COLOR_WHITE
                    text = f'  {option}'

                if option == 'EXIT' and i == self.option:
                    color = COLOR_RED

                self.draw_text(text, 38, color, (175, 330 + i * 70))

            self.draw_text(
                'UP / DOWN - NAVEGAR',
                18,
                COLOR_WHITE,
                (155, 675)
            )

            self.draw_text(
                'ENTER - CONFIRMAR',
                18,
                COLOR_YELLOW,
                (180, 705)
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.option -= 1
                        if self.option < 0:
                            self.option = len(MENU_OPTION) - 1

                    elif event.key == pygame.K_DOWN:
                        self.option += 1
                        if self.option >= len(MENU_OPTION):
                            self.option = 0

                    elif event.key == pygame.K_RETURN:
                        if self.option == 0:
                            return 1

                        if self.option == 1:
                            return 2

                        if self.option == 2:
                            pygame.quit()
                            sys.exit()

    def draw_text(self, text, size, color, pos):
        font = pygame.font.SysFont('Arial', size, bold=True)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)