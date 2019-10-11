import sys
from typing import List
import random as rnd
from Action import Action, ActionType
from State import State


class Agent:
    max_reward = 10
    __learning_rate = 0.8

    def __init__(self,  state_table: List[State]):
        self.state_table = state_table
        self.state = self.get_state_at(2, 3)

    def tick(self) -> None:
        # we need to pick an action for our agent to complete.
        # so lets get the actions that can be taken in its current state:
        actions = self.state.actions

        chosen_action = self.get_best_action(actions)
        current_q_value = chosen_action.reward

        self.state = self.take_action(chosen_action)

        new_q_value = current_q_value + Agent.__learning_rate * self.get_best_action(self.state.actions).reward
        chosen_action.reward = new_q_value

        print(self)

    def take_action(self, action) -> State:
        action_type = action.action_type

        x_change = 0
        y_change = 0

        if action_type == ActionType.RIGHT:
            x_change = 1

        if action_type == ActionType.LEFT:
            x_change = -1

        if action_type == ActionType.UP:
            y_change = -1

        if action_type == ActionType.DOWN:
            y_change = 1

        return self.get_state_at(self.state.x + x_change, self.state.y + y_change)

    @staticmethod
    def get_best_action(actions) -> Action:
        highest_actions = []
        max_q = -sys.maxsize
        for action in actions:
            q_value = action.reward

            if q_value is None:
                continue

            if q_value > max_q:
                max_q = q_value
                highest_actions.clear()
                highest_actions.append(action)
            elif q_value == max_q:
                highest_actions.append(action)

        chosen_action = highest_actions[0]
        if highest_actions.__len__() > 1:
            chosen_action = highest_actions[rnd.randint(0, highest_actions.__len__() - 1)]

        return chosen_action

    def __str__(self):
        string = "\n"

        for state in self.state_table:
            string += f"\n{str(state)}"

        return string

    def get_state_at(self, x, y):
        return self.state_table[x * 20 + y]
