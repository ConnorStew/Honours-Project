from Action import ActionType


class State:
    def __init__(self, x, y, actions):
        self.x = x
        self.y = y
        self.actions = actions

    def __str__(self):
        string = f"{self.x}, {self.y}:"

        for action in self.actions:
            string += f"\n\t{ActionType(action.action_type)}:{action.reward}"

        return string
