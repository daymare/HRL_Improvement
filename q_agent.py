"""
    agent that wanders around randomly to build a transition graph for testing partition algorithms
"""

import random
import os

import gym

from transitionGraph import *
import partition_visualization as pv
import ncut

import numpy as np
import random

# constants
episodes = 5
maxTimesteps = 200
render = False

class QAgent:
    def __init__(self):
        # initialize transition graph
        self.graph = TransitionGraph()

        # make taxi environment
        self.env = gym.make('Taxi-v2')

        # environment variables
        self.numEpisodes = 0
        num_actions = self.num_actions = self.env.action_space.n
        num_states = self.num_states = self.env.observation_space.n

        # q learner variables
        self.q = np.tile(1/float(num_actions), (num_states, num_actions))
        self.epsilon = 0.1
        self.alpha = 0.9
        self.minAlpha = 0.1
        self.annealingSteps = 10000
        self.alphaStepDrop = (self.alpha - self.minAlpha) / self.annealingSteps
        self.gamma = 1

    # run a single episode of wandering
    # store transition information in the transition graph
    def runEpisode(self, maxTimesteps=2000, render=False):
        initialState = self.env.reset()

        lastState = None
        currentState = initialState

        for i in range(maxTimesteps):
            # perform alpha decay
            if self.alpha > self.minAlpha:
                self.alpha -= self.alphaStepDrop

            # get action
            action = self.getAction(currentState)

            # perform action
            nextState, reward, terminal, _ = self.env.step(action)

            # update q function
            self.q[currentState][action] = (1-self.alpha) * self.q[currentState][action] + (self.alpha) * (reward + self.gamma * self.q[nextState].max())

            # process transition information
            lastState = currentState
            currentState = nextState
            
            # add to transition graph
            self.graph.addTransition(lastState, currentState)

            # render the environment
            if render == True:
                os.system('clear')
                self.env.render()

            if terminal == True:
                break

        print "finished episode: {}".format(self.numEpisodes)
        self.numEpisodes += 1

    def getAction(self, state):
        random_num = random.random()
        if random_num < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = self.q[state].argmax()

        return action
        

    # find a partition based on the transition graph
    def findPartition(self):
        partition = ncut.LCut(self.graph)
        return partition
        pv.render_partition(partition)

    def improvePartition(self, partition):
        partition = self.graph.improveAlgorithm(partition)

def main():
    agent = QAgent()

    # populate transition graph
    print "running episodes"
    for i in range(episodes):
        agent.runEpisode(maxTimesteps, render)
    print "finished running episodes"
    
    # find partition
    print "finding partition"
    partition = agent.findPartition()
    print "finished finding partition"

    # render
    os.system('clear')
    pv.render_partition(partition)
    


if __name__ == '__main__':
    main()

