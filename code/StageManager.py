#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.Cons import STAGES, ASSET_PATH, MENU_OPTION


class StageManager:
    def __init__(self, stage_number=1):
        self.stage_number = stage_number
        self.stage_data = STAGES[self.stage_number]

        self.start_time = pygame.time.get_ticks()
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.paused = False

    def get_stage_number(self):
        return self.stage_number

    def get_stage_name(self):
        return self.stage_data['name']

    def get_backgrounds(self):
        return self.stage_data['backgrounds']

    def get_music(self):
        return self.stage_data['music']

    def get_duration(self):
        return self.stage_data['duration']

    def get_spawn_time(self):
        return self.stage_data['spawn_time']

    def get_enemy_types(self):
        return self.stage_data['enemy_types']

    def get_next_stage(self):
        return self.stage_data['next_stage']

    def get_base_health(self, game_mode):
        if game_mode == MENU_OPTION[0]:
            return self.stage_data['base_health_1p']

        return self.stage_data['base_health_2p']

    def play_music(self):
        pygame.mixer_music.load(f"{ASSET_PATH}{self.get_music()}")
        pygame.mixer_music.play(-1)

    def pause_timer(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()

    def resume_timer(self):
        if self.paused:
            pause_end_time = pygame.time.get_ticks()
            self.total_pause_time += pause_end_time - self.pause_start_time
            self.pause_start_time = 0
            self.paused = False

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()

        if self.paused:
            return self.pause_start_time - self.start_time - self.total_pause_time

        return current_time - self.start_time - self.total_pause_time

    def is_stage_finished(self):
        return self.get_elapsed_time() >= self.get_duration()

    def has_next_stage(self):
        return self.get_next_stage() is not None

    def next_stage(self):
        if self.has_next_stage():
            self.stage_number = self.get_next_stage()
            self.stage_data = STAGES[self.stage_number]

            self.start_time = pygame.time.get_ticks()
            self.pause_start_time = 0
            self.total_pause_time = 0
            self.paused = False

            self.play_music()
            return True

        return False

    def get_remaining_time(self):
        remaining_time = self.get_duration() - self.get_elapsed_time()
        return max(0, remaining_time // 1000)