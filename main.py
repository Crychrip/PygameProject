import pygame
from game import Game
from camp import Camp
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("游戏demo")

    # 加载中文字体
    font = None
    font_names = ['simhei', 'microsoft yahei', 'simsun', 'noto sans cjk sc']
    for name in font_names:
        try:
            font = pygame.font.SysFont(name, 36)
            if font.size("测试")[0] > 0:
                break
        except:
            continue
    if font is None:
        font = pygame.font.Font(None, 36)
        print("警告：未找到中文字体")
    
    # 场景初始化
    current_scene = "camp"
    game = None
    camp = Camp(screen, font)

    def switch_to_battle():
        nonlocal current_scene, game
        screen.fill((0,0,0))
        font_big = pygame.font.Font(None, 48)
        text = font_big.render("NOW LOADING...", True, (255,255,255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()
        pygame.event.pump()
        game = Game(screen, font, switch_to_camp)
        current_scene = "battle"

    def switch_to_camp():
        nonlocal current_scene, camp
        camp = Camp(screen, font)
        current_scene = "camp"

    clock = pygame.time.Clock()
    running = True

    # 场景转换
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if current_scene == "camp":
            camp.handle_events(events)
            camp.update()
            camp.draw()
            if not camp.running:
                if camp.quit_to_exit:
                    running = False
                else:
                    switch_to_battle()
        elif current_scene == "battle":
            game.handle_events(events)
            game.update()
            game.draw()
            game.clock.tick(60)
            if game.wants_to_exit_to_camp():
                switch_to_camp()
                continue
            if not game.running:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()