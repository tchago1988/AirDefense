#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.Entity import Entity


class Explosion(Entity):  # Initialize the base entity.
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Scale the explosion sprite.
        self.surf = pygame.transform.scale(self.surf, (80, 80))
        # Position the explosion at the specified location.
        self.rect = self.surf.get_rect(center=position)
        # Define the explosion lifetime in frames.
        self.life_time = 20

    def move(self):  # Updates the explosion animation.
        # Decrease the remaining lifetime.
        self.life_time -= 1
        # Remove the explosion when its lifetime expires.
        if self.life_time <= 0:
            self.health = 0
