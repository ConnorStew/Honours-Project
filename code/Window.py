import time
import math
from typing import Tuple

from Action import Action
from GameObject import GameObject
from Tile import Tile
from Agent import Agent
import pygame
import os


def truncate(number, decimals=1):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


class Window:
    def __init__(self, tile_size: Tuple[int, int], tile_amount: Tuple[int, int]):
        self.tile_size = tile_size
        self.tile_amount = tile_amount
        self.tile_offset = 10
        self.tiles = []

        state_index_count = 0
        for x in range(0, tile_amount[0]):
            for y in range(0, tile_amount[1]):
                self.tiles.append(Tile(x, y, tile_size[0], tile_size[1], state_index_count))
                state_index_count += 1

        self.fill_tiles()

        self.agent_image = pygame.image.load(f'{os.getcwd()}/resources/agent.png')
        self.agent_image_offset = 5
        self.agent_image = pygame.transform.scale(self.agent_image, (tile_size[0] - self.agent_image_offset, tile_size[1] - self.agent_image_offset))

        self.agent = Agent(self, state_index_count, Action.__len__())

        # for i in range(0, 20000):
        #     print(i)
        #     self.agent.tick()

        Window.init_pygame()

        self.font_size = 8
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
        time_between_ticks = 60
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

            self.draw()

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        for tile in self.tiles:
            if tile.game_object is GameObject.FOOD:
                pygame.draw.rect(self.surface, (0, 255, 0), (tile.world_x, tile.world_y, self.tile_size[0], self.tile_size[1]), tile.thickness)
            else:
                pygame.draw.rect(self.surface, tile.colour, (tile.world_x, tile.world_y, self.tile_size[0], self.tile_size[1]), tile.thickness)

            #label = self.font_renderer.render(f"{tile.state_index}", True, (0, 255, 0))
            #self.surface.blit(label, (tile.world_x + tile.width / 2, tile.world_y + tile.height / 2))

            middle_of_tile_x = tile.world_x + tile.width / 2
            middle_of_tile_y = tile.world_y + tile.height / 2

            if not tile.is_filled():
                up_value = self.get_action_value(tile, Action.UP)
                up_label = self.font_renderer.render(f"{up_value}", True, (0, 255, 0))
                self.surface.blit(up_label, (middle_of_tile_x, middle_of_tile_y - self.tile_offset))

                down_value = self.get_action_value(tile, Action.DOWN)
                down_label = self.font_renderer.render(f"{down_value}", True, (0, 255, 0))
                self.surface.blit(down_label, (middle_of_tile_x, middle_of_tile_y + self.tile_offset))

                left_value = self.get_action_value(tile, Action.LEFT)
                left_label = self.font_renderer.render(f"{left_value}", True, (0, 255, 0))
                self.surface.blit(left_label, (middle_of_tile_x - self.tile_offset, middle_of_tile_y))

                right_value = self.get_action_value(tile, Action.RIGHT)
                right_label = self.font_renderer.render(f"{right_value}", True, (0, 255, 0))
                self.surface.blit(right_label, (middle_of_tile_x + self.tile_offset, middle_of_tile_y))

        agent_tile = self.tiles[self.agent.state]
        self.surface.blit(self.agent_image, (agent_tile.world_x, agent_tile.world_y))

        pygame.display.update()

    def get_action_value(self, tile, action) -> float:
        return truncate(self.agent.q_table[tile.state_index][action.value], 1)

    def fill_tiles(self) -> None:
        x_amount = self.tile_amount[0]
        y_amount = self.tile_amount[1]

        # filling in border
        self.fill_square(0, 0, x_amount, 1)
        self.fill_square(0, 0, 1, y_amount)
        self.fill_square(x_amount - 1, 0, 1, y_amount)
        self.fill_square(0, y_amount - 1, x_amount, 1)

        # filling in obstacles
        self.fill_square(2, 5, 5, 5)
        self.fill_square(8, 2, 5, 5)
        self.fill_square(6, 8, 5, 2)
        self.fill_square(6, 11, 2, 7)
        self.fill_square(15, 2, 6, 2)
        self.fill_square(17, 12, 5, 5)

        # add some food
        self.get_tile_at(20, 8).game_object = GameObject.FOOD
        self.get_tile_at(3, 12).game_object = GameObject.FOOD

    def fill_square(self, x, y, width, height) -> None:
        for _x in range(x, x + width):
            for _y in range(y,  y + height):
                self.get_tile_at(_x, _y).fill()

    def get_tile_at(self, x, y):
        return self.tiles[x * self.tile_amount[1] + y]
