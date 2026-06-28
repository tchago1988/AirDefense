#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import pygame
from code.Cons import ENTITY_SPEED, ENTITY_DAMAGE, ENTITY_HEALTH


class EnemyMissile:  # Define the missile properties.
    def __init__(self, position: tuple, target_position: tuple):
        self.name = 'EnemyMissile'
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.speed = ENTITY_SPEED[self.name]
        # Load and scale the missile sprite.
        self.surf = pygame.image.load('./asset/Missile.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (22, 44))
        # Calculate the direction vector toward the target.
        dx = target_position[0] - position[0]
        dy = target_position[1] - position[1]
        # Calculate the distance to the target.
        distance = math.hypot(dx, dy)
        # Prevent division by zero.
        if distance == 0: distance = 1
        # Calculate the movement speed on each axis.
        self.x_speed = (dx / distance) * self.speed
        self.y_speed = (dy / distance) * self.speed
        # Calculate the missile rotation angle.
        angle = math.degrees(math.atan2(-dy, dx))
        # Rotate the sprite toward the target.
        self.surf = pygame.transform.rotate(self.surf, angle - 90)
        # Create the collision rectangle.
        self.rect = self.surf.get_rect(center=position)
        # Store the position as floating-point values for smooth movement.
        self.x_float = float(self.rect.centerx)
        self.y_float = float(self.rect.centery)

    def move(self):  # Moves the missile toward the target.
        # Update the floating-point position.
        self.x_float += self.x_speed
        self.y_float += self.y_speed
        # Update the rectangle position.
        self.rect.centerx = int(self.x_float)
        self.rect.centery = int(self.y_float)
