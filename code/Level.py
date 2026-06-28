#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import pygame
from code.Cons import (WIN_WIDTH, WINDOW_HEIGHT, FPS, COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_RED, COLOR_BLUE,
                       ENEMY_EVENT, MENU_OPTION, ENTITY_SCORE, )
from code.StageManager import StageManager
from code.EntityFactory import EntityFactory
from code.Enemy import Enemy
from code.Missile import Missile
from code.EnemyMissile import EnemyMissile
from code.Explosion import Explosion

class Level:
    def __init__(self, window, game_mode, stage_number=1): # Main game window where everything is drawn.
        self.window = window
        # Selected game mode from the menu.
        self.game_mode = game_mode
        self.stage_manager = StageManager(stage_number)
        self.stage = self.stage_manager.get_stage_number()
        self.entity_list = []  # General entity list used for updating and drawing.
        # Separate lists for better organization.
        self.players = []
        self.backgrounds = []
        # General score values.
        self.score = 0
        self.score_p1 = 0
        self.score_p2 = 0
        # Gameplay statistics.
        self.enemies_destroyed = 0
        self.enemy_success = 0
        self.missiles_destroyed = 0
        self.missiles_launched = 0
        self.base_health = self.stage_manager.get_base_health(self.game_mode)
        # Game state flags.
        self.game_over = False
        self.win = False
        self.paused = False
        # Load initial stage objects.
        self.load_backgrounds()
        self.load_players()
        # Add backgrounds and players to the main entity list.
        self.entity_list.extend(self.backgrounds)
        self.entity_list.extend(self.players)
        # Configure audio channels.
        pygame.mixer.set_num_channels(16)
        # Load sound effects.
        self.shoot_sound = pygame.mixer.Sound('./asset/Shoot.wav')
        self.explosion_sound = pygame.mixer.Sound('./asset/Explosion.wav')
        # Set sound volumes.
        self.shoot_sound.set_volume(0.15)
        self.explosion_sound.set_volume(0.80)
        # Channels used for shooting sounds.
        self.shoot_channels = [
            pygame.mixer.Channel(1),
            pygame.mixer.Channel(2),
            pygame.mixer.Channel(3),
            pygame.mixer.Channel(4),]
        # Channels used for explosion sounds.
        self.explosion_channels = [
            pygame.mixer.Channel(5),
            pygame.mixer.Channel(6),
            pygame.mixer.Channel(7),
            pygame.mixer.Channel(8),
            pygame.mixer.Channel(9),
            pygame.mixer.Channel(10), ]
        # Indexes used to rotate between sound channels.
        self.current_shoot_channel = 0
        self.current_explosion_channel = 0

    def play_shoot_sound(self):  # Plays the shooting sound using rotating audio channels.
        channel = self.shoot_channels[self.current_shoot_channel]
        channel.play(self.shoot_sound)
        self.current_shoot_channel += 1
        if self.current_shoot_channel >= len(self.shoot_channels):
            self.current_shoot_channel = 0

    def play_explosion_sound(self):  # Plays the explosion sound using rotating audio channels.
        channel = self.explosion_channels[self.current_explosion_channel]
        channel.play(self.explosion_sound)
        self.current_explosion_channel += 1
        if self.current_explosion_channel >= len(self.explosion_channels):
            self.current_explosion_channel = 0

    def load_backgrounds(self):  # Loads all background layers for the current stage.
        for bg_name in self.stage_manager.get_backgrounds():
            bg_list = EntityFactory.get_entity(bg_name)
            if bg_list:
                self.backgrounds.extend(bg_list)

    def load_players(self):  # Loads player objects according to the selected game mode.
        if self.game_mode == MENU_OPTION[0]:
            # Player1 mode.
            player = EntityFactory.get_entity('Player1')
            player.rect.centerx = WIN_WIDTH // 2
            player.rect.bottom = WINDOW_HEIGHT - 95
            self.players.append(player)
        else:
            # Player2 mode.
            # Player2 starts on the left side.
            player2 = EntityFactory.get_entity('Player2')
            player2.rect.center = (int(WIN_WIDTH * 0.30), WINDOW_HEIGHT - 130)
            # Player1 starts on the right side.
            player1 = EntityFactory.get_entity('Player1')
            player1.rect.center = (int(WIN_WIDTH * 0.70), WINDOW_HEIGHT - 130)
            self.players.append(player2)
            self.players.append(player1)

    def run(self):  # Main stage loop.
        self.stage_manager.play_music()
        pygame.mixer.music.set_volume(0.20)
        # Start enemy spawn timer.
        pygame.time.set_timer(
            ENEMY_EVENT,
            self.stage_manager.get_spawn_time())
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # ESC returns to the menu.
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return 'menu'
                    # P pauses or resumes the game.
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                # Enemy spawn event.
                if (event.type == ENEMY_EVENT
                        and not self.game_over
                        and not self.win
                        and not self.paused):
                    enemy_name = random.choice(
                        self.stage_manager.get_enemy_types())
                    enemy = EntityFactory.get_entity(enemy_name)
                    if enemy:
                        self.entity_list.append(enemy)
            # If the game is paused, only draw the pause screen.
            if self.paused:
                self.draw_entities()
                self.draw_hud()
                self.draw_pause()
                pygame.display.flip()
                continue
            # Normal gameplay update.
            if not self.game_over and not self.win:
                self.update_players()
                self.update_entities()
                self.check_collisions()
                self.check_game_state()
            else:
                # After win or game over, wait for ENTER.
                self.draw_entities()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    pygame.mixer.music.stop()
                    if self.win:
                        return self.get_level_result('win')
                    return self.get_level_result('game_over')
            self.draw_hud()
            pygame.display.flip()

    def toggle_pause(self):  # Pauses or resumes the game.
        self.paused = not self.paused
        if self.paused:
            self.stage_manager.pause_timer()
            pygame.mixer.music.pause()
            pygame.time.set_timer(ENEMY_EVENT, 0)
        else:
            self.stage_manager.resume_timer()
            pygame.mixer.music.unpause()
            pygame.time.set_timer(
                ENEMY_EVENT,
                self.stage_manager.get_spawn_time())

    def update_players(self):  # Updates player movement and shooting.
        for player in self.players:
            player.move()
            missile = player.shoot()
            if missile:
                self.play_shoot_sound()
                self.entity_list.append(missile)
                self.missiles_launched += 1

    def update_entities(self):  # Updates and draws all entities.
        for ent in self.entity_list[:]:
            ent.move()
            self.window.blit(ent.surf, ent.rect)
            # Stage 3 enemy missile attack.
            if self.stage == 3 and isinstance(ent, Enemy):
                if ent.rect.centery <= WINDOW_HEIGHT // 2:
                    target_player = random.choice(self.players)
                    enemy_missile = ent.shoot(target_player.rect.center)
                    if enemy_missile:
                        self.entity_list.append(enemy_missile)

    def draw_entities(self):  # Draws all current entities on the screen.
        for ent in self.entity_list:
            self.window.blit(ent.surf, ent.rect)

    def check_collisions(self):  # Checks all gameplay collisions and removes invalid entities.
        remove_list = []
        for ent in self.entity_list:
            # Player missile logic.
            if isinstance(ent, Missile):
                # Remove player missiles that leave the screen.
                if (ent.rect.bottom < 0
                        or ent.rect.right < 0
                        or ent.rect.left > WIN_WIDTH):
                    remove_list.append(ent)
                # Player missile hitting enemies.
                for enemy in self.entity_list:
                    if isinstance(enemy, Enemy):
                        if ent.rect.colliderect(enemy.rect):
                            remove_list.append(ent)
                            enemy.health -= ent.damage
                            if enemy.health <= 0:
                                self.play_explosion_sound()
                                self.entity_list.append(
                                    Explosion('Explosion', enemy.rect.center))
                                remove_list.append(enemy)
                                self.enemies_destroyed += 1
                                points = ENTITY_SCORE[enemy.name]
                                self.score += points
                                if ent.owner == 'Player1':
                                    self.score_p1 += points
                                elif ent.owner == 'Player2':
                                    self.score_p2 += points
                # Player missile hitting enemy missile.
                for enemy_missile in self.entity_list:
                    if isinstance(enemy_missile, EnemyMissile):
                        if ent.rect.colliderect(enemy_missile.rect):
                            remove_list.append(ent)
                            remove_list.append(enemy_missile)
                            self.missiles_destroyed += 1
                            self.play_explosion_sound()
                            self.entity_list.append(
                                Explosion('Explosion', enemy_missile.rect.center))
            # Enemy missile logic.
            if isinstance(ent, EnemyMissile):
                # Remove enemy missiles that leave the screen.
                if (ent.rect.top > WINDOW_HEIGHT
                        or ent.rect.bottom < 0
                        or ent.rect.right < 0
                        or ent.rect.left > WIN_WIDTH):
                    remove_list.append(ent)
                # Enemy missile hitting a player.
                for player in self.players:
                    if ent.rect.colliderect(player.rect):
                        remove_list.append(ent)
                        # In this version, enemy missiles damage the base.
                        self.base_health -= ent.damage
            # Enemy crossing the bottom of the screen.
            if isinstance(ent, Enemy):
                if ent.rect.top > WINDOW_HEIGHT:
                    remove_list.append(ent)
                    # Every enemy that passes reduces base health.
                    self.base_health -= 1
                    self.enemy_success += 1
            # Remove finished explosion animations.
            if isinstance(ent, Explosion):
                if ent.health <= 0:
                    remove_list.append(ent)
        # Remove entities safely after collision checks.
        for ent in remove_list:
            if ent in self.entity_list:
                self.entity_list.remove(ent)

    def check_game_state(self):  # Checks if the player has won or lost the stage.
        if self.base_health <= 0:
            self.game_over = True
            pygame.mixer.music.stop()
            pygame.time.set_timer(ENEMY_EVENT, 0)
        if self.stage_manager.is_stage_finished():
            # Victory only happens if the base is alive
            # and no enemy has passed through the defense.
            if self.base_health > 0 and self.enemy_success == 0:
                self.win = True
            else:
                self.game_over = True
            pygame.mixer.music.stop()
            pygame.time.set_timer(ENEMY_EVENT, 0)

    def get_level_result(self, status):  # Returns the final result dictionary for the current level.
        return {
            'status': status,
            'stage': self.stage,
            'background': self.stage_manager.get_backgrounds()[0],
            'game_mode': self.game_mode,
            'score': self.score,
            'score_p1': self.score_p1,
            'score_p2': self.score_p2,
            'enemies_destroyed': self.enemies_destroyed,
            'enemy_success': self.enemy_success,
            'missiles_destroyed': self.missiles_destroyed,
            'missiles_launched': self.missiles_launched}

    def draw_hud(self): #Draws level information on the screen.
        self.draw_text(f'LEVEL: {self.stage}', (10, 10), COLOR_YELLOW)
        if self.game_mode == MENU_OPTION[0]:
            # Player1 HUD.
            self.draw_text(f'SCORE: {self.score}', (10, 35), COLOR_WHITE)
            self.draw_text(f'BASE: {self.base_health}', (10, 60), COLOR_WHITE)
        else:
            # Player2 HUD.
            self.draw_text(f'P1: {self.score_p1}', (10, 35), COLOR_BLUE)
            self.draw_text(f'P2: {self.score_p2}', (10, 60), COLOR_RED)
            self.draw_text(f'BASE: {self.base_health}', (10, 85), COLOR_WHITE)
        self.draw_text(
            f'TIME: {self.stage_manager.get_remaining_time()}',
            (WIN_WIDTH - 120, 10),
            COLOR_WHITE)
        self.draw_text(
            'P - PAUSE',
            (WIN_WIDTH - 120, 35),
            COLOR_YELLOW)
        self.draw_controls()
        if self.win:
            self.draw_text_center(
                'MISSION ACCOMPLISHED!',
                WINDOW_HEIGHT // 2,
                COLOR_GREEN)
            self.draw_text_center(
                'ENTER - RESULT',
                WINDOW_HEIGHT // 2 + 35,
                COLOR_WHITE)
        if self.game_over:
            self.draw_text_center(
                'BASE DESTROYED!',
                WINDOW_HEIGHT // 2,
                COLOR_RED)
            self.draw_text_center(
                'ENTER - RESULT',
                WINDOW_HEIGHT // 2 + 35,
                COLOR_WHITE)

    def draw_controls(self): #Draws control instructions according to the selected game mode.
        if self.game_mode == MENU_OPTION[0]:
            self.draw_text_center_small(
                'CONTROLS:  ← → MOVE   |   M SHOOT   |   P PAUSE',
                WINDOW_HEIGHT - 28,
                COLOR_WHITE)
        else:
            self.draw_control_box_p2_left()
            self.draw_control_box_p1_right()

    def draw_control_box_p2_left(self): #Draws Player 2 control instructions on the left side.
        box_width = 190
        box_height = 70
        box_x = 10
        box_y = WINDOW_HEIGHT - 85
        box = pygame.Surface((box_width, box_height))
        box.set_alpha(120)
        box.fill((0, 0, 0))
        self.window.blit(box, (box_x, box_y))
        self.draw_text_small('P2', (box_x + 20, box_y + 7), COLOR_RED)
        self.draw_text_small('A D MOVE', (box_x + 20, box_y + 30), COLOR_WHITE)
        self.draw_text_small('SPACE SHOOT', (box_x + 20, box_y + 53), COLOR_YELLOW)

    def draw_control_box_p1_right(self): #Draws Player 1 control instructions on the right side.
        box_width = 180
        box_height = 70
        box_x = WIN_WIDTH - box_width - 10
        box_y = WINDOW_HEIGHT - 85
        box = pygame.Surface((box_width, box_height))
        box.set_alpha(120)
        box.fill((0, 0, 0))
        self.window.blit(box, (box_x, box_y))
        self.draw_text_small('P1', (box_x + 20, box_y + 7), COLOR_BLUE)
        self.draw_text_small('← → MOVE', (box_x + 20, box_y + 30), COLOR_WHITE)
        self.draw_text_small('M SHOOT', (box_x + 20, box_y + 53), COLOR_YELLOW)

    def draw_pause(self): #Draws the pause overlay.
        overlay = pygame.Surface((WIN_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))
        self.draw_text_center(
            'PAUSE',
            WINDOW_HEIGHT // 2 - 40,
            COLOR_YELLOW)
        self.draw_text_center(
            'PRESS P TO CONTINUE',
            WINDOW_HEIGHT // 2 + 10,
            COLOR_WHITE)
        self.draw_text_center(
            'ESC - BACK TO MENU',
            WINDOW_HEIGHT // 2 + 55,
            COLOR_RED)

    def draw_text(self, text, pos, color): #Draws normal-sized text.
        font = pygame.font.SysFont('Arial', 22, bold=True)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)

    def draw_text_small(self, text, pos, color):  #Draws small text.
        font = pygame.font.SysFont('Arial', 16, bold=True)
        surf = font.render(text, True, color)
        self.window.blit(surf, pos)

    def draw_text_center(self, text, y, color): #Draws centered normal-sized text.
        font = pygame.font.SysFont('Arial', 26, bold=True)
        surf = font.render(text, True, color)
        x = (WIN_WIDTH - surf.get_width()) // 2
        self.window.blit(surf, (x, y))

    def draw_text_center_small(self, text, y, color): #Draws centered small text.
        font = pygame.font.SysFont('Arial', 17, bold=True)
        surf = font.render(text, True, color)
        x = (WIN_WIDTH - surf.get_width()) // 2
        self.window.blit(surf, (x, y))
