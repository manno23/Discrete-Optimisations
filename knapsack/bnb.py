from collections import namedtuple
from heapq import heappush, heappop
from itertools import count

capacity = 10
Item = namedtuple("Item", ['index', 'value', 'weight'])
items = [Item(0, 45, 5),
         Item(1, 48, 8),
         Item(2, 35, 3)]

best_result = 0

'''
Take the unit value of each item to aid in determining an estimate
(this is a decent heuristic)
for the branch and bounding

First create the heuristic, by taking a greedy appraoch to most value/weight
through dfs stop search at point in which conservative estimate (the best value
we've found so far) is bigger

Perform the branch and bound on a binary decision tree
A depth first creation of the tree, first choice is to include
tree is a list of node tuples, each node representing space left and
current optimistic estimate
if the relaxed(optimistic) solution along any branch is worse than our
best case so far, bound that branch

pop and push from the items, an empty item list signifys this is a leaf

'''
# node tuple = (total_value, total_weight, estimate, item_no_decision)
items = [Item(1,8,4),
         Item(2,10,5),
         Item(3,15,8),
         Item(4,4,3)]
tree_depth = len(items)


    

def bnb_knapsack(items, capacity):

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

    best_result = 0
    initial_node = (0, 0, 0)
    branch = [(-estimate(0, 0, 0), initial_node)]
    items.sort(key=lambda item: float(item.value) / float(item.weight), reverse=True)
    item_count = len(items)

    while branch:

        current = heappop(branch)
        print current
        current_estimate = current[0]
        value_sum = current[1][0]
        weight_sum = current[1][1]
        child_item_no = current[1][2] # the index number of items we will branch on

        if weight_sum <= capacity:
            if child_item_no < item_count:
                if -best_result >= current_estimate:
                    item = items[child_item_no]
                    # Not including the item
                    heappush(branch, (-estimate(value_sum, weight_sum, child_item_no+1),
                                      (value_sum, weight_sum, child_item_no+1)
                                     ))
                    # Including the item
                    heappush(branch, (-estimate(value_sum + item.value, weight_sum + item.weight, child_item_no+1),
                                      (value_sum + item.value, weight_sum +
                                          item.weight, child_item_no+1)
                                     ))
                else:
                    print 'bounded: best_result: ', best_result, ' > ', current_estimate
                    print ''
            else:
                print 'is a leaf'
                if best_result < value_sum:
                    print 'best result set: ', value_sum
                    best_result = value_sum
                print ''
        else:
            print 'overweight: ', weight_sum, ' >= ', capacity
            print ''

    return best_result

df_traversal()



def bnb_knapsack(items, capacity):

    # Take every element of the sorted list and add them from the beginning
    # such that the weight is equal to capacity
    num_items = len(items)
    items.sort(key = lambda item: float(item.value) / float(item.weight),
            reverse=True)


    '''
        bound 
    This function runs a greedy estimation through a linear relaxation of
    the 0-1 constraint.
    It is recomputed at each node
    @returns this greedy estimation

    '''
    def bound(sum_weight, sum_values, item_no):
        if item_no == num_items:
            return sum_values
        remaining_items = items[item_no:]
        for item in remaining_items:
            if sum_weight + float(item.weight) > capacity: break
            sum_weight += float(item.weight)
            sum_values += float(item.value)
        # returns the greedy value estimate
        return sum_values + ( float(item.value) / float(item.weight) ) * ( float(capacity) - sum_weight )
    

    '''
        node
    A generator function that yields a node plus the estimation at each call
    it branches by choosing a child, first without taking the item, then with
    It yields(continues branching) only when the branch looks promising, 
        ie. the optimistic estimate is better than our best guess

    '''
    def node(sum_weight, sum_values, item_no):
        global best_result

        if sum_weight > capacity: return
        best_result = max(best_result, sum_values)
        if item_no == num_items: return
        item = items[item_no]     # items sorted high to low
        children = [(sum_weight, sum_values),
                    (sum_weight + item.weight, sum_values + item.value)]
        for sum_weight, sum_values in children:
            b = bound(float(sum_weight), float(sum_values), item_no+1)
            if b > best_result:
                print b, sum_weight, sum_values, item_no+1
                yield b, node(sum_weight, sum_values, item_no+1)
            else:
                print 'bounded'

    num = count()
    decision_tree = [(0, next(num), node(0, 0, 0))]
    while decision_tree:
        _, _, r = heappop(decision_tree)
        print 'begin processing node children'
        for estimate, child in r:
            print estimate
            heappush(decision_tree, (estimate, next(num), child))

    return best_result
    

print bnb_knapsack(items, capacity)
