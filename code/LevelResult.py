#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import (
    WIN_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    ASSET_PATH,
    MENU_OPTION,
    COLOR_WHITE,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_CYAN
)


class LevelResult:
    def __init__(self, window, result, has_next_stage):
        # Main game window where the result screen is drawn.
        self.window = window

        # Dictionary containing all level result information.
        self.result = result

        # Indicates whether there is another stage after this result screen.
        self.has_next_stage = has_next_stage

        # Background name used by the finished level.
        background_name = self.result['background']

        # Load the level background image.
        self.background = pygame.image.load(
            f'{ASSET_PATH}{background_name}.png'
        ).convert()

        # Scale the background to fit the game window.
        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

        # Create the transparent result panel.
        self.panel = pygame.Surface(
            (WIN_WIDTH - 80, WINDOW_HEIGHT - 80)
        )

        self.panel.set_alpha(185)

        # Set the panel color according to the level result.
        if self.result['status'] == 'win':
            self.panel.fill((0, 20, 10))
        else:
            self.panel.fill((25, 0, 0))

    def run(self):  # Main result screen loop.
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)

            # Draw the background and panel.
            self.window.blit(self.background, (0, 0))
            self.window.blit(self.panel, (40, 40))

            # Draw the result information.
            self.draw_screen()

            pygame.display.flip()

            for event in pygame.event.get():

                # Close the game window.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    # ENTER continues, retries, or does nothing after final victory.
                    if event.key == pygame.K_RETURN:

                        if self.result['status'] == 'win':

                            # Continue only if this is not the final stage.
                            if not self.result.get('is_final_stage', False):
                                return 'next'

                        else:
                            # Retry the level after base destruction.
                            return 'retry'

                    # R returns to the main menu.
                    elif event.key == pygame.K_r:
                        return 'menu'

    def draw_screen(self):  # Draws the complete result screen.
        stage = self.result['stage']
        is_final_stage = self.result.get('is_final_stage', False)
        game_mode = self.result.get('game_mode')

        # Configure title and ENTER action according to the result.
        if self.result['status'] == 'win':

            if is_final_stage:
                title = 'CAMPANHA CONCLUIDA!'
            else:
                title = f'LEVEL {stage} COMPLETO'

            title_color = COLOR_GREEN
            enter_text = '[ENTER] CONTINUAR'

        else:
            title = 'BASE DESTRUIDA!'
            title_color = COLOR_RED
            enter_text = '[ENTER] RECOMEÇAR LEVEL'

        # Draw the main title.
        self.draw_text_center(
            title,
            38,
            title_color,
            45
        )

        # Show new record message on the final stage.
        if is_final_stage and self.result.get('new_record', False):
            self.draw_text_center(
                'NOVO RECORDE!',
                24,
                COLOR_YELLOW,
                88
            )

        # Draw the top separator line.
        pygame.draw.line(
            self.window,
            COLOR_CYAN,
            (100, 125),
            (WIN_WIDTH - 100, 125),
            2
        )

        y = 150

        # Draw score information for 1P mode.
        if game_mode == MENU_OPTION[0]:
            self.draw_stat(
                'Pontuação Level',
                self.result['score'],
                y
            )

            y += 38

        # Draw score information for 2P mode.
        else:
            self.draw_stat(
                'Pontuação P1',
                self.result['score_p1'],
                y
            )

            y += 38

            self.draw_stat(
                'Pontuação P2',
                self.result['score_p2'],
                y
            )

            y += 38

            self.draw_stat(
                'Pontuação Level',
                self.result['score'],
                y
            )

            y += 38

        # Draw the accumulated campaign score.
        self.draw_stat(
            'Pontuação Total',
            self.result['total_score'],
            y
        )

        y += 38

        # Draw the best score only on the final stage.
        if is_final_stage:
            self.draw_stat(
                'Melhor Resultado',
                self.result['best_score'],
                y
            )

            y += 38

        y += 6

        # Draw enemy statistics.
        self.draw_stat(
            'Inimigos abatidos',
            self.result['enemies_destroyed'],
            y
        )

        y += 38

        self.draw_stat(
            'Sucesso inimigo',
            self.result['enemy_success'],
            y
        )

        y += 38

        # Draw missile defense statistics only on Level 3.
        if stage == 3:
            self.draw_stat(
                'Mísseis abatidos',
                self.result['missiles_destroyed'],
                y
            )

            y += 38

        # Draw launched missile statistics.
        self.draw_stat(
            'Mísseis lançados',
            self.result['missiles_launched'],
            y
        )

        # Draw the bottom separator line.
        pygame.draw.line(
            self.window,
            COLOR_CYAN,
            (100, 510),
            (WIN_WIDTH - 100, 510),
            2
        )

        # Show ENTER when the player can continue or retry.
        if not is_final_stage or self.result['status'] != 'win':
            self.draw_text_center(
                enter_text,
                22,
                COLOR_YELLOW,
                550
            )

            self.draw_text_center(
                '[R] VOLTAR AO MENU PRINCIPAL',
                21,
                COLOR_WHITE,
                600
            )

        # On final victory, only allow returning to the menu.
        else:
            self.draw_text_center(
                '[R] VOLTAR AO MENU PRINCIPAL',
                22,
                COLOR_WHITE,
                580
            )

    def draw_stat(self, label, value, y):  # Draws one statistic line.
        font = pygame.font.SysFont(
            'Arial',
            23,
            bold=True
        )

        # Render the statistic label.
        label_surface = font.render(
            f'{label}:',
            True,
            COLOR_WHITE
        )

        # Render the statistic value.
        value_surface = font.render(
            str(value),
            True,
            COLOR_YELLOW
        )

        # Draw the label on the left side.
        self.window.blit(
            label_surface,
            (80, y)
        )

        # Draw the value aligned to the right side.
        self.window.blit(
            value_surface,
            (WIN_WIDTH - value_surface.get_width() - 80, y)
        )

    def draw_text_center(self, text, size, color, y):  # Draws centered text.
        font = pygame.font.SysFont(
            'Arial',
            size,
            bold=True
        )

        surface = font.render(
            text,
            True,
            color
        )

        # Calculate the horizontal center position.
        x = (WIN_WIDTH - surface.get_width()) // 2

        self.window.blit(
            surface,
            (x, y)
        )