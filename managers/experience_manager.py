import math
from settings import EXPERIENCE_ATTRACT_RADIUS, EXPERIENCE_ATTRACT_SPEED, BASE_EXPERIENCE_TO_LEVEL, EXPERIENCE_SCALING
from entities.experience import ExperienceOrb

class ExperienceManager:
    def __init__(self):
        self.orbs = []
        self.experience = 0
        self.level = 1
        self.next_level_exp = BASE_EXPERIENCE_TO_LEVEL

    def add_orb(self, x, y, value=10):
        self.orbs.append(ExperienceOrb(x, y, value))
        # print("经验球已添加")

    def update_orbs(self, player_x, player_y, dt):
        collected = 0
        for orb in self.orbs[:]:
            dx = player_x - orb.x
            dy = player_y - orb.y
            dist = math.hypot(dx, dy)
            if dist < EXPERIENCE_ATTRACT_RADIUS:
                if orb.attracted_update(player_x, player_y, EXPERIENCE_ATTRACT_SPEED, dt):
                    self.orbs.remove(orb)
                    collected += orb.value
        return collected

    def add_experience(self, amount):
        self.experience += amount
        leveled = False
        while self.experience >= self.next_level_exp:
            self.experience -= self.next_level_exp
            self.level += 1
            self.next_level_exp = int(BASE_EXPERIENCE_TO_LEVEL * (EXPERIENCE_SCALING ** (self.level - 1)))
            leveled = True
        return leveled

    def get_level_progress(self):
        return self.experience, self.next_level_exp