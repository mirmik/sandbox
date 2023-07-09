#!/usr/bin/env python3

import math 
import matplotlib.pyplot as plt
import random
import numpy


class Gamer:
    def __init__(self, start_strategy, speed, error, cond_equal):
        self.strategy = start_strategy
        self.error = error
        self.cond_equal = cond_equal
        self.speed = speed

    def move(self):
        r = random.random()
        return (self.strategy-self.error) > r

    def predict(self):
        r = random.random()
        return self.strategy  > r

    def knowlage(self, B, N):
        prediction_success = 0
        for i in range(N):
            prediction = self.predict()
            move = B.move()
            if move == prediction and self.cond_equal:
                prediction_success += 1
            if move != prediction and not self.cond_equal:
                prediction_success += 1
        return prediction_success / N 

    def update_model(self, win, true_false):
        target = true_false
        if not win:
            target = not true_false

        if target:
            self.strategy += self.speed
            #self.strategy += (1-self.strategy) * 0.001
        else:
            self.strategy -= self.speed
            #self.strategy -= (self.strategy) * 0.001

        self.strategy = min(1, self.strategy)
        self.strategy = max(0, self.strategy)
       

A = Gamer(0.5, speed=0.0001, error = 0.1, cond_equal = True)
B = Gamer(0.5, speed=0.000001, error = 0.001, cond_equal = False)


#A_knowlage = []
#B_knowlage = []
A_strategy = []
B_strategy = []
winners = []
for i in range(1000000):
    #A_kn = A.knowlage(B,1000)
    #B_kn = B.knowlage(A,1000)
    #A_knowlage.append(A_kn)
    #B_knowlage.append(B_kn)  
    A_strategy.append(A.strategy)  
    B_strategy.append(B.strategy)  

    A_move = A.move()
    B_move = B.move()

    A_win = A_move == B_move
    winners.append(A_win)

    A.update_model(A_win, A_move)
    B.update_model(not A_win, B_move)
    
acc = 0
for i in range(len(winners)):
    if winners[i]:
        acc += 1

print(acc/len(winners))

plt.plot(A_strategy, B_strategy, numpy.linspace(0,1,100), numpy.linspace(0,1,100), numpy.linspace(0,1,100), [0.5]*100, [0.5]*100, numpy.linspace(0,1,100))
#plt.plot(A_model, B_model)
plt.show()