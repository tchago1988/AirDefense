#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

# A
# Main asset folder path.
ASSET_PATH = './asset/'

# B
# Basic colors used in the game.
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_ORANGE = (255, 128, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)

# C
# Default cannon direction.
DIR_CENTER = 2

# D
# Damage value for each entity.
ENTITY_DAMAGE = {
    'Enemy1': 30,
    'Enemy2': 45,
    'EnemyMissile': 1,
    'Missile': 50,
    'Player1': 1,
    'Player2': 1,
}

# E
# Health value for each entity.
ENTITY_HEALTH = {
    'Background': 999,
    'Background1': 999,
    'Background2': 999,
    'Background3': 999,
    'Enemy1': 50,
    'Enemy2': 70,
    'EnemyMissile': 1,
    'Explosion': 1,
    'Missile': 1,
    'Player1': 300,
    'Player2': 300, }

# Score value awarded for destroying enemies.
ENTITY_SCORE = {
    'Enemy1': 100,
    'Enemy2': 200,
}

# Shooting delay for each player.
ENTITY_SHOT_DELAY = {
    'Player1': 15,
    'Player2': 15,
}

# Movement speed for each entity.
ENTITY_SPEED = {
    'Background': 0,
    'Background1': 0,
    'Background2': 0,
    'Background3': 0,
    'Enemy1': 1,
    'Enemy2': 1.5,
    'EnemyMissile': 2,
    'Explosion': 0,
    'Missile': 5,
    'Player1': 0,
    'Player2': 0, }

# Custom event used to spawn enemies.
ENEMY_EVENT = pygame.USEREVENT + 1

# F
# Game frame rate.
FPS = 60

# M
# Main menu options.
MENU_OPTION = (
    'PLAYER 1P',
    'PLAYER 2P - COOPERATIVE',
    'EXIT',)

# Missile angle for each cannon direction.
MISSILE_ANGLES = {
    0: 135,
    1: 115,
    2: 90,
    3: 65,
    4: 45, }

# P
# Key mapping for rotating left.
PLAYER_KEY_LEFT = {
    'Player1': pygame.K_LEFT,
    'Player2': pygame.K_a, }

# Empty movement mappings kept for compatibility with older classes.
PLAYER_KEY_DOWN = {}

# Key mapping for rotating right.
PLAYER_KEY_RIGHT = {
    'Player1': pygame.K_RIGHT,
    'Player2': pygame.K_d, }

# Key mapping for shooting.
PLAYER_KEY_SHOOT = {
    'Player1': pygame.K_m,
    'Player2': pygame.K_SPACE, }

# Empty movement mappings kept for compatibility with older classes.
PLAYER_KEY_UP = {}

# S
# Stage configuration.
STAGES = {
    1: {
        'name': 'Level1',
        'backgrounds': ('Background',),
        'music': 'Level1.mp3',
        'duration': 20000,
        'spawn_time': 1100,
        'enemy_types': ('Enemy1',),
        'base_health_1p': 3,
        'base_health_2p': 5,
        'next_stage': 2, },

    2: {
        'name': 'Level2',
        'backgrounds': ('Background2',),
        'music': 'Level2.mp3',
        'duration': 30000,
        'spawn_time': 950,
        'enemy_types': ('Enemy1', 'Enemy2'),
        'base_health_1p': 4,
        'base_health_2p': 6,
        'next_stage': 3, },

    3: {
        'name': 'Level3',
        'backgrounds': ('Background3',),
        'music': 'Level3.mp3',
        'duration': 35000,
        'spawn_time': 1300,
        'enemy_types': ('Enemy1', 'Enemy2'),
        'base_health_1p': 10,
        'base_health_2p': 15,
        'next_stage': None, },
}

# W
# Window size.
WIN_WIDTH = 576
WINDOW_HEIGHT = 680
