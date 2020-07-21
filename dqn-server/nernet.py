import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

class Mlp(nn.Module):
    def __init__(self, conf): # Example conf: "Linear:2*10->ReLU->Linear:10*5->ReLU->5*2"
        super(Mlp, self).__init__()
        self.layerNum = 0
        its = conf.split('->')
        for it in its:
            ft = it.split(':')
            if len(ft) == 1: 
                exec('self.layer' + str(self.layerNum) + ' = nn.'+ ft[0] +'()')
                self.layerNum = self.layerNum + 1
                continue
            if len(ft) == 2:
                sz = ft[1].split('*')
                exec('self.layer' + str(self.layerNum) + ' = nn.'+ ft[0] +'(' + sz[0] + ',' + sz[1] + ')')
                self.layerNum = self.layerNum + 1
                continue
            else:
                print('Error [nernet.py]: Format Not Support!')
                self.layerNum = self.layerNum + 1
        stop = 1
    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).   
    def forward(self, x):
        t = x
        for i in range(self.layerNum):
            t = eval('self.layer' + str(i) + '(t)')
        return t