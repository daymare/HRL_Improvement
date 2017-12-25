"""
    agent that wanders around randomly to build a transition graph for testing the improve algorithm
"""

import random

import gym

from transitionGraph import *

class Wanderer:
    def __init__(self):
        # initialize transition graph
        self.graph = TransitionGraph()

        # make taxi environment
        self.env = gym.make('Taxi-v2')
        self.numActions = env.actionSpace.n

    def runEpisode(self, maxTimesteps=2000):
        initialState = self.env.reset()

        lastState = None
        currentState = initialState

        for i in range(maxTimesteps):
            # get random action
            action = random.randint(self.numActions)

            # perform action
            nextState, reward, terminal, _ = self.env.step(action)

            # process transition information
            lastState = currentState
            currentState = nextState
            
            # add to transition graph
            startingNode = self.graph.getNode(lastState)
            endingNode = self.graph.getNode(currentState)
            startingNode.addToEdge(endingNode, 1)

            if terminal == True:
                break


def main():
    pass


if __name__ == 'main':
        pass

