import random
from settings import UPGRADE_OPTIONS

class UpgradeManager:
    @staticmethod
    def get_random_upgrades(count=3):
        return random.sample(UPGRADE_OPTIONS, min(count, len(UPGRADE_OPTIONS)))

    @staticmethod
    def apply_upgrade(player, weapons, upgrade):
        stat = upgrade["stat"]
        value = upgrade["value"]
        if stat == "damage":
            player.damage += value
        elif stat == "attack_speed":
            player.attack_speed += value
        elif stat == "speed":
            player.base_speed += value
        elif stat == "max_health":
            player.max_health += value
            player.health += value
        elif stat == "health_regen":
            player.health = min(player.max_health, player.health + value)