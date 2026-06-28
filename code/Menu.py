#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import (WIN_WIDTH, WINDOW_HEIGHT, FPS, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN,
                       COLOR_RED, MENU_OPTION)


class Menu:  # Main game window where the menu is displayed.
    def __init__(self, window):
        self.window = window
        # Currently selected menu option.
        self.option = 0
        # Load the menu background image.
        self.background = pygame.image.load('./asset/MenuBackground.png').convert()
        # Scale the background to fit the game window.
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WINDOW_HEIGHT))

    def run(self):  # Main menu loop.
        clock = pygame.time.Clock()
        # Load and play the menu background music.
        pygame.mixer.music.load('./asset/Menu.mp3')
        pygame.mixer.music.set_volume(0.50)
        pygame.mixer.music.play(-1)
        while True:
            clock.tick(FPS)
            # Draw the menu background.
            self.window.blit(self.background, (0, 0))
            # Draw menu components.
            self.draw_menu_options()
            self.draw_footer()
            pygame.display.flip()
            for event in pygame.event.get():
                # Close the game window.
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Select the previous menu option.
                    if event.key == pygame.K_UP:
                        self.option = (self.option - 1) % len(MENU_OPTION)
                    # Select the next menu option.
                    elif event.key == pygame.K_DOWN:
                        self.option = (self.option + 1) % len(MENU_OPTION)
                    # Confirm the selected option.
                    elif event.key == pygame.K_RETURN:
                        # Fade out the menu music before starting the game.
                        pygame.mixer.music.fadeout(800)
                        return MENU_OPTION[self.option]

    def draw_menu_options(self):  # Draws all menu options.
        font = pygame.font.SysFont('Arial', 28, bold=True)
        # Vertical position of each menu option.
        menu_y = [
            300,
            365,
            430,
            495,
            560, ]
        for i, option in enumerate(MENU_OPTION):
            # Highlight the currently selected option.
            if i == self.option:
                color = COLOR_RED if option == 'EXIT' else COLOR_GREEN
                text = f'> {option}'
            else:
                color = COLOR_WHITE
                text = f'  {option}'
            surf = font.render(text, True, color)
            # Center the option horizontally.
            x = (WIN_WIDTH - surf.get_width()) // 2
            self.window.blit(surf, (x, menu_y[i]))
        # Draw the developer signature background.
        box = pygame.Surface((340, 50))
        box.set_alpha(150)
        box.fill((0, 0, 0))
        self.window.blit(box, (118, 555))
        # Draw the developer signature below the menu.
        self.draw_text_center('@ Desenvolvido por Tiago T. Cavalheiro', 14, (144, 238, 144), 560)
        self.draw_text_center('RU1130178', 14, (144, 238, 144), 580)

    def draw_footer(self):  # Draws the menu instructions.
        self.draw_text_center('UP / DOWN - NAVEGAR', 18, COLOR_WHITE, 620)
        self.draw_text_center('ENTER - CONFIRMAR', 18, COLOR_YELLOW, 645)

    def draw_text_center(self, text, size, color, y):  # Draws centered text.
        font = pygame.font.SysFont('Arial', size, bold=True)
        surf = font.render(text, True, color)
        # Calculate the horizontal center position.
        x = (WIN_WIDTH - surf.get_width()) // 2
        self.window.blit(surf, (x, y))
