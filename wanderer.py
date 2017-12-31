"""
    agent that wanders around randomly to build a transition graph for testing the improve algorithm
"""

import random
import os

import gym

from transitionGraph import *

# constants
episodes = 20
maxTimesteps = 2000

class Wanderer:
    def __init__(self):
        # initialize transition graph
        self.graph = TransitionGraph()

        # make taxi environment
        self.env = gym.make('Taxi-v2')

    def runEpisode(self, maxTimesteps=2000):
        initialState = self.env.reset()

        lastState = None
        currentState = initialState

        for i in range(maxTimesteps):
            # get random action
            action = self.env.action_space.sample()

            # perform action
            nextState, reward, terminal, _ = self.env.step(action)

            # process transition information
            lastState = currentState
            currentState = nextState
            
            # add to transition graph
            self.graph.addTransition(lastState, currentState)

            # render the environment
            os.system('clear')
            self.env.render()


            if terminal == True:
                break


def main():
    agent = Wanderer()

    for i in range(episodes):
        agent.runEpisode(maxTimesteps)


if __name__ == '__main__':
    main()

