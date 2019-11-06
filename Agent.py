import sys
import random as rnd
from Action import Action
from GameObject import GameObject
from Tile import Tile
from typing import Optional


class Agent:
    max_reward = 10
    __learning_rate = 0.8
    __discount_factor = 0.8
    __discovery_chance = 0.3
    BASE_REWARD = -1
    STARTING_STATE = 42
    MAX_Q = 10
    MIN_Q = -10

    def __init__(self, window, state_count: int, action_count: int):
        self.window = window
        self.tiles = window.tiles
        self.state_count = state_count
        self.action_count = action_count
        self.state = Agent.STARTING_STATE
        self.q_table = [[0 for _ in range(0, action_count)] for _ in range(0, state_count)]
        self.reward_table = [[0 for _ in range(0, self.action_count)] for _ in range(0, self.state_count)]
        self.init_rewards_table()

        print(self)

    def init_rewards_table(self):
        self.reward_table = [[0 for _ in range(0, self.action_count)] for _ in range(0, self.state_count)]

        for tile in self.tiles:
            self.update_rewards_table(tile, Action.RIGHT, 1, 0)
            self.update_rewards_table(tile, Action.LEFT, -1, 0)
            self.update_rewards_table(tile, Action.UP, 0, -1)
            self.update_rewards_table(tile, Action.DOWN, 0, 1)

    def get_valid_tile(self, tile: Tile, x_change: int, y_change: int) -> Optional[Tile]:
        try:
            tile = self.window.get_tile_at(tile.x + x_change, tile.y + y_change)
            if not tile.is_filled():
                return tile
        except IndexError:
            return None

        return None

    def update_rewards_table(self, tile, action: Action, x_change, y_change):
        dest_tile = self.get_valid_tile(tile, x_change, y_change)

        reward_value = None
        if dest_tile is not None:
            reward_value = Agent.BASE_REWARD
            if dest_tile.game_object == GameObject.FOOD:
                reward_value = 10  # reward value for making the movement

        self.reward_table[tile.state_index][action.value] = reward_value

    def tick(self) -> None:
        # we need to pick an action for our agent to complete.
        # so lets get the actions that can be taken in its current state:
        chosen_action = self.select_action()

        current_q = self.q_table[self.state][chosen_action]
        current_state_reward = self.reward_table[self.state][chosen_action]

        next_state = self.take_action(self.state, chosen_action)
        max_q_from_next_state = self.q_table[next_state][self.select_best_action(next_state)]

        # noinspection PyTypeChecker
        new_q = (1 - Agent.__learning_rate) * current_q + Agent.__learning_rate * (current_state_reward + Agent.__discount_factor * max_q_from_next_state)

        if new_q > Agent.MAX_Q:
            new_q = Agent.MAX_Q

        if new_q < Agent.MIN_Q:
            new_q = Agent.MIN_Q

        self.q_table[self.state][chosen_action] = new_q
        self.state = next_state

        # move food to a random location after its been picked up
        if self.tiles[next_state].game_object == GameObject.FOOD:
            self.tiles[next_state].game_object = None
            self.tiles[rnd.randint(0, self.tiles.__len__() - 1)].game_object = GameObject.FOOD
            self.window.tiles = self.tiles
            self.init_rewards_table()

        # move agent back to start after finding food
        # if self.tiles[self.state].game_object == GameObject.FOOD:
        #     self.state = Agent.STARTING_STATE

    def take_action(self, state, action: int) -> int:
        x_change = 0
        y_change = 0

        if action == Action.RIGHT.value:
            x_change = 1

        if action == Action.LEFT.value:
            x_change = -1

        if action == Action.UP.value:
            y_change = -1

        if action == Action.DOWN.value:
            y_change = 1

        current_tile = self.tiles[state]
        new_tile = self.window.get_tile_at(current_tile.x + x_change, current_tile.y + y_change)
        return new_tile.state_index

    def select_action(self) -> int:
        if rnd.random() < Agent.__discovery_chance:
            chosen_action = self.select_random_action()
        else:
            chosen_action = Agent.select_best_action(self, self.state)

        if self.reward_table[self.state][chosen_action] is None:
            chosen_action = self.select_action()

        return chosen_action

    def select_random_action(self) -> int:
        return rnd.randint(0, Action.__len__() - 1)

    def select_best_action(self, state) -> int:
        highest_val = None
        highest_action = None
        q_values = []

        for action in Action:
            if self.reward_table[self.state][action.value] is None:
                continue

            current_q = self.q_table[state][action.value]
            q_values.append(current_q)
            if highest_val is None or current_q > highest_val:
                highest_val = current_q
                highest_action = action

        if len(set(q_values)) == 1:
            return self.select_random_action()

        return highest_action.value

    def __str__(self):
        space_between = 8
        string = "\n"

        string += "Reward Table\n"
        string += "\t\t"
        for action in Action:
            string += Agent.add_spacing(f"{str(action)[Action.__name__.__len__() + 1:]}", space_between)

        for reward_index in range(0, self.state_count):
            string += f"\n{reward_index}\t\t"
            for action in Action:
                string += Agent.add_spacing(f"{self.reward_table[reward_index][action.value]}", space_between)

        string += "\n\nQ Table\n"
        string += "\t\t"
        for action in Action:
            string += Agent.add_spacing(f"{str(action)[Action.__name__.__len__() + 1:]}", space_between)

        for q_index in range(0, self.state_count):
            string += f"\n{q_index}\t\t"
            for action in Action:
                string += Agent.add_spacing(f"{self.q_table[q_index][action.value]}", space_between)

        return string

    @staticmethod
    def add_spacing(string, space_between):
        # we want a space of "space_between" so we need to pad after the text for this space
        string_length = string.__len__()
        spacing_needed = space_between - string_length

        for i in range(0, spacing_needed):
            string += " "

        return string

    def get_tile_by_state_index(self, state_index):
        return self.tiles