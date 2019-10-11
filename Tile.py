class Tile:

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.world_x = x * width
        self.world_y = y * height
        self.width = width
        self.height = height
        self.__filled = False
        self.colour = (0, 0, 0)
        self.thickness = 1
        self.game_object = None

    def fill(self) -> None:
        self.__filled = True
        self.colour = (255, 255, 255)

    def is_filled(self) -> bool:
        return self.__filled

    def __str__(self):
        return f'Grid Location: {self.x}, {self.y}\nWorld Location: {self.world_x}, {self.world_y}'
