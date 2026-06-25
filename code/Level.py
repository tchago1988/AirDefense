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
    COLOR_BLUE,
    ENEMY_EVENT,
    SPAWN_TIME,
    BASE_HEALTH,
    WIN_SCORE,
    PLAYER1_ROTATE_LEFT,
    PLAYER1_ROTATE_RIGHT,
    PLAYER1_SHOOT,
    PLAYER2_ROTATE_LEFT,
    PLAYER2_ROTATE_RIGHT,
    PLAYER2_SHOOT
)

from code.EntityFactory import EntityFactory
from code.Enemy import Enemy
from code.Missile import Missile
from code.Explosion import Explosion
from code.Player import Player


class Level:

    def __init__(self, window, game_mode):
        self.window = window
        self.game_mode = game_mode

        self.background_file = './asset/Background.png' \
            if game_mode == 1 \
            else './asset/Background1.png'

        self.background = pygame.image.load(self.background_file).convert()
        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WINDOW_HEIGHT)
        )

        self.players = []

        if self.game_mode == 1:
            self.players.append(
                Player(
                    (WIN_WIDTH // 2, 600),
                    PLAYER1_ROTATE_LEFT,
                    PLAYER1_ROTATE_RIGHT,
                    PLAYER1_SHOOT,
                    'P1'
                )
            )

        else:
            self.players.append(
                Player(
                    (190, 530),
                    PLAYER1_ROTATE_LEFT,
                    PLAYER1_ROTATE_RIGHT,
                    PLAYER1_SHOOT,
                    'P1'
                )
            )

            self.players.append(
                Player(
                    (391, 530),
                    PLAYER2_ROTATE_LEFT,
                    PLAYER2_ROTATE_RIGHT,
                    PLAYER2_SHOOT,
                    'P2'
                )
            )

        self.entity_list = []
        self.entity_list.extend(self.players)

        self.score = 0
        self.score_p1 = 0
        self.score_p2 = 0
        self.base_health = BASE_HEALTH

        self.game_over = False
        self.win = False

        self.shoot_sound = pygame.mixer.Sound('./asset/Shoot.wav')
        self.explosion_sound = pygame.mixer.Sound('./asset/Explosion.wav')

        self.shoot_sound.set_volume(0.15)
        self.explosion_sound.set_volume(0.80)

    def run(self):
        pygame.mixer.music.load('./asset/Level1.mp3')
        pygame.mixer.music.set_volume(0.20)
        pygame.mixer.music.play(-1)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return

            self.window.blit(self.background, (0, 0))

            if not self.game_over and not self.win:
                self.update_players()
                self.update_entities()
                self.check_collisions()
                self.check_game_state()

            else:
                self.draw_entities()

                keys = pygame.key.get_pressed()

                if keys[pygame.K_RETURN]:
                    pygame.mixer.music.stop()
                    return

            self.draw_hud()
            pygame.display.flip()

    def update_players(self):
        for player in self.players:
            player.move()

            missile = player.shoot()

            if missile:
                self.shoot_sound.play()
                self.entity_list.append(missile)

    def update_entities(self):
        for ent in self.entity_list:
            ent.move()
            self.window.blit(ent.surf, ent.rect)

    def draw_entities(self):
        for ent in self.entity_list:
            self.window.blit(ent.surf, ent.rect)

    def check_collisions(self):
        remove_list = []

        for ent in self.entity_list:

            if isinstance(ent, Missile):
                if (
                    ent.rect.bottom < 0
                    or ent.rect.right < 0
                    or ent.rect.left > WIN_WIDTH
                ):
                    remove_list.append(ent)

                for enemy in self.entity_list:

                    if isinstance(enemy, Enemy) and ent.rect.colliderect(enemy.rect):
                        remove_list.append(ent)
                        enemy.health -= 1

                        if enemy.health <= 0:
                            self.explosion_sound.play()

                            self.entity_list.append(
                                Explosion('Explosion', enemy.rect.center)
                            )

                            remove_list.append(enemy)

                            points = 250 if enemy.name == 'Enemy1' else 1000

                            self.score += points

                            if ent.owner == 'P1':
                                self.score_p1 += points

                            elif ent.owner == 'P2':
                                self.score_p2 += points

            if isinstance(ent, Enemy):
                if ent.rect.top > WINDOW_HEIGHT:
                    remove_list.append(ent)
                    self.base_health -= 1

            if isinstance(ent, Explosion):
                if ent.health <= 0:
                    remove_list.append(ent)

        for ent in remove_list:
            if ent in self.entity_list:
                self.entity_list.remove(ent)

    def check_game_state(self):
        if self.base_health <= 0:
            self.game_over = True
            pygame.mixer.music.stop()

        if self.score >= WIN_SCORE:
            self.win = True
            pygame.mixer.music.stop()

    def draw_hud(self):
        if self.game_mode == 1:
            self.draw_text(f'SCORE: {self.score}', (10, 10), COLOR_WHITE)
            self.draw_text(f'BASE: {self.base_health}', (10, 35), COLOR_WHITE)

        else:
            self.draw_text(f'P1: {self.score_p1}', (10, 10), COLOR_BLUE)
            self.draw_text(f'P2: {self.score_p2}', (10, 35), COLOR_RED)
            self.draw_text(f'BASE: {self.base_health}', (10, 60), COLOR_WHITE)

        if self.win:
            self.draw_text('MISSAO CUMPRIDA!', (145, WINDOW_HEIGHT // 2), COLOR_GREEN)
            self.draw_text('ENTER - MENU', (190, WINDOW_HEIGHT // 2 + 40), COLOR_WHITE)

        if self.game_over:
            self.draw_text('BASE DESTRUIDA!', (145, WINDOW_HEIGHT // 2), COLOR_RED)
            self.draw_text('ENTER - MENU', (190, WINDOW_HEIGHT // 2 + 40), COLOR_WHITE)

    def draw_text(self, text, pos, color):
        font = pygame.font.SysFont('Arial', 22, bold=True)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)