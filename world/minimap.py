# ui/minimap.py
import pygame
from settings import MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_POS_X, MINIMAP_POS_Y

class MiniMap:
    def __init__(self, map_generator, camera, world_width, world_height):
        self.map_gen = map_generator
        self.camera = camera
        self.world_width = world_width
        self.world_height = world_height
        self.width = MINIMAP_WIDTH
        self.height = MINIMAP_HEIGHT
        self.surface = pygame.Surface((self.width, self.height))
        self.position = (MINIMAP_POS_X, MINIMAP_POS_Y)
        # 记录每个小地图像素是否已经被探索过
        self.explored_colors = [[None for _ in range(self.height)] for __ in range(self.width)]
        self.last_camera_rect = None

    def _world_to_minimap(self, world_x, world_y):
        """将世界坐标映射到小地图像素坐标"""
        px = int((world_x / self.world_width) * self.width)
        py = int((world_y / self.world_height) * self.height)
        return px, py

    def _update_pixel(self, px, py, color):
        """更新单个像素的颜色并绘制到表面"""
        if 0 <= px < self.width and 0 <= py < self.height:
            self.explored_colors[px][py] = color
            self.surface.set_at((px, py), color)

    def update(self):
        """根据当前相机视野，更新小地图上对应的像素"""
        camera_rect = self.camera.get_visible_rect()  # 返回世界矩形 (x,y,width,height)
        # 相机视野四个角在小地图上的像素范围
        left_top = self._world_to_minimap(camera_rect.left, camera_rect.top)
        right_bottom = self._world_to_minimap(camera_rect.right, camera_rect.bottom)
        # 限制 有效范围内
        min_px = max(0, left_top[0])
        max_px = min(self.width - 1, right_bottom[0])
        min_py = max(0, left_top[1])
        max_py = min(self.height - 1, right_bottom[1])

        # 遍历相机视野覆盖的小地图像素
        for px in range(min_px, max_px + 1):
            for py in range(min_py, max_py + 1):
                if self.explored_colors[px][py] is not None:
                    continue  # 已探索
                # 计算该像素对应的世界坐标中心
                world_x = (px + 0.5) / self.width * self.world_width
                world_y = (py + 0.5) / self.height * self.world_height
                color = self.map_gen.get_terrain_color(world_x, world_y)
                self._update_pixel(px, py, color)

    def draw(self, screen):
        self.update()
        # 绘制小地图背景
        screen.blit(self.surface, self.position)
        # 绘制玩家位置
        player_px, player_py = self._world_to_minimap(self.camera.target_x, self.camera.target_y)
        player_screen_x = self.position[0] + player_px
        player_screen_y = self.position[1] + player_py
        pygame.draw.circle(screen, (255, 255, 255), (player_screen_x, player_screen_y), 3)
        # 绘制边框
        pygame.draw.rect(screen, (200, 200, 200),
                         (self.position[0], self.position[1], self.width, self.height), 1)