import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, BLACK

class UIManager:
    def __init__(self, font):
        self.font = font

    def draw_game_ui(self, surface, player_health, enemy_count):
        health_text = self.font.render(f"生命: {player_health}", True, WHITE)
        surface.blit(health_text, (10, 10))
        enemy_text = self.font.render(f"敌人数: {enemy_count}", True, WHITE)
        surface.blit(enemy_text, (10, 50))

    def draw_game_over(self, surface):
        go_text = self.font.render("游戏结束！按 R 键重新开始", True, WHITE)
        rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(go_text, rect)

    def draw_upgrade_menu(self, surface, upgrades, selected_index=0):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        title = self.font.render("升级！选择一个强化", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(title, title_rect)
        for i, up in enumerate(upgrades):
            color = (255, 255, 0) if i == selected_index else WHITE
            text = self.font.render(up["name"], True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 80))
            surface.blit(text, rect)