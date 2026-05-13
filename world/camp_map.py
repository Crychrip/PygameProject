import pygame
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

# 营地地图尺寸
CAMP_WIDTH_TILES = 50
CAMP_HEIGHT_TILES = 50
CAMP_WIDTH = CAMP_WIDTH_TILES * TILE_SIZE
CAMP_HEIGHT = CAMP_HEIGHT_TILES * TILE_SIZE

# 建筑位置
BUILDINGS_POS = {
    "铁匠铺": (CAMP_WIDTH // 2 - 100, CAMP_HEIGHT // 2 - 50),
    "训练场": (CAMP_WIDTH // 2 + 100, CAMP_HEIGHT // 2 - 50),
    "魔法塔": (CAMP_WIDTH // 2 - 100, CAMP_HEIGHT // 2 + 50),
    "仓库": (CAMP_WIDTH // 2 + 100, CAMP_HEIGHT // 2 + 50),
}

WORKBENCH_POS = {
    "工作台": ((CAMP_WIDTH // 2, CAMP_HEIGHT // 2))
}

class CampMap:
    def __init__(self):
        self.width = CAMP_WIDTH
        self.height = CAMP_HEIGHT
        self.background_color = (34, 139, 34)

    def draw(self, surface, camera):
        surface.fill(self.background_color)
        font = pygame.font.SysFont('simhei', 16)

        # 绘制建筑
        for name, pos in BUILDINGS_POS.items():
            screen_x, screen_y = camera.apply(pos[0], pos[1])
            pygame.draw.circle(surface, (255, 255, 0), (int(screen_x), int(screen_y)), 20)
            text = font.render(name, True, (255,255,255))
            surface.blit(text, (screen_x - text.get_width()//2, screen_y - 30))
        
        # 绘制工作台
        for name, pos in WORKBENCH_POS.items():
            wx, wy = pos[0], pos[1]
            screen_x, screen_y = camera.apply(wx, wy)
            pygame.draw.circle(surface, (200, 100, 50), (int(screen_x), int(screen_y)), 20)
            text = font.render("工作台", True, (255,255,255))
            surface.blit(text, (screen_x - 20, screen_y - 30))