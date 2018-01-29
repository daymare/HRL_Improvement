
import networkx as nx


class TransitionGraph:
    MIN_CUTS_PER_IMPROVE = 4

    def __init__(self):
        self.g = nx.Graph()

    def improveAlgorithm(self, partition):
        for i in range(TransitionGraph.MIN_CUTS_PER_IMPROVE):
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

        return partition

    """
        calculate the approximate ncut value of the partion as described in Simsek and Barto (2005)

        ncut(partition):
            A = partition
            B = ~A

            cut(X,Y): sum of weights on edges that originate in X and end in Y
            vol(X) sum of wieghts on all edges that originate in X

            value = (cut(A,B) + cut(B,A)) / (vol(A) + cut(B,A)) + 
                (cut(B,A) + cut(A,B)) / (vol(B) + cut(A,B))

            since our graph is undirected cut(X,Y) == cut(Y,X)

            we can simplify value to:
            value = (2 * cut(A,B) / (vol(A) + cut(A,B))) + (2 * cut(A,B) / vol(B) + cut(A,B))

    """
    def evaluateNCut(self, partition):
        cut_value = self.evaluateCut(partition)
        vol_partition = self.evaluateVolume(partition)

        first_term = 2 * cut_value / (vol_partition[0] + cut_value)
        second_term = 2 * cut_value / (vol_partition[1] + cut_value)

        ncut_value = first_term + second_term
        return ncut_value

    # get the sum of weight on all edges originating in the partition and ending not in the partition
    def evaluateCut(self, partition):
        cut = 0

        for nodeID in partition[0]:
            neighbors = self.g.neighbors(nodeID)

            for neighborID in neighbors:
                if neighborID in partition[1]: 
                    cut += self.g[nodeID][neighborID]['weight']

        return cut

    # get the sum of weight on all edges originating in the partition
    def evaluateVolume(self, partition):
        volume = 0
        volume_i = 0

        for nodeId in partition[0]:
            node = self.g[nodeId]
            for neighbor in node:
                weight = self.getEdgeWeight(nodeId, neighbor)
                volume += weight

        for nodeId in partition[1]:
            node = self.g[nodeId]
            for neighbor in node:
                weight = self.getEdgeWeight(nodeId, neighbor)
                volume_i += weight

        return (volume, volume_i)

    # get a list of all the nodes in the graph
    def getNodes(self):
        return self.g.nodes()
    
    # get the weight of a single edge
    def getEdgeWeight(self, firstState, secondState):
        if self.g.has_edge(firstState, secondState):
            return self.g[firstState][secondState]['weight']
        else:
            return 0

    # get the size of the graph in both number of edges and number of nodes
    def getSize(self):
        nodes = self.g.number_of_nodes()
        edges = self.g.number_of_edges()

        return nodes, edges


    # get the weight of all outgoing edges from a given node
    def getNodeWeight(self, state):
        weight_sum = 0

        for other_state in self.g[state]:
            edge_weight = self.getEdgeWeight(state, other_state)
            weight_sum += edge_weight

        return weight_sum

    
    def addTransition(self, firstState, secondState):
        if self.g.has_edge(firstState, secondState):
            # increment edge
            self.g[firstState][secondState]['weight'] += 1
        else:
            # new edge
            self.g.add_edge(firstState, secondState, weight=1)


