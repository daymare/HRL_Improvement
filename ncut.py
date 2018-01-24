"""
    Implementation of the skill discovery algorithm from Simsek and Barto(2005)

    Citations:
    Shi, Jianbo, and Jitendra Malik. "Normalized cuts and image segmentation." IEEE Transactions on pattern analysis and machine intelligence 22.8 (2000): 888-905.

    Simsek, Ozgur, Alicia P. Wolfe, and Andrew G. Barto. "Identifying useful subgoals in reinforcement learning by local graph partitioning." Proceedings of the 22nd international conference on Machine learning. ACM, 2005. 
"""

import numpy

"""
    perform the LCut algorithm as described in Simsek and Barto (2005) except instead of outputting the access states we output the partition with the lowest NCut value from a set number of eigenvalues

    Note that the second eigenvector of the system should tell us how to cut our system
    and the second eigenvalue of our system should tell us the approximate minimum LCut value
"""
def LCut(graph):
    D = constructD(graph)
    W = constructW(graph)
    D_inverse = numpy.linalg.inv(D)

    # build the system
    system = (D - W) * D_inverse

    # find the second eigenvector of the system
    eigenValues, eigenVectors = numpy.linalg.eig(system)
    # sort the eigenvalues/eigenvectors to find the second smallest eigenvalue and its corresponding eigenvector
    eigenValues, eigenVectors = sortEigen(eigenValues, eigenVectors)

    # get the partition based on the second eigenvalue
    partition = findBestPartition(graph, eigenVectors[1], 5)

    return partition

"""
    Sort a list of eigenvalues and it's corresponding list of eigenVectors
"""
def sortEigen(eigenValues, eigenVectors):
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]

    return eigenValues, eigenVectors

# map all nodes to an integer between 0 and n
# TODO ensure that this function has the same output between calls
def mapToN(graph):
    list_nodes = graph.getNodes()
    n = len(list_nodes)

    node_map = {}

    i = 0
    for node in list_nodes:
        node_map[i] = node
        i += 1

    return node_map


"""
    get best partition based on the given eigenvector

    Each value in our eigenvector represents one of our nodes. To find which nodes belong in the partition we need to choose a splitting value s.t. values greater than the splitting value belong in one partition, while values below belong in the other.
    To do this we are going to take L evenly spaced cuts across the range of the eigenvector.

    distance between each cut will be range / (L+1)
    
    (| is a cut to evaluate. Each space is a distance D)
    min | | | | | max

    graph - graph to partition
    eigenVector - second eigenvector of the system described in Simsek and Barto (2005)
"""
def findBestPartition(graph, eigen_vector, num_cuts):
    minimum = min(eigen_vector)
    maximum = max(eigen_vector)
    eigen_range = maximum - minimum

    partition_distance = eigen_range / (num_cuts + 1)

    # evaluate first partition
    partition_value = minimum + partition_distance
    partition = getPartition(graph, eigen_vector, partition_value)
    cut_value = graph.evaluateNCut(partition)

    # initialize maximum
    max_partition = partition
    max_cut = cut_value
    
    for i in range(num_cuts-1):
        # get the next value 
        partition_value += partition_distance
        # get partition from current cut
        partition = getPartition(graph, eigen_vector, partition_value)
        # evaluate parition and find current max
        cut_value = graph.evaluateNCut(partition)

        if cut_value > max_cut:
            # set the current values as new maximums
            max_partition = partition
            max_cut = cut_value

    return max_partition

"""
    Get the partition defined by the eigen vector and split value.

    if the value of the index in the eigenvector is less than the split value we add it to the partition, otherwise we add it to the partition complement.
"""
def getPartition(graph, eigen_vector, split_value):
    node_map = mapToN(graph)
    n = len(eigen_vector)

    partition = []
    partition_complement = []

    for i in range(n):
        if eigen_vector[i] < split_value:
            partition.append(node_map[i])
        else:
            partition_complement.append(node_map[i])

    return (partition, partition_complement)


"""
    construct the diagonal matrix D as described in Shi and Malik (2000)

    Let N be the number of vertices in the graph
    Let w_i_j be the weight on the edge between vertices i 

    D shall be the diagonal matrix with D(i, i) = sum(j, w_i_j)
    that is each diagonal contains the sum of weight on it's corresponding node's outgoing edges

    If the edge (i, j) does not exist w_i_j will equal 0
"""
def constructD(graph):
    n, _ = graph.getSize()
    D = numpy.zeros((n,n))

    node_map = mapToN(graph)

    for i in range(n):
        state_node = node_map[i]
        weight = graph.getNodeWeight(state_node)

        D[i,i] = weight

    return D

"""
    construct the weight matrix as described in Shi and Malik (2000)

    Let N be the number of vertices in the graph
    Let w_i_j be the weight on the edge between vertices i 

    W will be the matrix where W(i, j) = w_i_j
"""
def constructW(graph):
    n, _ = graph.getSize()
    W = numpy.zeros((n,n))

    node_map = mapToN(graph)

    for i in range(n):
        for j in range(n):
            firstState = node_map[i]
            secondState = node_map[j]
            W[i, j] = graph.getEdgeWeight(firstState, secondState)

    return W
    




