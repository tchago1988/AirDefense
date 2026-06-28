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
        # Initialize Pygame modules.
        pygame.init()
        pygame.mixer.init()

        # Create the main game window.
        self.window = pygame.display.set_mode(
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

        # Set the game window title.
        pygame.display.set_caption('Air Defense')

        # Initialize the high score manager.
        self.score_manager = ScoreManager()

    def run(self):  # Main game loop.
        while True:
            # Display the main menu.
            menu = Menu(self.window)
            game_mode = menu.run()

            # Exit the game.
            if game_mode == 'EXIT':
                pygame.quit()
                sys.exit()

            # Start a new campaign from Level 1.
            stage_number = 1
            total_score = 0

            while True:
                # Create and run the current level.
                level = Level(
                    self.window,
                    game_mode,
                    stage_number
                )

                level_result = level.run()

                # Return to the main menu.
                if level_result == 'menu':
                    break

                # Exit the campaign loop if the level result is invalid.
                if not isinstance(level_result, dict):
                    break

                # Calculate the accumulated campaign score.
                previous_total = total_score
                attempt_total = previous_total + level_result['score']

                # Store the accumulated score in the result dictionary.
                level_result['total_score'] = attempt_total

                # Check whether another stage exists.
                has_next_stage = level.stage_manager.has_next_stage()
                is_final_stage = not has_next_stage

                # Store final stage and score information.
                level_result['is_final_stage'] = is_final_stage
                level_result['best_score'] = None
                level_result['new_record'] = False

                # Update the high score only after the final stage.
                if is_final_stage:
                    best_score_before = self.score_manager.load_best_score()

                    if attempt_total > best_score_before:
                        self.score_manager.save_best_score(attempt_total)

                        level_result['new_record'] = True
                        level_result['best_score'] = attempt_total

                    else:
                        level_result['best_score'] = best_score_before

                # Display the level result screen.
                result_screen = LevelResult(
                    self.window,
                    level_result,
                    has_next_stage
                )

                choice = result_screen.run()

                # Continue to the next stage.
                if choice == 'next':
                    if level_result['status'] == 'win':
                        # Save the accumulated score.
                        total_score = attempt_total

                        if has_next_stage:
                            stage_number = (
                                level.stage_manager.get_next_stage()
                            )

                        else:
                            # Campaign completed.
                            break

                    else:
                        # Stay on the current stage after failure.
                        stage_number = level.stage

                # Retry the current stage.
                elif choice == 'retry':
                    stage_number = level.stage

                # Return to the main menu.
                elif choice == 'menu':
                    break