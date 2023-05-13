#!/usr/bin/env python3

import gym
from time import sleep

# Создаем thr env
env = gym.make("Taxi-v3", render_mode="human").env

env.s = 328


# Устанавливаем в ноль количество итераций, штрафы и вознаграждение,
epochs = 0
penalties, reward = 0, 0

frames = []

done = False

env.reset()
while not done:
    action = env.action_space.sample()
    state, reward, done, info, _ = env.step(action)

    if reward == -10:
        penalties += 1

    # Каждый отображенный кадр помещаем в словарь для анимации
    frames.append({
        'frame': env.render(),
        'state': state,
        'action': action,
        'reward': reward
    }
    )

    epochs += 1

print("Timesteps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))

# Выводим все возможные действия, состояния, вознаграждения
def frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'].getvalue())
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)
        
frames(frames)