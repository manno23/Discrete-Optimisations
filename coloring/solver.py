#!/usr/bin/python
# -*- coding: utf-8 -*-


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    adjacency_list = create_adjacency_list_lot(node_count, edges)

    # return output_data
    # return graph_coloring_non_optimal(create_adjacency_list_lot(node_count, edges))
    import colouring 
    colour_count, solution = colour_count, solution = colouring.ortools_cp(adjacency_list, edges,
            node_count)


    # prepare the solution in the specified output format
    output_data = str(colour_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    
    return output_data


from collections import namedtuple
Node = namedtuple("Node", ["name", "neighbours"])
''' List of tuples
Can be sorted 
Cannot select by name unless the list index
aligns with the name tuple element '''
def create_adjacency_list_lot(node_count, edges):
    adjacency_list = [Node(i, set()) for i in xrange(node_count)]
    for edge in edges:
        adjacency_list[edge[0]].neighbours.add(edge[1])
        adjacency_list[edge[1]].neighbours.add(edge[0])
    return adjacency_list


''' Dict of sets
Useful for selecting a node 
Cannot be sorted '''
def create_adjacency_list_dos(node_count, edges):
    adjacency_list = {}
    for edge in edges:
        if not adjacency_list.has_key(edge[0]):
            adjacency_list[edge[0]] = set()
        if not adjacency_list.has_key(edge[1]):
            adjacency_list[edge[1]] = set()
        adjacency_list[edge[0]].add(edge[1])
        adjacency_list[edge[1]].add(edge[0])
    return adjacency_list

''' List of sets
Not used for sorting, because the node is represented
by it's position in the list 
Will usually use a dict of sets over this'''
def create_adjacency_list_los(node_count, edges):
    adjacency_list = [set() for i in xrange(node_count)]
    for edge in edges:
        adjacency_list[edge[0]].add(edge[1])
        adjacency_list[edge[1]].add(edge[0])
    return adjacency_list


''' Greedy Colouring
Returns the minimum number of colours needed to colour every
vertex neighbours a different colour

Orders the nodes from high degree to low,
tries each colour in order until no neighbours are the same,
then assigns the node that colour.

Produces, sub-optimal results each time
Ordering produces SLIGHTLY better results each time
Is relatively fast for all inputs: O(n^3)
        
'''
def graph_coloring_non_optimal(adjacency_list):

    Colour = namedtuple("Colour", ['value', 'members'])
    colour_list = [ Colour(i, set()) for i in xrange(len(adjacency_list)) ]
    adjacency_list.sort(key=lambda node: len(node[1]), reverse=True)
    number_of_colours_used = 0
    for node in adjacency_list:
        for colour in colour_list:
            colour_chosen = True
            for neighbour in node[1]:
                if neighbour in colour.members:
                    colour_chosen = False
            if colour_chosen:
                colour.members.add(node[0])
                if colour.value > number_of_colours_used:
                    number_of_colours_used = colour.value 
                break

    node_count = 0
    for colour in colour_list:
        for member in colour.members:
            node_count = node_count + 1
                    
    solution = []
    for i in xrange(node_count):
        for colour in colour_list:
            if i in colour[1]:
                solution.append(colour[0])
                break

    output_data = str(number_of_colours_used + 1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data

def brute_force(node_count, edges):
    
    from collections import namedtuple
    Node = namedtuple("Node", ["name", "neighbours", "selected_colour", "colours"])
    colour_set = set([i for i in xrange(node_count)])
    G = [Node(i, set(), 0, colour_set) for i in xrange(node_count)]
    for edge in edges:
        G[edge[0]].neighbours.add(edge[1])
        G[edge[1]].neighbours.add(edge[0])

    P, Q = dict(), set() # P:predecessor, Q:frontier
    start = 0
    G[start].colours = set()  # Choose a colour for the first node
    G[start].selected_colour = 0
    P[start] = None
    Q.add(start)
    while Q:
        u =  Q.pop()
        for neighbour in G[u].neighbours.difference(P):
            G[neighbour].colours.remove(u.colours)
            Q.add(neighbour)
            P[neighbour] = u



import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

