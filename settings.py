# settings.py
import pygame

# 窗口设置
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# 颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 地图设置
TILE_SIZE = 64                    # 每个地形瓦片的像素大小
WORLD_WIDTH_TILES = 200           # 世界宽度瓦片数 (200*50=10000)
WORLD_HEIGHT_TILES = 200          # 世界高度瓦片数
WORLD_WIDTH = WORLD_WIDTH_TILES * TILE_SIZE
WORLD_HEIGHT = WORLD_HEIGHT_TILES * TILE_SIZE

TERRAIN_TEXTURES = {
    "rainforest": "assets/textures/rainforest.png",
    "desert": "assets/textures/desert.png",
    "forest": "assets/textures/forest.png",
    "grass": "assets/textures/grass.png",
    "tundra": "assets/textures/tundra.png",
    "ice": "assets/textures/ice.png",
}

# 地形生成参数
TERRAIN_NOISE_SCALE = 0.0003
TERRAIN_NOISE_SCALE_TWO = 0.0002
TERRAIN_NOISE_OCTAVES = 4
TERRAIN_NOISE_PERSISTENCE = 0.5
TERRAIN_NOISE_LACUNARITY = 2.0

# 小地图设置
MINIMAP_WIDTH = 120               # 宽度像素
MINIMAP_HEIGHT = 120              # 高度像素
MINIMAP_POS_X = 10
MINIMAP_POS_Y = SCREEN_HEIGHT - MINIMAP_HEIGHT - 10
MINIMAP_RADIUS = 1500
MINIMAP_UPDATE_INTERVAL = 0.2

# 装饰物
DECORATION_TEXTURES = {
    "rainforest": ["assets/decorations/tree_01.png"],
    "forest": ["assets/decorations/tree_02.png"],
    "grass": ["assets/decorations/flower_01.png"],
    "desert": ["assets/decorations/cactus.png"],
    "tundra": ["assets/decorations/rock_01.png"],
    "ice": ["assets/decorations/ice_crystal.png"],
}

MATERIAL_NAMES = {
    "wood": "木材",
    "stone": "石头",
    "scrap": "废旧零件",
    "herb": "草药",
    "crystal": "水晶",
    "cactus": "仙人掌",
    "wooden_plank": "木板",
    "stone_block": "石砖",
    "iron_pickaxe": "铁镐",
    "health_potion": "生命药水",
}

# 玩家设置
PLAYER_RADIUS = 15
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 3
INVINCIBLE_FRAMES = 30   # 无敌帧数

# 敌人设置
ENEMY_RADIUS = 12
ENEMY_SPEED = 2
ENEMY_SPAWN_DELAY = 1000  # 毫秒
ENEMY_SPAWN_RADIUS_MIN = 400   # 距离玩家最小距离（像素）
ENEMY_SPAWN_RADIUS_MAX = 800   # 距离玩家最大距离（像素）

# 武器设置
WEAPON_RADIUS = 8
WEAPON_DAMAGE = 1
WEAPON_KNOCKBACK = 3.0        # 击退力度
WEAPON_ROTATION_SPEED = 5.0    # 弧度/秒（约 300 度/秒）
WEAPON_COUNT = 1               # 武器数量（后续可升级）

# 经验设置
EXPERIENCE_RADIUS = 6
EXPERIENCE_ATTRACT_RADIUS = 100
EXPERIENCE_ATTRACT_SPEED = 300
BASE_EXPERIENCE_TO_LEVEL = 100
EXPERIENCE_SCALING = 1.2

# 升级选项库
UPGRADE_OPTIONS = [
    {"name": "攻击力 +1", "stat": "damage", "value": 1},
    {"name": "攻击速度 +0.5", "stat": "attack_speed", "value": 0.5},
    {"name": "移动速度 +0.5", "stat": "speed", "value": 0.5},
    {"name": "最大生命 +1", "stat": "max_health", "value": 1},
    {"name": "生命恢复 +1", "stat": "health_regen", "value": 1},
]

# 材料系统
MATERIAL_RADIUS = 8
MATERIAL_ATTRACT_RADIUS = 120
MATERIAL_ATTRACT_SPEED = 300
MATERIAL_DROP_VALUE = 5  # 每个敌人掉落材料数量

# 建筑升级配置
BUILDING_PRICES = {
    "铁匠铺": [50, 150, 300],   # 等级0->1, 1->2, 2->3 所需材料
    "训练场": [30, 100, 200],
    "魔法塔": [40, 120, 250],
    "仓库": [20, 80, 160]
}
BUILDING_EFFECTS = {
    "铁匠铺": {"stat": "damage", "value": 1},
    "训练场": {"stat": "max_health", "value": 10},
    "魔法塔": {"stat": "attack_speed", "value": 0.5},
    "仓库": {"stat": "speed", "value": 0.5}
}

# 游戏设置
FPS = 60