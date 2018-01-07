
import networkx as nx


class TransitionGraph:
    MIN_CUTS_PER_IMPROVE = 4

    def __init__(self):
        self.g = nx.Graph()

    def improveAlgorithm(self, partition):
        for i in range(MIN_CUTS_PER_IMPROVE):
            # set up source and sink
            for node in self.g.nodes_iter(data=False):
                if node == 'source' or node == 'sink':
                    continue
                elif node in partition:
                    self.g.add_edge('source', node, weight=1)
                else:
                    self.g.add_edge(node, 'sink', weight=1)
            
            # run max_flow_min_cut
            cut_value, new_partition = nx.minimum_cut(self.g, 'source', 'sink')

            # update the partition
            partition = new_partition[0]

            # remove source and sink nodes
            self.g.remove_node('source')
            self.g.remove_node('sink')
    
    # get the weight of a single edge
    def getEdgeWeight(self, firstState, secondState):
        return self.g[firstState]['weight']

    # get the size of the graph in both number of edges and number of nodes
    def getSize(self):
        nodes = self.graph.number_of_nodes()
        edges = self.graph.number_of_edges()

    # get the weight of all outgoing edges from a given node
    def getNodeWeight(self, state):
        weight_sum = 0

        for edge in self.g[firstState]:
            weight_sum += edge['weight']

        return weight_sum

    
    def addTransition(self, firstState, secondState):
        if self.g.has_edge(firstState, secondState):
            # increment edge
            self.g[firstState][secondState]['weight'] += 1
        else:
            # new edge
            self.g.add_edge(firstState, secondState, weight=1)


