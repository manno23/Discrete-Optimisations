#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from heapq import heappop, heappush

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):

    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    if item_count < 400:
        value, taken = iterative_knapsack(capacity, items)
    else:
        value, taken = bnb_knapsack(capacity, items)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def greedy_knapsack(capacity, items):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

def iterative_knapsack(capacity, items):
    item_count = len(items)
    values = [[0]*(item_count+1) for _ in range(capacity+1)]
    chosen = [0]*item_count

    for item in items:
        i = item.index+1
        for k in range(1, capacity+1):
            if item.weight <= k:
                values[k][i] = max( values[k-item.weight][i-1] + item.value, values[k][i-1] )
            else:
                values[k][i] = values[k][i-1]

    optimum_value = values[capacity][item_count]

    column, j = item_count, capacity
    for i in range(column, 0, -1):
        if values[j][i] is not values[j][i-1]:
            chosen[i-1] = 1
            j = j - items[i-1].weight 


    return optimum_value, chosen

def modified_iterative_knapsack(capacity, items):
    item_count = len(items)
    values = [[0]*(capacity+1) for _ in range(2)]
    chosen = [0]*item_count

    for item in items:
        values[0], values[1] = values[1], values[0]
        for k in range(1, capacity+1):
            if item.weight <= k:
                values[1][k] = max( values[0][k-item.weight] + item.value,
                                    values[0][k] )
            else:
                values[1][k] = values[0][k]

    optimum_value = values[1][capacity]
    return optimum_value, chosen

def bnb_knapsack(capacity, items):

    def estimate(sum_values, sum_weight, item_no):
        if item_no == len(items):
            return sum_values
        remaining_s_items = items[item_no:]
        for item in remaining_s_items:
            if sum_weight + float(item.weight) > capacity: break
            sum_weight += float(item.weight)
            sum_values += float(item.value)
        # returns the greedy value estimate
        return sum_values + ( float(item.value) / float(item.weight) ) * ( float(capacity) - sum_weight )

    items.sort(key=lambda item: float(item.value) / float(item.weight), reverse=True)
    item_count = len(items)

    best_result = 0
    chosen = [0 for _ in xrange(item_count)]

    initial_node = (0, 0, 0, [0 for _ in xrange(item_count)])
                    
    branch = [(-estimate(0, 0, 0), initial_node)]
    while branch:

        current = heappop(branch)
        current_estimate = current[0]
        value_sum = current[1][0]
        weight_sum = current[1][1]
        child_item_no = current[1][2] # the index number of items we will branch on
        branch_items = current[1][3][:]
        branch_items_added = current[1][3][:]

        if weight_sum <= capacity:
            if child_item_no < item_count:
                if -best_result >= current_estimate:
                    item = items[child_item_no]
                    # Not including the item
                    heappush(branch, (-estimate(value_sum, weight_sum, child_item_no+1),
                                      (value_sum, weight_sum, child_item_no+1,
                                          branch_items)
                                     ))
                    # Including the item
                    branch_items_added[child_item_no] = 1
                    heappush(branch, (-estimate(value_sum + item.value, weight_sum + item.weight, child_item_no+1),
                                      (value_sum + item.value, weight_sum +
                                          item.weight, child_item_no+1,
                                          branch_items_added)
                                     ))
            else:
                if best_result < value_sum:
                    best_result = value_sum
                    chosen = branch_items[:]

    reordered = [0 for _ in xrange(item_count)]
    for i in xrange(item_count):
        if chosen[i] is 1:
            reordered[items[i].index] = 1

    return best_result, reordered 


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'
