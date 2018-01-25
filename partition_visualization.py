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

    WARNING: only human mode is supported currently
"""
def render_partition(partition, width=6, mode='human'):
    # calculate the number of maps we will need to display
    # note that the passenger can be in 5 locations, one for being in the taxi
    # formula is (choose_destination * choose_passenger_location)
    # which equals: (4 choices of destination) * (4 choices of passenger location, 3 + 1 for taxi)
    num_locations = len(LOCS)
    num_maps = ((num_locations * num_locations) - num_locations) * 2

    height = int(math.ceil(num_maps / width)) 

    # create a 2d array of maps, one for each state
    maps = create_map_array(width, height)
    
    # fill in each map with the proper highlights
    fill_maps(maps, width, partition)
    
    # print out the maps to the screen
    print_maps(maps)

# print populated 2d array of maps
def print_maps(maps):
    height = len(maps)
    width = len(maps[0])
    
    for i in range(height):
        map_line = maps[i]
        print_map_line(map_line)

def print_map_line(map_line):
    height = len(map_line[0])
    
    for j in range(height):
        for nmap in map_line:
            # print out a line of a map
            print_map_string(nmap[j])
        print_ns("\n")

"""
    print a line from a map
    print out each character in an array of maps
"""
def print_map_string(map_string):
    for c in map_string:
        if c != '\n':
            print_ns(c)
            

"""
    print with no space

    print function except with no space or newline at the end
"""
def print_ns(obj):
    sys.stdout.write(str(obj))
    sys.stdout.flush()

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

def fill_map(smap, partition, desLoc, passLoc):
    taxirow = 2
    taxicol = 2
    state = encode(taxirow, taxicol, passLoc, desLoc)
    
    # fill in the partition
    highlight_partition(smap, partition, state)

    # fill in the state information over the partition
    highlight_state(smap, state)


def highlight_partition(smap, partition, state):
    # iterate through each taxi posititon in the map and check if it is in the partition
    _, _, passid, destid = decode(state)

    for taxirow in range(5):
        for taxicol in range(5):
            cState = encode(taxirow, taxicol, passid, destid)

            if cState in partition[0]:
                # this location is in the partition
                set_pixel(smap, taxirow, taxicol, 'red', True)
            elif cState in partition[1]:
                # this location is in the partition complement
                set_pixel(smap, taxirow, taxicol, 'blue', True)


def set_pixel(out, row, column, color, highlight=False):
    out[1+row][2*column+1] = utils.colorize(out[1+row][2*column+1], color, highlight=highlight)


def highlight_state(out, state):
    taxirow, taxicol, passidx, destidx = decode(state)

    def ul(x): return "_" if x == " " else x
    
    # highlight taxi
    if passidx < 4:
        # passenger not yet picked up
        # highlight the taxi
        out[1+taxirow][2*taxicol+1] = utils.colorize(out[1+taxirow][2*taxicol+1], 'yellow', highlight=True)

        # passenger
        pi, pj = LOCS[passidx]
        out[1+pi][2*pj+1] = utils.colorize(out[1+pi][2*pj+1], 'blue', bold=True)
    else: 
        # passenger in taxi
        # highlight the passenger-taxi
        out[1+taxirow][2*taxicol+1] = utils.colorize(ul(out[1+taxirow][2*taxicol+1]), 'green', highlight=True)

    # highlight the destination
    di, dj = LOCS[destidx]
    out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')



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





