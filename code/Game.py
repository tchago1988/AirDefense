#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame

from code.Cons import WIN_WIDTH, WINDOW_HEIGHT
from code.Menu import Menu
from code.Level import Level
from code.LevelResult import LevelResult
from code.ScoreManager import ScoreManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIN_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Coastal Air Defense')

        self.score_manager = ScoreManager()

    def run(self):
        while True:
            menu = Menu(self.window)
            game_mode = menu.run()

            if game_mode == 'EXIT':
                pygame.quit()
                sys.exit()

            stage_number = 1
            total_score = 0

            while True:
                level = Level(self.window, game_mode, stage_number)
                level_result = level.run()

                if level_result == 'menu':
                    break

                if isinstance(level_result, dict):
                    previous_total = total_score
                    attempt_total = previous_total + level_result['score']

                    level_result['total_score'] = attempt_total

                    has_next_stage = level.stage_manager.has_next_stage()
                    is_final_stage = not has_next_stage

                    level_result['is_final_stage'] = is_final_stage
                    level_result['best_score'] = None
                    level_result['new_record'] = False

                    if is_final_stage:
                        best_score_before = self.score_manager.load_best_score()

                        if attempt_total > best_score_before:
                            self.score_manager.save_best_score(attempt_total)
                            level_result['new_record'] = True
                            level_result['best_score'] = attempt_total
                        else:
                            level_result['best_score'] = best_score_before

                    result_screen = LevelResult(
                        self.window,
                        level_result,
                        has_next_stage
                    )

                    choice = result_screen.run()

                    if choice == 'next':
                        if level_result['status'] == 'win':
                            total_score = attempt_total

                            if has_next_stage:
                                stage_number = level.stage_manager.get_next_stage()
                            else:
                                break
                        else:
                            stage_number = level.stage

                    elif choice == 'retry':
                        stage_number = level.stage

                    elif choice == 'menu':
                        break

                else:
                    break