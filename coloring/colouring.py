#!/usr/bin/python
# -#- coding: utf-8 -*-


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


class MinGraphColouringDecisionBuilder(pywrapcp.PyDecisionBuilder):

    def __init__(self, v, adjacency_list, edges, s):
        self.__v = v
        self.__nc= [len(x.neighbours) for x in adjacency_list]
        self.node_count = len(v)
        self.colour_count = [self.node_count-1 for _ in xrange(self.node_count)]
        self.last_assigned_colours = []

    ''' 
    Called each time a decision needs to be made
    Choose a value that rules out the fewest v in remaining variables
    (keep a count of each colour per node available, choose the highest count) '''
    def Next(self, s):
        try:
            var = self.NextVar()
            if var:

                min_colour = self.node_count-1
                for c in xrange(self.node_count):
                    if var.Contains(c):
                        if self.colour_count[c] <= min_colour:
                            min_colour = c
                            break

                decision = s.AssignVariableValue(var, min_colour)

                self.colour_count[min_colour] -= 1
                self.last_assigned_colours.append(min_colour)
                return decision
            else:
                c = self.last_assigned_colours.pop()
                self.colour_count[c] += 1
                return None
        except Exception, e:
            print e
    
    '''
    Makes a decision on what variable to update next
    Chooses the variable with minimal remaining v   #s.CHOOSE_MIN_SIZE
    On a tie break choose variable with most constraints  order edges by degree
    '''
    def NextVar(self):
        r = zip(self.__v, self.__nc)
        top_val = max([x.Size() for (x,y) in r if x.Size() > 1])
        res = filter(lambda (x, y): x.Size() == top_val, r)
        if res:
            res.sort(key=lambda x: x[1], reverse=True)
            return res[0][0]
        else:
            return None


def ortools_cp(adjacency_list, edges, node_count):

    # Create the s
    s = pywrapcp.Solver('Solver')

    v = [s.IntVar(0, node_count-1, '%i' % i) for i in range(node_count)]
    for edge in edges:
        s.Add( v[edge[0]] != v[edge[1]])

    #Symmetry breaking
    s.Add(v[0] == 0)
    s.Add(v[1] == 1)

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

    BronKerbosch(set(), set([i for i in xrange(node_count-1)]), set(),
            adjacency_list)

    for clique in cliques:
        i = [v[x] for x in clique]
        s.AllDifferent(i)

    db = MinGraphColouringDecisionBuilder(v, adjacency_list, edges, s)
    db = s.Phase(v,
                      s.CHOOSE_MIN_SIZE,
                      s.ASSIGN_MIN_VALUE)
    solution = s.Assignment()
    solution.Add(v)

    def count_num_colours(values):
        seen = set()
        return len( [x for x in values if x not in seen and not seen.add(x)] )

    num_solutions = 0
    minimising_sol_no = 0
    min_colours = node_count
    min_config = []



    s.NewSearch(db, [])
    while s.NextSolution():
        val = [v[i].Value() for i in xrange(node_count)]
        num_colours = count_num_colours(val)

        if num_colours < min_colours:
            minimising_sol_no = num_solutions
            min_config = val
            min_colours = num_colours 

        if num_solutions > 6000000:
            break

        num_solutions += 1

    s.EndSearch()
    
    return min_colours, min_config 

    '''
    print print "minimum colouring of", min_colours
    print "at sol'n no:", minimising_sol_no
    print min_config

    print "num solutions:", num_solutions
    print "failures:", s.Failures()
    print "branches:", s.Branches()
    print "WallTime:", s.WallTime()
    '''

def main(input_data):

    adjacency_list, edges, node_count = readData(input_data)
    print ortools_cp(adjacency_list, edges, node_count)


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        main(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python s.py ./data/gc_4_1)'

