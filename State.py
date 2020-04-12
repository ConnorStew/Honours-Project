
STATE_VARIABLES = 2


class State:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.new_reward = 0
        self.current_reward = 0

    def to_array(self):
        return [float(self.x), float(self.y), float(self.new_reward), float(self.current_reward)]
