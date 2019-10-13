
import numpy as np

import gym
from utils import plotLearning

from DeepQNetwork import Agent


if __name__ == '__main__':
    env = gym.make('stuff')
    lr = 0.0005
    n_games = 500
    agent = Agent(gamma = 0.99, epilon = 1.0, lr = lr, input_dims = [8],
            n_actions = 4, mem_wie = 10000000, batch_size = 64)
    
    filename = 'temp.png'
    scores = []
    eps_history = []

    score = 0

    for i in range(n_games):
        done = False
        if i % 10 == 9 and i > 0:
            avg_score = np.mean(scores[max(0, i-10):(i+1)])
            print('bah')

        else:
            print('wah')

        observation = env.reset()
        score = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, 
                                  int(done))
            observation = observation_
            agent.learn()

        scores.append(score)
        eps_history.append(agent.epsilon)

    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
    