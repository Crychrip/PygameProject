import pygame
import math
from settings import EXPERIENCE_RADIUS

class ExperienceOrb:
    def __init__(self, x, y, value=10):
        self.x = x
        self.y = y
        self.radius = EXPERIENCE_RADIUS
        self.value = value

    def draw(self, surface, screen_x, screen_y):
        # pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (0, 255, 255), (int(screen_x), int(screen_y)), self.radius)

    def attracted_update(self, target_x, target_y, speed, dt):
        """判断是否应被拾取"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 5:
            return True
        if dist > 0:
            move = min(speed * dt, dist - 5)
            self.x += (dx / dist) * move
            self.y += (dy / dist) * move
        return False