from ortools.constraint_solver import pywrapcp

def readData(input_data):

    # Read in the file
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    from collections import namedtuple
    Node = namedtuple("Node", ["name", "neighbours"])
    def create_adjacency_list_lot(node_count, edges):
        adjacency_list = [Node(i, set()) for i in xrange(node_count)]
        for edge in edges:
            adjacency_list[edge[0]].neighbours.add(edge[1])
            adjacency_list[edge[1]].neighbours.add(edge[0])
        return adjacency_list

    return create_adjacency_list_lot(node_count, edges), edges, node_count

'''
Recursive algorithm to find all the maximal cliques in a graph
that include all vertices in R,
     some of the vertices in P,
     none of the vertices in X
'''

def main(input_data):
    adj_list, edges, node_count = readData(input_data) 

    cliques = []
    def BronKerbosch(R, P, X, adj_list):
        if len(P) is 0 and len(X) is 0:
            cliques.append(R)
        for v in P:
            pcopy = P.copy()
            rcopy = R.copy()
            xcopy = X.copy()
            BronKerbosch(rcopy.union(set([v])), pcopy.intersection(adj_list[v].neighbours),
                        xcopy.intersection(adj_list[v].neighbours), adj_list)
            pcopy.remove(v)
            xcopy.add(v)

    BronKerbosch(set(), set([i for i in xrange(node_count-1)]), set(), adj_list)

    for clique in cliques:
        print clique

    print len(cliques)

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        main(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'
