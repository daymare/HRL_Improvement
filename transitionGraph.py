
"""
    State Node class
    Represents a single state in a transition graph
"""
class StateNode(object):
    def __init__(self, stateNumber):
        # list of edges {int, id's: (StateNode nodes, num_transitions)}
        self.edges = {}
        # list of reverse edges, edges that come into this node (not traversable)
        self.stateNumber = stateNumber
        self.mark = 0

    def addEdge(self, rNode, value=1):
        rStateNumber = rNode.stateNumber
        self.edges[rStateNumber] = (rNode, value)

    def addToEdge(self, otherNode, value):
        # check if edge exists

        if value < 0 and -value > 


    def subtractFromEdge(self, otherNode, value):
        pass

    def reverseFlow(self, otherNode, amount):
        # get edge to reduce
        edge = self.edges[otherNode.stateNumber]
        assert edge[1] >= amount

        # reduce the edge
        edge[1] -= amount

        # check if we need to remove the edge now
        if edge[1] == 0:
            # remove the edge

        # add flow to the reverse edge


        

class TransitionGraph(object):
    def __init__(self):
        self.nodes = {}
        self.sourceNode = None
        self.sinkNode = None

    def addNode(self, nodeId):
        self.nodes[node] = StateNode(nodeId)


    """
        increment the value of an edge in the transition graph, indicating that the agent has taken this transition
        state: integer, id of the state the agent started in
        rState: integer, id of the state the agent ended up in
        returns: None
    """
    def incrementEdge(self, state, rState):
        # check both the start and end node exist
        if state not in self.nodes:
            self.addNode(state)

        if state not in self.nodes:
            self.addNode(rState)
            
        # check if the edge exists
        node = self.nodes[state]
        rNode = self.nodes[rState]

        if rState not in node.edges:
            node.addEdge(rNode)
        else:
            # increment the count of the edge
            edge = edges[rState]
            edge[1] += 1
            # TODO potential bug, edge may not get incremented by this, should work.



