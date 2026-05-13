import opensimplex
import random
import hashlib
import pygame
from settings import (TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, 
                      TERRAIN_NOISE_SCALE, TERRAIN_NOISE_SCALE_TWO,
                      TERRAIN_TEXTURES, WORLD_WIDTH_TILES, WORLD_HEIGHT_TILES)
from entities.decoration import Decoration

class TerrainType:
    RAINFOREST = 0
    DESERT = 1
    FOREST = 2
    GRASS = 3
    TUNDRA = 4
    ICE = 5

    COLORS = {
        RAINFOREST: (0, 100, 0),
        DESERT: (255, 255, 0),
        FOREST: (0, 128, 0),
        GRASS: (85, 107, 47),
        TUNDRA: (169, 169, 169),
        ICE: (173, 216, 230)
    }


class MapGenerator:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randint(0, 10000)
        opensimplex.seed(self.seed)
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.scale = TERRAIN_NOISE_SCALE
        self.scale_2 = TERRAIN_NOISE_SCALE_TWO
        self.textures = self._load_textures()
        self.deco_textures = self._load_deco_textures()
        self.decoration_objects = []
        self.tiles = {}
    
    def _load_textures(self):
        """加载场景的贴图"""
        textures = {}
        for name, path in TERRAIN_TEXTURES.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                if img.get_width() != TILE_SIZE or img.get_height() != TILE_SIZE:
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                textures[name] = img
            except (pygame.error, FileNotFoundError):
                print(f"无场景贴图 {path}")
                fallback = pygame.Surface((TILE_SIZE, TILE_SIZE))
                terrain_type = self._get_terrain_type_from_name(name)
                fallback.fill(TerrainType.COLORS.get(terrain_type, (255, 0, 255)))
                textures[name] = fallback
        return textures
    
    def _load_deco_textures(self):
        """加载装饰物贴图"""
        from settings import DECORATION_TEXTURES
        deco_textures = {}
        for biome, texture_paths in DECORATION_TEXTURES.items():
            deco_textures[biome] = []
            for path in texture_paths:
                try:
                    img = pygame.image.load(path).convert_alpha()
                    target_size = (TILE_SIZE, TILE_SIZE)
                    if img.get_size() != target_size:
                        img = pygame.transform.scale(img, target_size)
                    deco_textures[biome].append(img)
                except FileNotFoundError:
                    print(f"无装饰物贴图 {path}")
        return deco_textures
    
    def _get_terrain_type_from_name(self, name):
        """根据生物群落名称返回对应的代号"""
        mapping = {
            "rainforest": TerrainType.RAINFOREST,
            "desert": TerrainType.DESERT,
            "forest": TerrainType.FOREST,
            "grass": TerrainType.GRASS,
            "tundra": TerrainType.TUNDRA,
            "ice": TerrainType.ICE,
        }
        return mapping.get(name, TerrainType.GRASS)
    
    def _get_biome_name_from_terrain(self, terrain_type):
        """根据代号返回群落名称"""
        mapping = {
            TerrainType.RAINFOREST: "rainforest",
            TerrainType.DESERT: "desert",
            TerrainType.FOREST: "forest",
            TerrainType.GRASS: "grass",
            TerrainType.TUNDRA: "tundra",
            TerrainType.ICE: "ice",
        }
        return mapping.get(terrain_type, "grass")

    def get_terrain_at(self, world_x, world_y):
        """根据世界坐标获取地形类型"""
        # 计算噪声坐标
        nx = world_x * self.scale
        ny = world_y * self.scale
        # 使用Perlin 噪声
        temp = opensimplex.noise2(nx, ny) # 温度
        humid = opensimplex.noise2(world_x * self.scale_2, world_y * self.scale_2 + 100) # 湿度
        if temp > 0.4:
            if humid > 0.4:
                return TerrainType.RAINFOREST       # 雨林
            else:
                return TerrainType.DESERT      # 沙漠
        elif temp > -0.4:
            if humid > 0:
                return TerrainType.FOREST        # 森林
            else:
                return TerrainType.GRASS      # 草原
        else:  # temp <= -0.2
            if humid > 0:
                return TerrainType.TUNDRA    # 苔原
            else:
                return TerrainType.ICE   # 冰川
            
    def get_biome(self, world_x, world_y):
        """返回生物群落的字符串名称"""
        terrain = self.get_terrain_at(world_x, world_y)
        # 定义映射关系
        biome_map = {
            TerrainType.RAINFOREST: "rainforest",
            TerrainType.DESERT: "desert",
            TerrainType.FOREST: "forest",
            TerrainType.GRASS: "grass",
            TerrainType.TUNDRA: "tundra",
            TerrainType.ICE: "ice",
        }
        return biome_map.get(terrain, "grass")

    """        
    def get_decoration(self, world_x, world_y):
        # 获取生物群落名称
        biome = self.get_biome(world_x, world_y)
        density = DECORATION_DENSITY.get(biome, 0.1)

        # 基于瓦片坐标和种子生成 0-1 之间的伪随机值
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        seed_hash = int(hashlib.md5(f"{tile_x},{tile_y},{self.seed}".encode()).hexdigest(), 16)
        rand_val = (seed_hash % 1000) / 1000.0   # 0.000 ~ 0.999

        return rand_val < density
    """

    def get_tile(self, tile_x, tile_y):
        """获取指定瓦片坐标的地形"""
        key = (tile_x, tile_y)
        if key not in self.tiles:
            # 计算瓦片中心的世界坐标
            world_center_x = (tile_x + 0.5) * TILE_SIZE
            world_center_y = (tile_y + 0.5) * TILE_SIZE
            terrain = self.get_terrain_at(world_center_x, world_center_y)
            self.tiles[key] = terrain
        return self.tiles[key]

    def draw_tile(self, surface, tile_x, tile_y, screen_rect):
        """绘制单个瓦片"""
        world_left = tile_x * TILE_SIZE
        world_top = tile_y * TILE_SIZE
        tile_rect = pygame.Rect(world_left, world_top, TILE_SIZE, TILE_SIZE)
        """
        if tile_rect.colliderect(screen_rect):
            terrain = self.get_tile(tile_x, tile_y)
            color = TerrainType.COLORS[terrain]
            # 将世界坐标转换为屏幕坐标
            screen_x = tile_rect.x - screen_rect.x
            screen_y = tile_rect.y - screen_rect.y
            pygame.draw.rect(surface, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        """
        if not tile_rect.colliderect(screen_rect):
            return

        screen_x = tile_rect.x - screen_rect.x
        screen_y = tile_rect.y - screen_rect.y

        terrain = self.get_tile(tile_x, tile_y)
        biome_name = self._get_biome_name_from_terrain(terrain)
        tex = self.textures.get(biome_name)
        if tex:
            dest_pos = (tile_rect.x - screen_rect.x, tile_rect.y - screen_rect.y)
            surface.blit(tex, dest_pos)
        else:
            color = TerrainType.COLORS.get(terrain, (255, 0, 255))
            pygame.draw.rect(surface, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

    
    def generate_full_map(self):
        self.tile_grid = [[None for _ in range(WORLD_HEIGHT_TILES)] for __ in range(WORLD_WIDTH_TILES)]
        self.decoration_objects = []
        deco_density = {
            TerrainType.RAINFOREST: 0.4,
            TerrainType.FOREST: 0.3,
            TerrainType.GRASS: 0.2,
            TerrainType.DESERT: 0.15,
            TerrainType.TUNDRA: 0.1,
            TerrainType.ICE: 0.05,
        }
        biome_drops = {
            "rainforest": ("wood", 5),
            "forest":    ("wood", 4),
            "grass":     ("herb", 2),
            "desert":    ("cactus", 3),
            "tundra":    ("stone", 3),
            "ice":       ("crystal", 2),
        }
        for tx in range(WORLD_WIDTH_TILES):
            for ty in range(WORLD_HEIGHT_TILES):
                world_x = (tx + 0.5) * TILE_SIZE
                world_y = (ty + 0.5) * TILE_SIZE
                terrain = self.get_terrain_at(world_x, world_y)
                self.tile_grid[tx][ty] = terrain
                # 装饰物生成
                density = deco_density.get(terrain, 0.1)
                hash_val = (tx * 73856093) ^ (ty * 19349663) ^ self.seed
                rand_val = (hash_val & 0xFFFF) / 65536.0
                if rand_val < density:
                    biome_name = self._get_biome_name_from_terrain(terrain)
                    deco_list = self.deco_textures.get(biome_name, [])
                    if deco_list:
                        idx = (tx * 131071 + ty * 524287) % len(deco_list)
                        img = deco_list[idx]
                        drop_item, drop_amount = biome_drops.get(biome_name, ("material", 1))
                        deco = Decoration(world_x, world_y, biome_name, img, drop_item, drop_amount)
                        self.decoration_objects.append(deco)

    def get_terrain_color(self, world_x, world_y):
        """返回地形对应的 RGB 颜色"""
        terrain = self.get_terrain_at(world_x, world_y)
        return TerrainType.COLORS[terrain]
    
    def generate_terrain_grid(self, grid_width, grid_height):
        """预先生成一个低分辨率的地形网格"""
        self.terrain_grid = [[None for _ in range(grid_height)] for __ in range(grid_width)]
        step_x = self.world_width / grid_width
        step_y = self.world_height / grid_height
        for gx in range(grid_width):
            for gy in range(grid_height):
                world_x = gx * step_x + step_x/2
                world_y = gy * step_y + step_y/2
                color = self.get_terrain_color(world_x, world_y)
                self.terrain_grid[gx][gy] = color
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_step_x = step_x
        self.grid_step_y = step_y

    def get_terrain_color_from_grid(self, world_x, world_y):
        """从预生成网格中获取颜色"""
        gx = int(world_x / self.grid_step_x)
        gy = int(world_y / self.grid_step_y)
        gx = max(0, min(gx, self.grid_width-1))
        gy = max(0, min(gy, self.grid_height-1))
        return self.terrain_grid[gx][gy]
    
    