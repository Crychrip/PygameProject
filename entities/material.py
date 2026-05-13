import pygame
import math
from settings import MATERIAL_RADIUS

class Material:
    def __init__(self, x, y, item_id, amount=1, value=5):
        self.x = x
        self.y = y
        self.radius = MATERIAL_RADIUS
        self.item_id = item_id
        self.amount = amount
        self.value = value

    def draw(self, surface, screen_x, screen_y):
        # pygame.draw.circle(surface, (255, 215, 0), (int(self.x), int(self.y)), self.radius)  # 金色
        pygame.draw.circle(surface, (255, 215, 0), (int(screen_x), int(screen_y)), self.radius)

    def attracted_update(self, target_x, target_y, speed, dt):
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