import pygame
from settings import (PLAYER_RADIUS, PLAYER_SPEED, PLAYER_MAX_HEALTH, 
                      INVINCIBLE_FRAMES, WORLD_HEIGHT, WORLD_WIDTH, GREEN)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.base_speed = PLAYER_SPEED
        self.damage = 1
        self.attack_speed = 5.0
        self.invincible_timer = 0
    
    @property
    def speed(self):
        return self.base_speed

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # 边界限制
        self.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.y))

    def take_damage(self, amount=1):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = INVINCIBLE_FRAMES
            return True
        return False

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw(self, surface, screen_x, screen_y):
        # 无敌闪烁
        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            color = (100, 255, 100)
        else:
            color = GREEN
        # pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), self.radius)