#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

WIN_WIDTH = 576
WINDOW_HEIGHT = 680
FPS = 60

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 128, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_CYAN = (0, 255, 255)

MENU_OPTION = (
    'PLAYER 1P',
    'PLAYER 2P - COOPERATIVE',
    'EXIT',
)

ENEMY_EVENT = pygame.USEREVENT + 1

BASE_HEALTH = 10
DIR_CENTER = 2

MISSILE_ANGLES = {
    0: 135,
    1: 115,
    2: 90,
    3: 65,
    4: 45,
}

STAGES = {
    1: {
        'name': 'Level1',
        'backgrounds': ('Background',),
        'music': 'Level1.mp3',
        'duration': 20000,
        'spawn_time': 1400,
        'enemy_types': ('Enemy1',),
        'next_stage': 2,
    },

    2: {
        'name': 'Level2',
        'backgrounds': ('Background2',),
        'music': 'Level2.mp3',
        'duration': 30000,
        'spawn_time': 1000,
        'enemy_types': ('Enemy1', 'Enemy2'),
        'next_stage': 3,
    },

    3: {
        'name': 'Level3',
        'backgrounds': ('Background3',),
        'music': 'Level3.mp3',
        'duration': 40000,
        'spawn_time': 900,
        'enemy_types': ('Enemy1', 'Enemy2'),
        'next_stage': None,
    },
}

ENTITY_SPEED = {
    'Background': 0,
    'Background1': 0,
    'Background2': 0,
    'Background3': 0,

    'Player1': 0,
    'Player2': 0,

    'Missile': 5,
    'EnemyMissile': 2.5,

    'Enemy1': 1,
    'Enemy2': 1.5,

    'Explosion': 0,
}

ENTITY_HEALTH = {
    'Background': 999,
    'Background1': 999,
    'Background2': 999,
    'Background3': 999,

    'Player1': 300,
    'Player2': 300,

    'Missile': 1,
    'EnemyMissile': 1,

    'Enemy1': 50,
    'Enemy2': 80,

    'Explosion': 1,
}

ENTITY_DAMAGE = {
    'Missile': 50,
    'EnemyMissile': 1,

    'Enemy1': 30,
    'Enemy2': 45,

    'Player1': 1,
    'Player2': 1,
}

ENTITY_SCORE = {
    'Enemy1': 100,
    'Enemy2': 200,
}

ENTITY_SHOT_DELAY = {
    'Player1': 15,
    'Player2': 15,
}

PLAYER_KEY_LEFT = {
    'Player1': pygame.K_LEFT,
    'Player2': pygame.K_a,
}

PLAYER_KEY_RIGHT = {
    'Player1': pygame.K_RIGHT,
    'Player2': pygame.K_d,
}

PLAYER_KEY_SHOOT = {
    'Player1': pygame.K_m,
    'Player2': pygame.K_SPACE,
}

PLAYER_KEY_UP = {}
PLAYER_KEY_DOWN = {}

ASSET_PATH = './asset/'