#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import (
    WIN_WIDTH,
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

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            self.window.fill((10, 20, 30))

            self.draw_text('COASTAL AIR DEFENSE', 42, COLOR_YELLOW, (60, 120))
            self.draw_text('A/D - P1 gira | SPACE - P1 atira', 18, COLOR_WHITE, (120, 190))
            self.draw_text('SETAS - P2 gira | ENTER - P2 atira', 18, COLOR_WHITE, (105, 220))

            for i, option in enumerate(MENU_OPTION):
                color = COLOR_GREEN if i == self.option else COLOR_WHITE

                if option == 'EXIT':
                    color = COLOR_RED if i == self.option else COLOR_WHITE

                self.draw_text(option, 34, color, (190, 330 + i * 60))

            self.draw_text('UP/DOWN - Navegar | ENTER - Confirmar', 18, COLOR_WHITE, (105, 650))

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