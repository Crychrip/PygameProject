# 合成配方：产物ID -> 详细信息
RECIPES = {
    "wooden_plank": {
        "name": "木板",
        "category": "material",          # 材料类
        "materials": {"wood": 2, "scrap": 1},
        "result_amount": 1,
        "description": "2木材 + 1废料 → 木板"
    },
    "stone_block": {
        "name": "石砖",
        "category": "material",
        "materials": {"stone": 3},
        "result_amount": 1,
        "description": "3石头 → 石砖"
    },
    "iron_pickaxe": {
        "name": "铁镐",
        "category": "tool",              # 工具类
        "materials": {"scrap": 5, "wood": 2},
        "result_amount": 1,
        "description": "5废料 + 2木材 → 铁镐 (开采装备)"
    },
    "health_potion": {
        "name": "生命药水",
        "category": "consumable",        # 消耗品类
        "materials": {"herb": 2, "scrap": 1},
        "result_amount": 1,
        "description": "2草药 + 1废料 → 生命药水"
    },
}

# 类别
CATEGORY_NAMES = {
    "material": "材料",
    "tool": "工具",
    "consumable": "消耗品",
    "equipment": "装备"
}

# 类别排序
CATEGORY_ORDER = ["material", "tool", "consumable", "equipment"]

# 装备
EQUIPMENTS = {
    "iron_pickaxe": {
        "name": "铁镐",
        "type": "harvest",          # 开采类
        "effect": {"harvest_bonus": 2},
        "description": "开采材料数量+2"
    },
    "health_potion": {
        "name": "生命药水",
        "type": "consumable",       # 消耗品
        "effect": {"heal": 20},
        "description": "恢复20生命"
    },
}