#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import (
    WIN_WIDTH,
    WINDOW_HEIGHT,
    FPS,
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
        pygame.mixer.music.load('./asset/Menu.mp3')  # Música do Menu
        pygame.mixer.music.set_volume(0.50)
        pygame.mixer.music.play(-1)

        while True:
            clock.tick(FPS)
            self.window.blit(self.background, (0, 0))
            self.draw_menu_options()
            self.draw_footer()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.option = (self.option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_DOWN:
                        self.option = (self.option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN:
                        # Faz uma transição suave para a música da fase
                        pygame.mixer.music.fadeout(800)
                        return MENU_OPTION[self.option]

    def draw_menu_options(self):
        font = pygame.font.SysFont('Arial', 28, bold=True)
        menu_y = [
            300,
            365,
            430,
            495,
            560,
        ]

        for i, option in enumerate(MENU_OPTION):
            if i == self.option:
                color = COLOR_RED if option == 'EXIT' else COLOR_GREEN
                text = f'> {option}'
            else:
                color = COLOR_WHITE
                text = f'  {option}'
            surf = font.render(text, True, color)
            x = (WIN_WIDTH - surf.get_width()) // 2
            self.window.blit(surf, (x, menu_y[i]))

    def draw_footer(self):
        self.draw_text_center(
            'UP / DOWN - NAVEGAR',
            18,
            COLOR_WHITE,
            620)
        self.draw_text_center(
            'ENTER - CONFIRMAR',
            18,
            COLOR_YELLOW,
            645
        )

    def draw_text_center(self, text, size, color, y):
        font = pygame.font.SysFont('Arial', size, bold=True)
        surf = font.render(text, True, color)
        x = (WIN_WIDTH - surf.get_width()) // 2
        self.window.blit(surf, (x, y))