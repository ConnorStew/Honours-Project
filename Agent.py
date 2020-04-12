import pygame
import numpy
from keras.models import Sequential
from keras.layers import Dense

import Environment as Environment
import random as rnd
from State import State
from Action import Action
import os

from Tile import Tile


class Agent:
    """ An Individual agent in the simulation. """

    __MAX_REWARD = 10  # The maximum reward given from a single action.
    __LEARNING_RATE = 0.8  # Determines how fast the agent learns from new stimulus.
    __DISCOUNT_FACTOR = 0.8  # The closer to 1 the higher the value the agent places on long term.
    __DISCOVERY_CHANCE = 0.3  # The percentage chance that the agent will choose to explore instead of exploit.
    __DEFAULT_REWARD = -1
    __FOOD_REWARD = 2

    __MAX_Q = 10
    __MIN_Q = -10

    def __init__(self, environment: Environment, start_x: int, start_y: int):
        self.environment = environment
        self.q_table = [[0 for _ in range(0, environment.action_count)] for _ in range(0, environment.state_count)]
        self.state = State()
        self.state.x = start_x
        self.state.y = start_y
        self.state_size = len(self.state.to_array())

        # values are in one line (state values)(possible actions)
        self.data = numpy.array([], dtype=float)
        self.model = Sequential()

        self.model.add(Dense(4, activation='relu', input_dim=self.state_size))  # input layer
        self.model.add(Dense(4, activation='relu'))  # hidden layer
        self.model.add(Dense(4, activation='softmax'))  # output layer

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        sprite_offset = 5
        sprite_width = environment.tile_size[0] - sprite_offset
        sprite_height = environment.tile_size[1] - sprite_offset
        self.sprite = pygame.image.load(f'{os.getcwd()}/agent.png')
        self.sprite = pygame.transform.scale(self.sprite, (sprite_width, sprite_height))

    def tick(self) -> None:
        # we need to pick an action for our agent to complete.
        # so lets get the actions that can be taken in its current state:
        self.take_action()

    def take_action(self) -> None:
        if len(self.data) < 2:
            action = rnd.choice(list(Action))
        else:
            result = self.model.predict([numpy.array([self.state.to_array()])])
            highest_index = numpy.argmax(result[0])
            if highest_index == 0:
                action = Action.RIGHT

            if highest_index == 1:
                action = Action.LEFT

            if highest_index == 2:
                action = Action.UP

            if highest_index == 3:
                action = Action.DOWN

        x_change = 0
        y_change = 0

        right_value = 0.0
        left_value = 0.0
        up_value = 0.0
        down_value = 0.0

        if action == Action.RIGHT:
            right_value = 1.0
            x_change = 1

        if action == Action.LEFT:
            left_value = 1.0
            x_change = -1

        if action == Action.UP:
            up_value = 1.0
            y_change = -1

        if action == Action.DOWN:
            down_value = 1.0
            y_change = 1

        # insert new data
        state_array = numpy.array(self.state.to_array() + [right_value, left_value, up_value, down_value])

        if len(self.data) == 0:
            self.data = numpy.array([state_array])
        else:
            self.data = numpy.vstack((self.data, state_array))

        if len(self.data) >= 2:
            x_train = self.data[:, 0:self.state_size]
            y_train = self.data[:, self.state_size:]
            self.model.fit(x_train, y_train, epochs=10)

        try:
            current_tile = self.get_current_tile()
            if current_tile.contains_food:
                self.state.current_reward = Agent.__FOOD_REWARD
            else:
                self.state.current_reward = Agent.__DEFAULT_REWARD

            new_tile = self.environment.get_valid_tile(current_tile, x_change, y_change)
            if new_tile.contains_food:
                self.state.new_reward = Agent.__FOOD_REWARD
            else:
                self.state.new_reward = Agent.__DEFAULT_REWARD
        except:
            print(self)
            exit(-1)

        self.state.x = new_tile.x
        self.state.y = new_tile.y

    def select_action(self) -> int:
        if rnd.random() < Agent.__DISCOVERY_CHANCE:
            chosen_action = self.select_random_action()
        else:
            chosen_action = Agent.select_best_action(self, (self.state.x, self.state.y))

        if self.environment.reward_table[(self.state.x, self.state.y)][chosen_action] is None:
            chosen_action = self.select_action()

        return chosen_action

    @staticmethod
    def select_random_action() -> int:
        return rnd.randint(0, Action.__len__() - 1)

    def select_best_action(self, position) -> int:
        highest_val = None
        highest_action = None
        q_values = []

        for action in Action:
            if self.environment.reward_table[(self.state.x, self.state.y)][action.value] is None:
                continue

            current_q = self.q_table[position][action.value]
            q_values.append(current_q)
            if highest_val is None or current_q > highest_val:
                highest_val = current_q
                highest_action = action

        if len(set(q_values)) == 1:
            return self.select_random_action()

        return highest_action.value

    def __str__(self):
        # space_between = 8
        # string = "\n"
        #
        # string += "\n\nQ Table\n"
        # string += "\t\t"
        # for action in Action:
        #     string += Agent.add_spacing(f"{str(action)[Action.__name__.__len__() + 1:]}", space_between)
        #
        # for q_index in range(0, len(self.q_table)):
        #     string += f"\n{q_index}\t\t"
        #     for action in Action:
        #         string += Agent.add_spacing(f"{self.q_table[q_index][action.value]}", space_between)

        return self.data.tostring()

    @staticmethod
    def add_spacing(string, space_between):
        # we want a space of "space_between" so we need to pad after the text for this space
        string_length = string.__len__()
        spacing_needed = space_between - string_length

        for i in range(0, spacing_needed):
            string += " "

        return string

    def get_current_tile(self) -> Tile:
        return self.environment.get_tile_at(self.state.x, self.state.y)

    def draw(self, surface):
        current_tile = self.get_current_tile()
        surface.blit(self.sprite, (current_tile.world_x, current_tile.world_y))
