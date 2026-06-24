#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

# =========================
# WINDOW
# =========================

WIN_WIDTH = 576
WINDOW_HEIGHT = 768

# =========================
# COLORS
# =========================

COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLACK = (0, 0, 0)

# =========================
# EVENTS
# =========================

ENEMY_EVENT = pygame.USEREVENT + 1
SPAWN_TIME = 1200

# =========================
# SPEEDS
# =========================

ENTITY_SPEED = {
    'Player': 5,
    'Missile': 10,
    'Enemy1': 3,
    'Enemy2': 2,
}

# =========================
# HEALTH
# =========================

ENTITY_HEALTH = {
    'Player': 100,
    'Missile': 1,
    'Enemy1': 1,
    'Enemy2': 5,
}

# =========================
# GAME RULES
# =========================

BASE_HEALTH = 10
WIN_SCORE = 1500

# =========================
# TURRET DIRECTIONS
# =========================

DIR_LEFT = 0
DIR_CENTER_LEFT = 1
DIR_CENTER = 2
DIR_CENTER_RIGHT = 3
DIR_RIGHT = 4

# =========================
# MISSILE TRAJECTORIES
# =========================
# (x_speed, y_speed)
#
# Mais reto para frente,
# acompanhando a direção da torre.

MISSILE_ANGLES = {
    DIR_LEFT: (-7, -8),
    DIR_CENTER_LEFT: (-4, -9),
    DIR_CENTER: (0, -10),
    DIR_CENTER_RIGHT: (4, -9),
    DIR_RIGHT: (7, -8),
}

# =========================
# CONTROLS
# =========================

PLAYER_KEY_ROTATE_LEFT = pygame.K_a
PLAYER_KEY_ROTATE_RIGHT = pygame.K_d
PLAYER_KEY_SHOOT = pygame.K_SPACE