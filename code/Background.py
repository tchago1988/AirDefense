#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.Entity import Entity
from code.Cons import WIN_WIDTH, WINDOW_HEIGHT


class Background(Entity):  # Initialize the base entity.
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Scale the background to fill the game window.
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WINDOW_HEIGHT))
        # Position the background at the top-left corner.
        self.rect = self.surf.get_rect(left=0, top=0)

    def move(self):  # Background remains static during gameplay.
        pass
