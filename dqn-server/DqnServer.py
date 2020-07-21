import math
import random
import numpy as np
from collections import namedtuple
from itertools import count
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from drawnow import drawnow
from optim import modelOptimise
from utils import ReplayMemory

import os
class DqnServer():
    def __init__(self, device, nActions, policyNet, targetNet, memory, PATH):
        self.device = device
        self.transitionFormat = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))
        self.updateInterval = 4          # 4 episode -> target := predict 
        self.nActions = nActions
        self.policyNet = policyNet                          # Mlp(2, (10, 5), 4).to(self.device)
        self.targetNet = targetNet                          # Mlp(2, (10, 5), 4).to(self.device)
        self.memory = memory                                # it is updated outside the server

        # check if there is trained neural network, if yes use it. 
        if (os.path.isfile(PATH)):
            self.policyNet.load_state_dict(torch.load(PATH))

        self.targetNet.load_state_dict(self.policyNet.state_dict())
        self.targetNet.eval()
        self.optimiser = optim.RMSprop(self.policyNet.parameters())
        self.optimiser.param_groups[0]['lr'] = 0.0001
        self.episodeCount = 0
        self.stepCount = 0
        self.isEpisodeFinished = 0
        self.isExplore = 1
    def setMemory(self, memory):
        self.memory = memory                                # it is updated outside the server

    def train(self):
        modelOptimise(self.memory, self.device, self.transitionFormat, self.policyNet, self.targetNet, self.optimiser)
        self.updateTargetNet()

    def updateTargetNet(self):
        if self.episodeCount % self.updateInterval == 0:
            self.targetNet.load_state_dict(self.policyNet.state_dict())

    def episodeFinish(self):
        self.episodeCount = self.episodeCount + 1
        self.isEpisodeFinished = 1

    def getAction(self, state):
        if self.isEpisodeFinished == 1:
            EPS_START = 0.05
            EPS_END = 0.05
            EPS_DECAY = 10000
            sample = random.random()
            eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * self.episodeCount / EPS_DECAY)
            self.isEpisodeFinished = 0
            if sample > eps_threshold:
                self.isExplore = 1
            else:
                self.isExplore = 0

        self.stepCount += 1

        if self.isExplore == 1:
            with torch.no_grad():
                return self.policyNet(torch.tensor([state], dtype=torch.float)).max(1)[1].view(1, 1).item()
        else:
            return random.randint(0, eval(self.nActions) - 1)