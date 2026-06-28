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
        self.window = window
        self.result = result
        self.has_next_stage = has_next_stage

        background_name = self.result['background']

        self.background = pygame.image.load(
            f'{ASSET_PATH}{background_name}.png'
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

        self.panel = pygame.Surface((WIN_WIDTH - 80, WINDOW_HEIGHT - 80))
        self.panel.set_alpha(185)

        if self.result['status'] == 'win':
            self.panel.fill((0, 20, 10))
        else:
            self.panel.fill((25, 0, 0))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)

            self.window.blit(self.background, (0, 0))
            self.window.blit(self.panel, (40, 40))

            self.draw_screen()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        if not self.result.get('is_final_stage', False):
                            if self.result['status'] == 'win':
                                return 'next'
                            return 'retry'

                    elif event.key == pygame.K_r:
                        return 'menu'

    def draw_screen(self):
        stage = self.result['stage']
        is_final_stage = self.result.get('is_final_stage', False)
        game_mode = self.result.get('game_mode')

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

        self.draw_text_center(title, 38, title_color, 45)

        if is_final_stage and self.result.get('new_record', False):
            self.draw_text_center(
                'NOVO RECORDE!',
                24,
                COLOR_YELLOW,
                88
            )

        pygame.draw.line(
            self.window,
            COLOR_CYAN,
            (100, 125),
            (WIN_WIDTH - 100, 125),
            2
        )

        y = 150

        if game_mode == MENU_OPTION[0]:
            self.draw_stat('Pontuação Level', self.result['score'], y)
            y += 38

        else:
            self.draw_stat('Pontuação P1', self.result['score_p1'], y)
            y += 38

            self.draw_stat('Pontuação P2', self.result['score_p2'], y)
            y += 38

            self.draw_stat('Pontuação Level', self.result['score'], y)
            y += 38

        self.draw_stat('Pontuação Total', self.result['total_score'], y)
        y += 38

        if is_final_stage:
            self.draw_stat('Melhor Resultado', self.result['best_score'], y)
            y += 38

        y += 6

        self.draw_stat('Inimigos abatidos', self.result['enemies_destroyed'], y)
        y += 38

        self.draw_stat('Sucesso inimigo', self.result['enemy_success'], y)
        y += 38

        if stage == 3:
            self.draw_stat('Mísseis abatidos', self.result['missiles_destroyed'], y)
            y += 38

        self.draw_stat('Mísseis lançados', self.result['missiles_launched'], y)

        pygame.draw.line(
            self.window,
            COLOR_CYAN,
            (100, 510),
            (WIN_WIDTH - 100, 510),
            2
        )

        if not is_final_stage:
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

        else:
            self.draw_text_center(
                '[R] VOLTAR AO MENU PRINCIPAL',
                22,
                COLOR_WHITE,
                580
            )

    def draw_stat(self, label, value, y):
        font = pygame.font.SysFont('Arial', 23, bold=True)

        label_surface = font.render(
            f'{label}:',
            True,
            COLOR_WHITE
        )

        value_surface = font.render(
            str(value),
            True,
            COLOR_YELLOW
        )

        self.window.blit(label_surface, (80, y))

        self.window.blit(
            value_surface,
            (WIN_WIDTH - value_surface.get_width() - 80, y)
        )

    def draw_text_center(self, text, size, color, y):
        font = pygame.font.SysFont('Arial', size, bold=True)
        surface = font.render(text, True, color)

        x = (WIN_WIDTH - surface.get_width()) // 2
        self.window.blit(surface, (x, y))