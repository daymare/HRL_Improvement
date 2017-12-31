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


def fill_maps(maps, width, partition):
    num_locs = 4
    map_x = 0
    map_y = 0

    # iterate through each possibility of states
    for destLoc in range(num_locs):
        for passLoc in range(num_locs):
            # skip states where passenger location 
            # is equal to destination location
            if destLoc == passLoc:
                continue

            # fill the next map
            cur_map = maps[map_y][map_x]
            fill_map(cur_map, partition, destLoc, passLoc)

            # increment map 
            map_x += 1
            if map_x == width:
                map_y += 1
                map_x = 0

            # fill the bordering map with the passenger picked up map
            cur_map = maps[map_y][map_x]
            fill_map(cur_map, partition, destLoc, 4)

            # increment map 
            map_x += 1
            if map_x == width:
                map_y += 1
                map_x = 0

def fill_map(map, partition, desLoc, passLoc):
    taxirow = 2
    taxicol = 2

    # fill in the map with the state information
    
    # fill in the partition




"""
    encode a state into an integer
"""
def encode(taxirow, taxicol, passloc, destidx):
    # (5) 5, 5, 4
    i = taxirow
    i *= 5
    i += taxicol
    i *= 5
    i += passloc
    i *= 4
    i += destidx
    return i

"""
    decode a state integer into it's parts
"""
def decode(i):
    out = []
    out.append(i % 4)
    i = i // 4
    out.append(i % 5)
    i = i // 5
    out.append(i % 5)
    i = i // 5
    out.append(i)
    assert 0 <= i < 5
    return reversed(out)



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





