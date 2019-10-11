from enum import IntEnum


class ActionType(IntEnum):
    LEFT = 0,
    RIGHT = 1,
    UP = 2,
    DOWN = 3


class Action:
    def __init__(self, action_type: ActionType, reward: int):
        self.action_type = action_type
        self.reward = reward

    def take_action(self):
        if self.action_type == ActionType.LEFT:
            self.move_and_update(-1, 0)

        if self.action_type == ActionType.RIGHT:
            self.move_and_update(1, 0)

        if self.action_type == ActionType.UP:
            self.move_and_update(0, -1)

        if self.action_type == ActionType.DOWN:
            self.move_and_update(0, 1)