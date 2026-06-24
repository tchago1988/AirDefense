#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

WIN_WIDTH = 576
WINDOW_HEIGHT = 768

COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLACK = (0, 0, 0)

ENEMY_EVENT = pygame.USEREVENT + 1
SPAWN_TIME = 1200

ENTITY_SPEED = {
    'Player': 5,
    'Missile': 9,
    'Enemy1': 3,
    'Enemy2': 2,
}

ENTITY_HEALTH = {
    'Player': 100,
    'Missile': 1,
    'Enemy1': 1,
    'Enemy2': 5,
}

PLAYER_KEY_LEFT = pygame.K_LEFT
PLAYER_KEY_RIGHT = pygame.K_RIGHT
PLAYER_KEY_SHOOT = pygame.K_SPACE

BASE_HEALTH = 10
WIN_SCORE = 1500