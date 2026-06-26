#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import pygame
from code.Cons import (WIN_WIDTH, WINDOW_HEIGHT, FPS, COLOR_WHITE, COLOR_YELLOW,
                       COLOR_GREEN, COLOR_RED, COLOR_BLUE, ENEMY_EVENT, MENU_OPTION, BASE_HEALTH, ENTITY_SCORE, )
from code.StageManager import StageManager
from code.EntityFactory import EntityFactory
from code.Enemy import Enemy
from code.Missile import Missile
from code.EnemyMissile import EnemyMissile
from code.Explosion import Explosion


class Level:
    def __init__(self, window, game_mode, stage_number=1):
        self.window = window
        self.game_mode = game_mode
        self.stage_manager = StageManager(stage_number)
        self.stage = self.stage_manager.get_stage_number()
        self.entity_list = []
        self.players = []
        self.backgrounds = []
        self.score = 0
        self.score_p1 = 0
        self.score_p2 = 0
        self.base_health = BASE_HEALTH
        self.game_over = False
        self.win = False
        self.load_backgrounds()
        self.load_players()
        self.entity_list.extend(self.backgrounds)
        self.entity_list.extend(self.players)
        self.shoot_sound = pygame.mixer.Sound('./asset/Shoot.wav')
        self.explosion_sound = pygame.mixer.Sound('./asset/Explosion.wav')
        self.shoot_sound.set_volume(0.15)
        self.explosion_sound.set_volume(0.80)

    def load_backgrounds(self):
        for bg_name in self.stage_manager.get_backgrounds():
            bg_list = EntityFactory.get_entity(bg_name)
            if bg_list:
                self.backgrounds.extend(bg_list)

    def load_players(self):
        if self.game_mode == MENU_OPTION[0]:
            player = EntityFactory.get_entity('Player1')
            player.rect.centerx = WIN_WIDTH // 2
            player.rect.bottom = WINDOW_HEIGHT - 95
            self.players.append(player)

        else:
            player2 = EntityFactory.get_entity('Player2')
            player2.rect.center = (int(WIN_WIDTH * 0.30),WINDOW_HEIGHT - 150)
            player1 = EntityFactory.get_entity('Player1')
            player1.rect.center = (int(WIN_WIDTH * 0.70),WINDOW_HEIGHT - 150)
            self.players.append(player2)
            self.players.append(player1)

    def run(self):
        self.stage_manager.play_music()
        pygame.mixer.music.set_volume(0.20)
        pygame.time.set_timer(ENEMY_EVENT,self.stage_manager.get_spawn_time())
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return 'menu'

                if event.type == ENEMY_EVENT and not self.game_over and not self.win:
                    enemy_name = random.choice(self.stage_manager.get_enemy_types())
                    enemy = EntityFactory.get_entity(enemy_name)
                    if enemy:
                        self.entity_list.append(enemy)

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
                    if self.win:
                        return 'win'
                    return 'menu'

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
        for ent in self.entity_list[:]:
            ent.move()
            self.window.blit(ent.surf, ent.rect)

            # LEVEL 3:
            # os aviões só lançam mísseis da parte de cima até o meio da tela
            if self.stage == 3 and isinstance(ent, Enemy):
                if ent.rect.centery <= WINDOW_HEIGHT // 2:
                    target_player = random.choice(self.players)

                    enemy_missile = ent.shoot(target_player.rect.center)

                    if enemy_missile:
                        self.entity_list.append(enemy_missile)

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

                # Míssil do player acerta inimigo
                for enemy in self.entity_list:
                    if isinstance(enemy, Enemy):
                        if ent.rect.colliderect(enemy.rect):
                            remove_list.append(ent)
                            enemy.health -= ent.damage

                            if enemy.health <= 0:
                                self.explosion_sound.play()

                                self.entity_list.append(
                                    Explosion('Explosion', enemy.rect.center)
                                )

                                remove_list.append(enemy)

                                points = ENTITY_SCORE[enemy.name]
                                self.score += points

                                if ent.owner == 'Player1':
                                    self.score_p1 += points

                                elif ent.owner == 'Player2':
                                    self.score_p2 += points

                # Míssil do player abate míssil inimigo
                for enemy_missile in self.entity_list:
                    if isinstance(enemy_missile, EnemyMissile):
                        if ent.rect.colliderect(enemy_missile.rect):
                            remove_list.append(ent)
                            remove_list.append(enemy_missile)

                            self.explosion_sound.play()

                            self.entity_list.append(
                                Explosion('Explosion', enemy_missile.rect.center)
                            )

            if isinstance(ent, EnemyMissile):
                if (
                        ent.rect.top > WINDOW_HEIGHT
                        or ent.rect.bottom < 0
                        or ent.rect.right < 0
                        or ent.rect.left > WIN_WIDTH
                ):
                    remove_list.append(ent)

                for player in self.players:
                    if ent.rect.colliderect(player.rect):
                        remove_list.append(ent)
                        self.base_health -= ent.damage

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

        if self.stage_manager.is_stage_finished():
            self.win = True
            pygame.mixer.music.stop()

    def draw_hud(self):
        self.draw_text(f'LEVEL: {self.stage}', (10, 10), COLOR_YELLOW)

        if self.game_mode == MENU_OPTION[0]:
            self.draw_text(f'SCORE: {self.score}', (10, 35), COLOR_WHITE)
            self.draw_text(f'BASE: {self.base_health}', (10, 60), COLOR_WHITE)

        else:
            self.draw_text(f'P1: {self.score_p1}', (10, 35), COLOR_BLUE)
            self.draw_text(f'P2: {self.score_p2}', (10, 60), COLOR_RED)
            self.draw_text(f'BASE: {self.base_health}', (10, 85), COLOR_WHITE)

        self.draw_text(
            f'TIME: {self.stage_manager.get_remaining_time()}',
            (WIN_WIDTH - 120, 10),
            COLOR_WHITE
        )

        if self.win:
            self.draw_text_center('MISSAO CUMPRIDA!', WINDOW_HEIGHT // 2, COLOR_GREEN)
            self.draw_text_center('ENTER - CONTINUAR', WINDOW_HEIGHT // 2 + 35, COLOR_WHITE)

        if self.game_over:
            self.draw_text_center('BASE DESTRUIDA!', WINDOW_HEIGHT // 2, COLOR_RED)
            self.draw_text_center('ENTER - MENU', WINDOW_HEIGHT // 2 + 35, COLOR_WHITE)

    def draw_text(self, text, pos, color):
        font = pygame.font.SysFont('Arial', 22, bold=True)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)

    def draw_text_center(self, text, y, color):
        font = pygame.font.SysFont('Arial', 26, bold=True)
        surf = font.render(text, True, color)
        x = (WIN_WIDTH - surf.get_width()) // 2
        self.window.blit(surf, (x, y))
