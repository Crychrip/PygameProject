from formula import EQUIPMENTS

class EquipmentManager:
    def __init__(self, material_manager):
        self.material_mgr = material_manager   # 用于检查是否有该物品
        self.equipped_items = []               # 已装备的物品ID列表

    def equip(self, item_id):
        if item_id in self.material_mgr.inventory and self.material_mgr.inventory[item_id] > 0:
            if item_id not in self.equipped_items:
                self.equipped_items.append(item_id)
                return True
        return False

    def unequip(self, item_id):
        if item_id in self.equipped_items:
            self.equipped_items.remove(item_id)
            return True
        return False

    def get_total_bonus(self):
        bonus = {"damage": 0, "max_health": 0, "harvest_bonus": 0, "speed": 0, "attack_speed": 0}
        for item_id in self.equipped_items:
            effect = EQUIPMENTS.get(item_id, {}).get("effect", {})
            for stat, val in effect.items():
                if stat in bonus:
                    bonus[stat] += val
        return bonus

    def to_dict(self):
        return {"equipped_items": self.equipped_items}

    def from_dict(self, data):
        self.equipped_items = data.get("equipped_items", [])