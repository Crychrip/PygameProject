import pygame

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.width = width          # 屏幕宽度
        self.height = height        # 屏幕高度
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0

    def update(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        # 相机跟随玩家 且将玩家置于屏幕中心
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2
        # 边界限制
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))

    def apply(self, world_x, world_y):
        """将世界坐标转换为屏幕坐标"""
        return world_x - self.x, world_y - self.y

    def get_visible_rect(self):
        """返回当前相机可见的世界矩形区域"""
        return pygame.Rect(self.x, self.y, self.width, self.height)