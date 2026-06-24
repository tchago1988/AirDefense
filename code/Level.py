#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import pygame

from code.Cons import (
    WIN_WIDTH,
    WINDOW_HEIGHT,
    COLOR_WHITE,
    COLOR_GREEN,
    COLOR_RED,
    ENEMY_EVENT,
    SPAWN_TIME,
    BASE_HEALTH,
    WIN_SCORE
)

from code.EntityFactory import EntityFactory
from code.Enemy import Enemy
from code.Missile import Missile


class Level:

    def __init__(self, window):
        self.window = window

        self.background = pygame.image.load('./asset/Background.png').convert()
        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

        self.player = EntityFactory.get_entity('Player')
        self.entity_list = [self.player]

        self.score = 0
        self.base_health = BASE_HEALTH
        self.game_over = False
        self.win = False

    def run(self):
        pygame.time.set_timer(ENEMY_EVENT, SPAWN_TIME)

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == ENEMY_EVENT and not self.game_over and not self.win:
                    if random.randint(0, 10) < 8:
                        self.entity_list.append(EntityFactory.get_entity('Enemy1'))
                    else:
                        self.entity_list.append(EntityFactory.get_entity('Enemy2'))

            self.window.blit(self.background, (0, 0))

            if not self.game_over and not self.win:
                self.player.move()

                missile = self.player.shoot()
                if missile:
                    self.entity_list.append(missile)

                for ent in self.entity_list:
                    ent.move()
                    self.window.blit(ent.surf, ent.rect)

                self.check_collisions()
                self.check_game_state()

            else:
                for ent in self.entity_list:
                    self.window.blit(ent.surf, ent.rect)

            self.draw_hud()

            pygame.display.flip()

    def check_collisions(self):
        remove_list = []

        for ent in self.entity_list:
            if isinstance(ent, Missile):
                if ent.rect.bottom < 0:
                    remove_list.append(ent)

                for enemy in self.entity_list:
                    if isinstance(enemy, Enemy):
                        if ent.rect.colliderect(enemy.rect):
                            remove_list.append(ent)
                            enemy.health -= 1

                            if enemy.health <= 0:
                                remove_list.append(enemy)

                                if enemy.name == 'Enemy1':
                                    self.score += 100
                                elif enemy.name == 'Enemy2':
                                    self.score += 500

            if isinstance(ent, Enemy):
                if ent.rect.top > WINDOW_HEIGHT:
                    remove_list.append(ent)
                    self.base_health -= 1

        for ent in remove_list:
            if ent in self.entity_list:
                self.entity_list.remove(ent)

    def check_game_state(self):
        if self.base_health <= 0:
            self.game_over = True

        if self.score >= WIN_SCORE:
            self.win = True

    def draw_hud(self):
        self.draw_text(f'SCORE: {self.score}', (10, 10), COLOR_WHITE)
        self.draw_text(f'BASE: {self.base_health}', (10, 35), COLOR_WHITE)

        if self.win:
            self.draw_text('MISSAO CUMPRIDA!', (150, WINDOW_HEIGHT // 2), COLOR_GREEN)

        if self.game_over:
            self.draw_text('BASE DESTRUIDA!', (150, WINDOW_HEIGHT // 2), COLOR_RED)

    def draw_text(self, text, pos, color):
        font = pygame.font.SysFont('Arial', 22)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)