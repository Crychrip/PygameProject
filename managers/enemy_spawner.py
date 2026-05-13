import pygame
import random
import math
from settings import ENEMY_SPAWN_DELAY
from entities.enemy import Enemy
from settings import (ENEMY_SPAWN_DELAY, ENEMY_SPAWN_RADIUS_MIN, 
                      ENEMY_SPAWN_RADIUS_MAX)

class EnemySpawner:
    def __init__(self):
        self.last_spawn_time = pygame.time.get_ticks()

    def update(self, enemies_list, player_x, player_y, world_width, world_height):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > ENEMY_SPAWN_DELAY:
            # 以玩家为中心，在环形区域内随机生成敌人
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(ENEMY_SPAWN_RADIUS_MIN, ENEMY_SPAWN_RADIUS_MAX)
            x = player_x + math.cos(angle) * radius
            y = player_y + math.sin(angle) * radius
            # 确保生成位置不超出世界边界
            margin = 50
            x = max(margin, min(world_width - margin, x))
            y = max(margin, min(world_height - margin, y))
            enemies_list.append(Enemy(x, y))
            self.last_spawn_time = now