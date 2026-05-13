import pygame
import math
from settings import WEAPON_RADIUS, WEAPON_DAMAGE, WEAPON_KNOCKBACK, WEAPON_ROTATION_SPEED

class Weapon:
    def __init__(self, player, offset_angle):
        self.player = player
        self.angle = offset_angle  # 当前角度（弧度）
        self.radius = WEAPON_RADIUS
        # self.damage = WEAPON_DAMAGE
        self.knockback = WEAPON_KNOCKBACK
    
    @property
    def damage(self):
        return self.player.damage
    
    @property
    def rotation_speed(self):
        return self.player.attack_speed

    def update(self, dt):
        """更新武器位置"""
        self.angle += WEAPON_ROTATION_SPEED * dt
        # print(f"角度: {self.angle}, 转速: {self.rotation_speed}, dt: {dt}")
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def get_position(self):
        """计算武器在世界坐标系中的位置"""
        x = self.player.x + math.cos(self.angle) * (self.player.radius + self.radius + 5)
        y = self.player.y + math.sin(self.angle) * (self.player.radius + self.radius + 5)
        return x, y

    def draw(self, surface, screen_x, screen_y):
        # x, y = self.get_position()
        x = screen_x
        y = screen_y
        pygame.draw.circle(surface, (200, 200, 0), (int(x), int(y)), self.radius)
        # 绘制一个小剑
        end_x = x + math.cos(self.angle) * self.radius * 1.5
        end_y = y + math.sin(self.angle) * self.radius * 1.5
        pygame.draw.line(surface, (255, 255, 0), (int(x), int(y)), (int(end_x), int(end_y)), 3)