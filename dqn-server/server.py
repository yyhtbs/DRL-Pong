import socket
import json
import math
import random
import numpy as np
from collections import namedtuple
import torch
import torch.nn as nn
import torch.optim as optim
from DqnServer import DqnServer
from nernet import Mlp
import os
import io
from utils import ReplayMemory

# Create the service

device = torch.device("cpu")
policyNet = None
targetNet = None
dataAnalysisServerdqnSvc = None

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
conn, addr = serv.accept()
from_client = ''
## Initialise
connected = False

PATH = ''

memory = ReplayMemory(10000, namedtuple('Transition', ('state', 'action', 'next_state', 'reward')))

dqnSvc = None

while True:
    buffer = conn.recv(65535)
    if not buffer: break
    
    tdata = buffer.decode()

    tdata = tdata.split('#')
    for data in tdata:
        if data == '': continue
        # print(data)
        if 'Init' in data:
            its = data.split(':')

            policyNet = Mlp('Linear:' + its[1] + '*10->Sigmoid->Linear:10*10->Sigmoid->Linear:10*' + its[2]).to(device)
            targetNet = Mlp('Linear:' + its[1] + '*10->Sigmoid->Linear:10*10->Sigmoid->Linear:10*' + its[2]).to(device)
            PATH = './nn' + its[1] + 'x' + its[2] + '.conf'#
            dqnSvc = DqnServer(device, its[2], policyNet, targetNet, memory, PATH)
            conn.send("X".encode())
            connected = True

        elif connected and 'GetAction' in data:
            state = eval(data.split(':')[1])
            conn.send(str(dqnSvc.getAction(state)).encode()) # skip it to double the action
            # conn.send(str(random.randint(0, 1)).encode()) # skip it to double the action

        elif connected and 'Push' in data:
            its = data.split(':')
            idx         = its[1]
            state       = its[2]  
            action      = its[3]
            nextState   = its[5]  
            reward      = its[4]
            sample = (eval(state), eval(action), eval(nextState), eval(reward)) # (s, a, s', r)

            memory.push(sample)
            conn.send("X".encode()) # Finish Signal

        elif connected and 'Train' in data:
            dqnSvc.train()
            conn.send("X".encode()) # Finish Signal
            torch.save(policyNet.state_dict(), PATH)

        elif connected and 'EpisodeFinish' in data:
            its = data.split(':')
            idx         = its[1]
            dqnSvc.episodeFinish()
            conn.send("X".encode()) # Finish Signal
            torch.save(policyNet.state_dict(), PATH)

conn.close()
print ('client disconnected')