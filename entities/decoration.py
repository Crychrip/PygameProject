import pygame
from settings import TILE_SIZE

class Decoration:
    def __init__(self, x, y, biome_name, image, drop_item, drop_amount):
        self.x = x
        self.y = y
        self.biome = biome_name
        self.image = image
        self.radius = TILE_SIZE // 3 
        self.drop_item = drop_item
        self.drop_amount = drop_amount


    def draw(self, surface, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        w, h = self.image.get_size()
        dest_x = screen_x - w // 2
        dest_y = screen_y - h // 2
        surface.blit(self.image, (dest_x, dest_y))

    def get_rect(self):
        # 碰撞交互
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius*2, self.radius*2)