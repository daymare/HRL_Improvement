"""
    Implementation of the skill discovery algorithm from Simsek and Barto(2005)

    Citations:
    Shi, Jianbo, and Jitendra Malik. "Normalized cuts and image segmentation." IEEE Transactions on pattern analysis and machine intelligence 22.8 (2000): 888-905.

    Şimşek, Özgür, Alicia P. Wolfe, and Andrew G. Barto. "Identifying useful subgoals in reinforcement learning by local graph partitioning." Proceedings of the 22nd international conference on Machine learning. ACM, 2005. 
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

    # get the partition based on the second eigenvalue
    partition = getPartition(graph, eigenVectors[1])

    return partition


"""
    get best partition based on the given eigenvector

    graph - graph to partition
    eigenVector - second eigenvector of the system described in Simsek and Barto (2005)
"""
def getPartition(graph, eigenVector):
    pass


"""
    construct the diagonal matrix D as described in Shi and Malik (2000)

    Let N be the number of vertices in the graph
    Let w_i_j be the weight on the edge between vertices i 

    D shall be the diagonal matrix with D(i, i) = sum(j, w_i_j)
    that is each diagonal contains the sum of weight on it's corresponding node's outgoing edges

    If the edge (i, j) does not exist w_i_j will equal 0
"""
def constructD(graph):
    
    pass

"""
    construct the weight matrix as described in Shi and Malik (2000)

    Let N be the number of vertices in the graph
    Let w_i_j be the weight on the edge between vertices i 

    W will be the matrix where W(i, j) = w_i_j
"""
def constructW(graph):
    pass



