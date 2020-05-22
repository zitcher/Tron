import numpy as np
import pickle

from torch import nn
import torch

class DeepQModel(nn.Module):
    def __init__(self, input_channels=9, num_classes=4):
        super(DeepQModel, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(input_channels, 256, kernel_size=5, stride=1, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            nn.Conv2d(512, 1024, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(1024, 1024, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(1024, 1024, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(1024 * 6 * 6, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        """
        Predicts the rewards for actions given an game state using fully connected layers

        :return: the predicted label as a tensor
        """
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class QTable:
    def __init__(self, num_actions=4):
        self.num_actions = num_actions
        self.table = dict()

    def knows_state(self, state):
        return state in self.table

    def init_state(self, state):
        self.table[state] = [0] * self.num_actions

    def set_state_action_as_index(self, state, action, value):
        if not self.knows_state(state):
            self.init_state(state)

        self.table[state][action] = value

    def get_optimal_action(self, state):
        if self.knows_state(state):
            return np.argmax(self.table[state])
        else:
            return np.random.randint(self.num_actions)

    def get_state_action_value(self, state, action):
        if not self.knows_state(state):
            self.init_state(state)
        return self.table[state][action]

    def save_table(self, path):
        with open(path, 'wb') as fp:
            pickle.dump(self.table, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def load_table(self, path):
        with open(path, 'rb') as fp:
            self.table = pickle.load(fp)
