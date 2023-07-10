#!/usr/bin/env python3

import math 
import matplotlib.pyplot as plt
import random
import numpy
import sympy

class Gamer:
    def __init__(self, start_strategy, speed, error, cond_equal):
        self.strategy = start_strategy
        self.error = error
        self.cond_equal = cond_equal
        self.speed = speed

    def move(self):
        r = random.random()
        return (self.strategy-self.error) > r

    def moves(self):
        return self.strategy-self.error

    def update_model(self, win, true_false):
        target = true_false
        if not win:
            target = not true_false

        if target:
            self.strategy += self.speed
            #self.strategy += (1-self.strategy) * self.speed
        else:
            self.strategy -= self.speed
            #self.strategy -= (self.strategy) * self.speed

        if self.strategy-self.error > 1:
            self.strategy = 1 + self.error
        if self.strategy-self.error < 0:
            self.strategy = 0 + self.error
       

A = Gamer(0.5, speed=0.00001, error = 0.1, cond_equal = True)
B = Gamer(0.5, speed=0.00001, error = 0.1, cond_equal = False)


#A_knowlage = []
#B_knowlage = []
A_strategy = []
B_strategy = []
A_moves = []
B_moves = []
winners = []
winfunc = []
winfunc2 = []
for i in range(1000000):
    #A_kn = A.knowlage(B,1000)
    #B_kn = B.knowlage(A,1000)
    #A_knowlage.append(A_kn)
    #B_knowlage.append(B_kn)  
    A_strategy.append(A.strategy)  
    B_strategy.append(B.strategy)  

    A_move = A.move()
    B_move = B.move()
    A_moves.append(A.moves())
    B_moves.append(B.moves())

    #print(A_move, B_move, A.strategy, B.strategy)

    A_win = A_move == B_move
    winners.append(A_win)

    A.update_model(A_win, A_move)
    B.update_model(not A_win, B_move)

    winfunc.append(1+2*A.moves()*B.moves() - A.moves() - B.moves())
    winfunc2.append(-2*A.moves()*B.moves() + A.moves() + B.moves())
    
acc = 0
for i in range(len(winners)):
    if winners[i]:
        acc += 1

print(acc/len(winners))

A_win_count = 0
B_win_count = 0
for i in range(len(winners)):
    if winners[i]:
        A_win_count += 1
    else:
        B_win_count += 1

print(A_win_count)
print(B_win_count)

sympy.var("x a b y p")

E = sympy.integrate(-2*(a*sympy.cos(p)+x)*(b*sympy.sin(p)+y)+a*sympy.cos(p)+x+b*sympy.sin(p)+y, (p, 0, 2*sympy.pi))
sympy.pprint(E)

plt.plot(A_strategy, B_strategy, numpy.linspace(0,1,100), numpy.linspace(0,1,100), numpy.linspace(0,1,100), [0.5]*100, [0.5]*100, numpy.linspace(0,1,100))
plt.plot(A_moves, B_moves, numpy.linspace(0,1,100), numpy.linspace(0,1,100), numpy.linspace(0,1,100), [0.5]*100, [0.5]*100, numpy.linspace(0,1,100))
#plt.plot(range(1000000), A_strategy, range(1000000), B_strategy)
#plt.plot(range(1000000), winfunc, range(1000000), winfunc2)
#plt.scatter(range(1000000), winners)
plt.show()