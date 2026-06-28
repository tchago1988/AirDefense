#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import pygame
from code.Entity import Entity
from code.Cons import ENTITY_SPEED, ENTITY_DAMAGE


class Missile(Entity):
    def __init__(self, name: str, position: tuple, angle_degrees: int, owner: str):
        super().__init__(name, position)
        # Store the missile owner.
        self.owner = owner
        # Set the missile speed and damage.
        self.speed = ENTITY_SPEED[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        # Store the firing angle.
        self.angle_degrees = angle_degrees
        # Scale the missile sprite.
        self.surf = pygame.transform.scale(self.surf, (28, 56))
        # Rotate the sprite according to the firing angle.
        self.surf = pygame.transform.rotate(self.surf, self.angle_degrees - 90)
        # Create the collision rectangle.
        self.rect = self.surf.get_rect(center=position)
        # Convert the angle to radians.
        angle_radians = math.radians(self.angle_degrees)
        # Calculate the movement speed on each axis.
        self.x_speed = math.cos(angle_radians) * self.speed
        self.y_speed = -math.sin(angle_radians) * self.speed
        # Store the position as floating-point values for smooth movement.
        self.x_float = float(self.rect.centerx)
        self.y_float = float(self.rect.centery)

    def move(self):  # Moves the missile according to its trajectory.
        # Update the floating-point position.
        self.x_float += self.x_speed
        self.y_float += self.y_speed
        # Update the rectangle position.
        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)
