import numpy as np
import sys
from gym import utils

import math

"""
    This file is for visualization techniques on our partitions so we can see how well the partition algorithm is doing.

    The main thing here is render_partition, which will visualize a partition on the whole state space.
"""

# global map for creating the displays
MAP = [
    "+---------+",
    "|R: | : :G|",
    "| : : : : |",
    "| : : : : |",
    "| | : | : |",
    "|Y| : |B: |",
    "+---------+",
]
NP_MAP = np.asarray(MAP, dtype='c')

LOCS = [(0,0), (0,4), (4,0), (4,3)]

"""
    render patition,

    display a rectangular grid of maps each highlighted with the parititon
"""
def render_partition(partition, width=3, mode='human'):
    # calculate the number of maps we will need to display
    # note that the passenger can be in 5 locations, one for being in the taxi
    # formula is (choose_destination * choose_passenger_location)
    # which equals: (4 choices of destination) * (4 choices of passenger location, 3 + 1 for taxi)
    num_locations = len(LOCS)
    num_maps = num_locations * num_locations

    height = math.ceil(num_maps / width)

    # create a 2d array of maps, one for each state
    maps = create_map_array(width, height)
    
    # fill in each map with the proper highlights
    fill_maps(maps, partition)


def fill_maps(maps, partition):
    pass


"""
    create map array

    create an array of maps of the specified width and height
"""
def create_map_array(width, height):
    map_array = []

    for j in range(height):
        map_line = []
        for i in range(width):
            map_line.append(NP_MAP.copy().tolist())
        map_array.append(map_line)

    return map_array





