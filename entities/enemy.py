import pygame
import math
from settings import WORLD_WIDTH, WORLD_HEIGHT, ENEMY_RADIUS, ENEMY_SPEED, RED

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = ENEMY_RADIUS
        self.health = 1
        self.dead = False
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.dead = True

    def update(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += (dx / dist) * ENEMY_SPEED
            self.y += (dy / dist) * ENEMY_SPEED

    def draw(self, surface, screen_x, screen_y):
        # pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, RED, (int(screen_x), int(screen_y)), self.radius)

    def is_off_screen(self, margin=500):
        """判断是否远离屏幕"""
        return (self.x < -margin or self.x > WORLD_WIDTH + margin or
                self.y < -margin or self.y > WORLD_HEIGHT + margin)