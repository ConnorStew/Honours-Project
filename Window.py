import time
from typing import Tuple

from Action import Action
from Environment import Environment
from GameObject import GameObject
from Agent import Agent
import pygame
from keras import backend as K


class Window:
    def __init__(self, tile_size: Tuple[int, int], tile_amount: Tuple[int, int]):
        self.environment = Environment(tile_size, tile_amount)
        self.agent = Agent(self.environment, 1, 1)

        # for i in range(0, 20000):
        #     print(i)
        #     self.agent.tick()

        Window.init_pygame()

        self.font_size = 6
        default_font = pygame.font.get_default_font()
        self.font_renderer = pygame.font.Font(default_font, self.font_size)
        self.surface = pygame.display.set_mode((tile_size[0] * tile_amount[0] + 1, tile_size[1] * tile_amount[1] + 1))

        self.main_loop()

    @staticmethod
    def init_pygame() -> None:
        pygame.init()
        pygame.display.set_caption('RL Maths')
        pygame.font.init()

    def main_loop(self) -> None:
        time_between_ticks = 0.5
        last_tick_time = int(time.time())
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.agent)
                    pygame.quit()

            current_time = int(time.time())
            time_since_last_tick = current_time - last_tick_time
            if time_since_last_tick > time_between_ticks:
                last_tick_time = int(time.time())
                self.agent.tick()

           # self.draw()

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        for tile in self.environment.tiles:
            tile.draw(self.surface, self.font_renderer)

        self.agent.draw(self.surface)

        pygame.display.update()


Window((50, 50), (20, 20))
