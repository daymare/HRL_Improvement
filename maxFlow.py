"""
    Library for doing max flow problems on TransitionGraphs

    We want to take the transition graph and run max_flow_min_cut on it
    Steps:
        Set up source and sink, source with an edge of weight 1 to each node "left" of the partition and sink with an edge of weight 1 to each node "right" of the partition.
"""
import copy

from transitionGraph import *

"""
    improve a partition on a transition graph by running max-flow min-cut several times
    graph: transition graph
    partition: set of nodes, partition on that graph
"""
def improvePartition(graph, partition):
    # create a copy of the graph and partition to work on.
    currentGraph = copy.deepcopy(graph)
    currentPartition = copy.deepcopy(partition)
    
    # run the ford faulkerson algorithm a set number of times to get the desired graph improvement
    for i in range(4):
        # add source and sink to graph as start and end nodes
        setSourceSink(currentGraph, currentPartition)
        nextPartition = maxFlow(currentPartition)

        currentGraph = copy.deepcopy(graph)
        currentPartition = nextPartition

    return currentPartition


"""
    Add edges to the graph ST
        All nodes within the partition have an edge coming from the source node to the node with capacity 1
        All nodes outside of the partition have an edge going to the sink node with capacity 1
"""
def setSourceSink(graph, partition):
    sourceNode = StateNode()
    sinkNode = StateNode()

    graph.sourceNode = sourceNode
    graph.sinkNode = sinkNode

    for node in graph.nodes:
        # TODO check if this works. iterating through a hash map may produce a tuple, not sure
        if node in partition:
            sourceNode.addEdge(node)
        else:
            node.addEdge(sinkNode)

"""
    Run the ford faulkerson algorithm on a graph with a source and sink node.
    graph: TransitionGraph
    returns: the set of nodes in the resulting max-flow partition
"""
def maxFlow(graph):
    # find the first augmenting path through the list
    path = findAugmentingPath(graph)

    # while we can find another augmenting path in the graph
    while path != None:
    {
        # apply the path flow 
        applyAugmentingPath(graph, path)

        # find another path
        path = findAugmentingPath(graph)
    }

    # do reachability to find the new partition
    # TODO

"""
    Run through the path and apply the maximum flow we can through the path
"""
def applyAugmentingPath(graph, path):
    lastNode = None
    currentNode = path[0]
    maximum = 0

    # find the maximum flow
    for node in path[1:]:
        lastNode = currentNode
        currentNode = node

        # find the edge
        edge = lastNode.edges[currentNode.stateNumber]
        value = edge[1]

        maximum = max(maximum, value) 

    # apply the maximum flow to each node in the graph
    lastNode = None
    currentNode = path[0]

    for node in path[1:]:
        lastNode = currentNode
        currentNode = node

        # reverse the flow of the 


    
"""
    Run depth first search on the graph from source to sink
    returns: 
        a list of the nodes in the path from start to finish order
        None if a path from source to sink does not exist
"""
def findAugmentingPath(graph):
    path = []
    dfs(path, graph.source, graph.sink)

    if len(path) == 0:
        path = None

    return path

def dfs(path, node, goal):
    if node.mark == 1:
        return 0

    node.mark = 1
    path.append(node)

    for edge in node.edges:
        # TODO double check iterating through a hash map does not iterate through the empty crap
        result = dfs(path, edge[0], goal)
        if result == 1:
            return 1

    # could not find the goal node through this node
    path.pop()
    return 0




