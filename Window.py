import time
from typing import Tuple, List

from Action import Action, ActionType
from GameObject import GameObject
from State import State
from Tile import Tile
from Agent import Agent
import pygame
import os


class Window:
    def __init__(self, tile_size: Tuple[int, int], tile_amount: Tuple[int, int]):
        Window.init_pygame()

        self.tile_size = tile_size
        self.tile_amount = tile_amount
        self.tiles = {}

        for x in range(0, tile_amount[0]):
            for y in range(0, tile_amount[1]):
                self.tiles[(x, y)] = Tile(x, y, tile_size[0], tile_size[1])

        self.font_size = 12
        default_font = pygame.font.get_default_font()
        self.font_renderer = pygame.font.Font(default_font, self.font_size)
        self.surface = pygame.display.set_mode((tile_size[0] * tile_amount[0] + 1, tile_size[1] * tile_amount[1] + 1))

        self.fill_tiles()

        self.agent_image = pygame.image.load(f'{os.getcwd()}/agent.png')
        self.agent_image_offset = 5
        self.agent_image = pygame.transform.scale(self.agent_image, (tile_size[0] - self.agent_image_offset, tile_size[1] - self.agent_image_offset))

        state_table = self.init_agent_values()
        self.agent = Agent(state_table)

        self.main_loop()

    def init_agent_values(self) -> ([int], [int]):
        q_table = []
        for x in range(0, self.tile_amount[0]):
            for y in range(0, self.tile_amount[1]):
                actions = []
                self.check_tile(actions, ActionType.RIGHT, x, y, 1, 0)
                self.check_tile(actions, ActionType.LEFT, x, y, -1, 0)
                self.check_tile(actions, ActionType.DOWN, x, y, 0, 1)
                self.check_tile(actions, ActionType.UP, x, y, 0, -1)
                q_table.append(State(x, y, actions))

        return q_table

    def check_tile(self, actions: List[Action], action_type: ActionType, tile_x: int, tile_y: int, x_change: int, y_change: int):
        can_move_to = True

        try:
            if self.tiles[(tile_x + x_change,tile_y + y_change)].is_filled():
                can_move_to = False
        except KeyError:
            can_move_to = False

        reward_amount = -1
        if can_move_to:
            if self.tiles[(tile_x, tile_y)].game_object == GameObject.FOOD:
                reward_amount = 10
        else:
            reward_amount = None

        actions.append(Action(action_type, reward_amount))

    @staticmethod
    def init_pygame() -> None:
        pygame.init()
        pygame.display.set_caption('RL Maths')
        pygame.font.init()

    def main_loop(self) -> None:
        # time_between_ticks = 6
        # last_tick_time = int(time.time())
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # current_time = int(time.time())
            # time_since_last_tick = current_time - last_tick_time
            # if time_since_last_tick > time_between_ticks:
            #     last_tick_time = int(time.time())

            self.agent.tick()

            self.draw()

    def draw(self) -> None:
        self.surface.fill((0, 0, 0))

        for tile in self.tiles.values():
            if tile.game_object is GameObject.FOOD:
                tile.colour = (0, 255, 0)
            pygame.draw.rect(self.surface, tile.colour, (tile.world_x, tile.world_y, self.tile_size[0], self.tile_size[1]), tile.thickness)
            label = self.font_renderer.render(f"{tile.x}, {tile.y}", True, (0, 255, 0))
            self.surface.blit(label, (tile.world_x + tile.width / 2, tile.world_y + tile.height / 2))

        agent_state = self.agent.state
        agent_tile = self.tiles[(agent_state.x, agent_state.y)]
        self.surface.blit(self.agent_image, (agent_tile.world_x, agent_tile.world_y))

        pygame.display.update()

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
        self.tiles[(20, 8)].game_object = GameObject.FOOD
        self.tiles[(3, 12)].game_object = GameObject.FOOD

    def fill_square(self, x, y, width, height) -> None:
        for _x in range(x, x + width):
            for _y in range(y,  y + height):
                self.tiles[(_x, _y)].fill()