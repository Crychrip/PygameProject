import pygame
from settings import PLAYER_SPEED

class InputManager:
    @staticmethod
    def get_movement():
        """返回移动方向"""
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        return dx, dy