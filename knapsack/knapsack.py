import functools

"""
Recursive
Knapsack algorithm for determining the optimal value from the set of possible 
values
Included a memoizing decorator to store solved values, this is more space efficient than
using a full table
"""

K = 10
weight = [3,4,5]
value = [5,6,3]
num_items = len(weight)



def memo(obj):
	cache = obj.cache = {}
	kwargs = obj(**kwargs)
	@functools.wraps(obj)
	def memoizer(*args):
		if args not in cache:
			cache[args] = obj(*args)
		return cache[args]
	return memoizer

@memo
def r_knap(k, j):
	if j is 0:
		return 0
	elif (weight[j] <= k):
		return max(r_knap(k, j-1), value[j] + r_knap(k - weight[j], j-1))
	else:
		return r_knap(k, j-1)

print r_knap(K, num_items-1)

"""
Iterative
0-1 Knapsack algorithm
No need to recurse from top-down
Create a table from the bottom up, deciding whether to choose an item, 
stopping from recomputing the same operation
"""

print ''

def IO(k):
	values = []
	# Initialise the table
	for j in range(k+1):
		values.append([0, 0, 0, 0])

	for item in range(num_items):
		for k in range(K):
			if weight[item] <= k:
				values[k][item+1] = max(values[k-weight[item]][item] + value[item], values[k][item])
			else:
				values[k][item+1] = values[k][item]

	for j in range(k+1):
		print values[j]

IO(K)
