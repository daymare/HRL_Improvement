import numpy as np
import sys
from six import StringIO

from gym import utils


"""
    this file needs to be able to take in a partition on a taxi state graph and output the boundary of the partition as a highlight
"""
MAP = [
    "+---------+",
    "|R: | : :G|",
    "| : : : : |",
    "| : : : : |",
    "| | : | : |",
    "|Y| : |B: |",
    "+---------+",
]

DESC = np.asarray(MAP, dtype='c')

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

def set_pixel(out, row, column, color, highlight=False):
    out[1+row][2*column+1] = utils.colorize(out[1+row][2*column+1], color, highlight=highlight)

def highlight_state(out, state):
    taxirow, taxicol, passidx, destidx = decode(s)
    
    # highlight taxi
    if passidx < 4:
        # highlight the taxi
        out[1+taxirow][2*taxicol+1] = utils.colorize(out[1+taxirow][2*taxicol+1], 'yellow', highlight=True)

        # highlight the passenger
        pi, pj = locs[passidx]
        out[1+pi][2*pj+1] = utils.colorize(out[1+pi][2*pj+1], 'blue', bold=True)
    else: 
        # passenger in taxi
        # highlight the passenger
        out[1+taxirow][2*taxicol+1] = utils.colorize(ul(out[1+taxirow][2*taxicol+1]), 'green', highlight=True)

    # highlight the destination
    di, dj = locs[destidx]
    out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')
    outfile.write("\n".join(["".join(row) for row in out])+"\n")



def highlight_partition(out, partition):
    
    pass



"""
    append maps by width

    append a number of maps width wise

    global_map: global map to append maps to should be in the form of List(List(character)) (IE a 2 dimensional list of characters kindof)
    num_maps: the number of maps to append width wise
"""
def append_maps_by_width(global_map, num_maps):
    
    # append a line with the appropriate number of maps
    pass


def create_global_map(width, height):
    global_map = []

    width = len(DESC[0])
    height = len(DESC)

    append_maps_by_width(num_maps)
    # append each line of the local map x times
    for current_y in range(height):
        map_line = []
        for current_x in range(x):
            for j in range(width-1):
                map_line.append(DESC[current_y][current_x])
        
        pass
        
    # do this y times
    pass


def render_board(partition, passenger_pos):
    pass

"""
    highlight all states that are in a partition and return

    print out 12 copies of the board representing each position of the passenger and destination
"""
def render_partition(partition, mode='human'):
    outfile = StringIO() if mode == 'ansi' else sys.stdout

    out = DESC.copy().tolist()
    out = [[c.decode('utf-8') for c in line] for line in out]

    def ul(x): return "_" if x == " " else x

    # highlight the partition
    highlight_partition(out, partition)
    
    # highlight the state
    if state != None:
        highlight_state(out, state)


    # No need to return anything for human
    if mode != 'human':
        return outfile
