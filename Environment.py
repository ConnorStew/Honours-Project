from typing import Tuple

from Action import Action
from GameObject import GameObject
from Tile import Tile


class Environment:
    """ Represents the environment that Agents operate in. """

    __BASE_REWARD = -1  # The default reward for a tile with nothing in it.

    def __init__(self, tile_size: Tuple[int, int], tile_amount: Tuple[int, int]):
        """
        :param tile_size: the pixel size of each tile. tile_size[0] = x size, tile_size[1] = y size
        :param tile_amount: the amount of tiles. tile_amount[0] = x amount, tile_amount[1] = y amount
        """
        self.tiles = []
        self.tile_amount = tile_amount
        self.tile_size = tile_size
        self.action_count = Action.__len__()
        self.state_count = int(tile_amount[0] * tile_amount[1])

        state_index_count = 0
        for x in range(0, tile_amount[0]):
            for y in range(0, tile_amount[1]):
                self.tiles.append(Tile(x, y, tile_size[0], tile_size[1], state_index_count))
                state_index_count += 1

        self.tiles[10].contains_food = True

    def __fill_tiles(self) -> None:
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
            for _y in range(y, y + height):
                self.get_tile_at(_x, _y).fill()

    def get_tile_at(self, x, y):
        return self.tiles[x * self.tile_amount[1] + y]

    def get_valid_tile(self, tile, x_change, y_change):
        tile_x = tile.x + x_change
        tile_y = tile.y + y_change
        tile_index = tile_y + (tile_x * self.tile_amount[0])
        if tile_index >= len(self.tiles):
            return None
        else:
            return self.tiles[tile_index]