"""
    agent that wanders around randomly to build a transition graph for testing partition algorithms
"""

import random
import os

import gym

from transitionGraph import *
import partition_visualization as pv
import ncut

# constants
episodes = 1
maxTimesteps = 200
render = False

class Wanderer:
    def __init__(self):
        # initialize transition graph
        self.graph = TransitionGraph()

        # make taxi environment
        self.env = gym.make('Taxi-v2')

        self.numEpisodes = 0

    # run a single episode of wandering
    # store transition information in the transition graph
    def runEpisode(self, maxTimesteps=2000, render=False):
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
            if render == True:
                os.system('clear')
                self.env.render()

            if terminal == True:
                break

        print "finished episode: {}".format(self.numEpisodes)
        self.numEpisodes += 1

    # find a partition based on the transition graph
    def findPartition(self):
        partition = ncut.LCut(self.graph)
        return partition


def main():
    agent = Wanderer()

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

