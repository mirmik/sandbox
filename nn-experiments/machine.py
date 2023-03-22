#!/usr/bin/env python3

import torch
import torch.nn as nn
import torch.nn.functional as F

import matplotlib.pyplot as plt
import math
import dataclasses

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

class Machine:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.vel = 0
        self.acc = 0
        self.theta = 0
        self.thetavel = 0
        self.memory = []

    def apply(self, delta):
        self.vel += self.acc * delta
        xvel = self.vel * math.cos(self.theta)
        yvel = self.vel * math.sin(self.theta)
        xacc = self.acc * math.cos(self.theta)
        yacc = self.acc * math.sin(self.theta)
        self.xpos += xvel * delta + 0.5 * xacc * delta * delta
        self.ypos += yvel * delta + 0.5 * yacc * delta * delta
        self.theta += self.thetavel * delta

    def set_control(self, acc, thetavel):
        self.acc = acc
        self.thetavel = thetavel

    def get_state(self):
        return dataclasses.asdict(self)

    def do_step(self, delta, acc, thetavel):
        memory.append(get_state())
        set_control(acc, thetavel)
        apply(delta)       

    def distance_to(self, target):
        return math.sqrt((self.xpos - target[0]) ** 2 + (self.ypos - target[1]) ** 2)
        
def plot_machine(machine):
    ax.clear()
    ax.plot([machine.xpos], [machine.ypos], 'ro')
    ax.plot([machine.xpos, machine.xpos + 0.5 * math.cos(machine.theta)], [machine.ypos, machine.ypos + 0.5 * math.sin(machine.theta)], 'b-')
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.draw()
    plt.pause(0.001)

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer1 = nn.Linear(4, 32)
        self.layer2 = nn.Linear(32, 32)
        self.layer3 = nn.Linear(32, 2)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

model = Model()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# loss is the distance between the last position and the target
target = torch.tensor([0, 0], dtype=torch.float)

for epoch in range(10):
    machine = Machine(-10, -10)
    for step in range(100):
        action = model(state)
        machine.do_step(0.1, action[0], action[1])

    # final distance
    loss = torch.distance_to(target)
    optimizer.zero_grad()
    loss.backward()

    for state in reversed(machine.memory):
        optimizer.step()    