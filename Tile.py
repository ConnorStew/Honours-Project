import pygame


class Tile:

    def __init__(self, x: int, y: int, width: int, height: int, state_index: int):
        self.x = x
        self.y = y
        self.world_x = x * width
        self.world_y = y * height
        self.width = width
        self.height = height
        self.__filled = False
        self.colour = (50, 0, 0)
        self.thickness = 1
        self.game_object = None
        self.state_index = state_index
        self.contains_food = False

    def fill(self) -> None:
        self.__filled = True
        self.colour = (255, 255, 255)

    def is_filled(self) -> bool:
        return self.__filled

    def draw(self, surface, font_renderer):
        draw_colour = self.colour

        if self.contains_food:
            draw_colour = (0, 50, 0)

        pygame.draw.rect(surface, draw_colour, (self.world_x, self.world_y, self.width, self.height), self.thickness)
        label = font_renderer.render(f"{self.state_index}", True, (0, 255, 0))
        surface.blit(label, (self.world_x + self.width / 2, self.world_y + self.height / 2))

    def __str__(self):
        return f'Grid Location: {self.x}, {self.y}\nWorld Location: {self.world_x}, {self.world_y}'
