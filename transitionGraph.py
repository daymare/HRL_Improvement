
import networkx as nx

class TransitionGraph:
    def __init__(self):
        self.g = nx.Graph()
    
    def addTransition(self, firstState, secondState):
        if self.g.has_edge(firstState, secondState):
            # increment edge
            self.g[firstState][secondState]['weight'] += 1
        else:
            # new edge
            self.g.add_edge(firstState, secondState, weight=1)


