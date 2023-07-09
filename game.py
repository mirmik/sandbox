#!/usr/bin/env python3

import math 
import matplotlib.pyplot as plt
import random
import numpy


class Gamer:
    def __init__(self, start_strategy, error, cond):
        self.strategy = start_strategy
        self.model = start_strategy
        self.error = error
        self.cond = cond

    def move(self):
        r = random.random()
        return r > self.strategy 

    def predict(self):
        r = random.random()
        return r > self.model 

    def knowlage(self, B, N):
        prediction_success = 0
        for i in range(N):
            prediction = self.predict()
            move = B.move()
            if move == prediction and self.cond:
                prediction_success += 1
            if move != prediction and not self.cond:
                prediction_success += 1
        return prediction_success / N 

    def update_model(self, true_false):
        if true_false:
            self.model += (1-self.model) * 0.001
        else:
            self.model -= (self.model) * 0.001

        if self.cond:
            self.strategy = self.model-self.error
        else:
            self.strategy = 1-(self.model-self.error)
       

A = Gamer(0.1, error = 0.4, cond = True)
B = Gamer(0.1, error = -0.4, cond = False)


A_knowlage = []
B_knowlage = []
A_strategy = []
B_strategy = []
A_model = []
B_model = []
for i in range(10000):
    A_kn = A.knowlage(B,1000)
    B_kn = B.knowlage(A,1000)
    A_knowlage.append(A_kn)
    B_knowlage.append(B_kn)  
    A_strategy.append(A.strategy)  
    B_strategy.append(B.strategy)  
    A_model.append(A.model)  
    B_model.append(B.model)

    A_move = A.move()
    B_move = B.move()

    A.update_model(B_move)
    B.update_model(A_move)
    
plt.plot(A_knowlage, B_knowlage)
plt.plot(A_strategy, B_strategy, A_model, B_model, numpy.linspace(0,1,100), numpy.linspace(0,1,100), numpy.linspace(0,1,100), [0.5]*100, [0.5]*100, numpy.linspace(0,1,100))
#plt.plot(A_model, B_model)
plt.show()