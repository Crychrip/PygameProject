import math
from settings import MATERIAL_ATTRACT_RADIUS, MATERIAL_ATTRACT_SPEED
from entities.material import Material

class MaterialManager:
    def __init__(self):
        self.materials = []
        self.inventory = {}

    def add_material(self, x, y, item_id, amount):
        self.materials.append(Material(x, y, item_id, amount))
        self.inventory[item_id] = self.inventory.get(item_id, 0) + amount
        # self.total_value += amount

    def update(self, player_x, player_y, dt):
        """更新材料球吸引，并处理拾取"""
        collected = {}   # 本次拾取的材料
        for mat in self.materials[:]:
            dx = player_x - mat.x
            dy = player_y - mat.y
            dist = math.hypot(dx, dy)
            if dist < MATERIAL_ATTRACT_RADIUS:
                if mat.attracted_update(player_x, player_y, MATERIAL_ATTRACT_SPEED, dt):
                    self.materials.remove(mat)
                    collected[mat.item_id] = collected.get(mat.item_id, 0) + mat.amount
        # 将拾取的材料累加到 inventory
        for item_id, total in collected.items():
            self.inventory[item_id] = self.inventory.get(item_id, 0) + total
        return collected

    def draw(self, surface, camera):
        for mat in self.materials:
            screen_x, screen_y = camera.apply(mat.x, mat.y)
            mat.draw(surface, screen_x, screen_y)

    def clear(self):
        self.materials.clear()
        self.inventory.clear()

    def get_inventory(self):
        return self.inventory

    def get_material(self, item_id):
        return self.inventory.get(item_id, 0)

    def set_inventory(self, inventory):
        self.inventory = inventory.copy()

    def to_dict(self):
        return self.inventory

    def from_dict(self, data):
        self.inventory = data.copy()
    
    def deduct_material(self, item_id, amount):
        """从库存中扣除指定材料"""
        if self.inventory.get(item_id, 0) >= amount:
            self.inventory[item_id] -= amount
            if self.inventory[item_id] == 0:
                del self.inventory[item_id]   # 可选：移除键值为0的项
            return True
        return False