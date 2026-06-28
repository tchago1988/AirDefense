#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import pygame
from code.Cons import ENTITY_HEALTH


class Entity(ABC):  # Store the entity name.
    def __init__(self, name: str, position: tuple):
        self.name = name
        # Load the entity sprite.
        self.surf = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        # Create the collision rectangle.
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        # Set the initial health value.
        self.health = ENTITY_HEALTH[self.name]

    @abstractmethod
    def move(self):  # Defines the movement behavior for derived classes.
        pass
