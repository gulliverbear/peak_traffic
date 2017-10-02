#!/usr/bin/python
'''
7/7/14
peak traffic
'''
import sys
import itertools
verbose = False

def get_key(user1, user2):
    '''
    converts two users into a tuple, sorted alphabetically
    '''
    if user1 <= user2:
        return (user1, user2)
    return (user2, user1)
    
def remove_node(d, node):
    '''
    a dictionary where the values are sets of connected nodes, key is a node
    remove the node from all values and as a key, return new dictionary
    '''
    temp_d = dict(d)
    if node in temp_d:
        del temp_d[node]
    for key in temp_d:
        if node in temp_d[key]:
            temp_d[key].remove(node)
    return temp_d
    
def is_clique(d, t):
    '''
    given a dictionary of connections and a tuple of 3 nodes
    checks if they form a clique
    '''
    temp_d = dict(d) # just good practice to make a local copy
    node1, node2, node3 = t
    if node2 not in temp_d[node1] or node3 not in temp_d[node1]:
        return False
    if node2 not in temp_d[node3]:
        return False
    return True
    
def check_merge_cliques(t1, t2, d):
    '''
    given 2 cliques and a connections dictionary
    returns True if can merge the cliques
    '''
    temp_d = dict(d)
    for node1 in t1:
        for node2 in t2:
            if node2 not in temp_d[node1] and node1 != node2:
                return False
    return True
    
def check_subset(t1, t2):
    '''
    given 2 tuples checks if the smaller tuple is a subet of the larger
    '''
    s1 = set(t1)
    s2 = set(t2)
    s3 = s1 & s2
    return len(s1 & s2) == min(len(s1), len(s2))
    
d = {}
connected = {}

with open(sys.argv[1]) as FH:
    for line in FH:
        line = line.rstrip()
        #date, user1, user2 = line.split('    ')
        date, user1, user2 = line.split('\t')
        #user1 = user1.split('@')[0]
        #user2 = user2.split('@')[0]
        key = get_key(user1, user2)

        pos = key.index(user1) # pos in tuple of who sent message
        if key not in d:
            d[key] = [0, 0]
            d[key][pos] = 1
        else:
            d[key][pos] = 1
            if sum(d[key]) == 2:
                if key[0] not in connected:
                    connected[key[0]] = set()
                connected[key[0]].add(key[1])
                if key[1] not in connected:
                    connected[key[1]] = set()
                connected[key[1]].add(key[0])

# only nodes that appear twice in connected can be a clique
while True:
    starting_nodes = connected.keys()
    nodes_to_remove = []
    for node in starting_nodes:
        if len(connected[node]) < 2:
            nodes_to_remove.append(node)
    for node in nodes_to_remove:
        connected = remove_node(connected, node)
    final_nodes = connected.keys()
    if len(starting_nodes) == len(final_nodes):
        break
if verbose:
    print 'Number of connected nodes found = {}'.format(len(connected))
     
# find all cliques of size 3        
cliques = set()
for node in connected:
    children_nodes = connected[node] # this is a set of nodes
    combinations = itertools.combinations(children_nodes, 2) # tuples of 2 nodes
    for combo in combinations:
        temp_clique = combo + (node,)
        temp_clique = sorted(temp_clique)
        temp_clique = tuple(temp_clique)
        if temp_clique not in cliques:
            if is_clique(connected, temp_clique):
                cliques.add(temp_clique)
if verbose:
    print 'number of cliques before merging = {}'.format(len(cliques))

# merge the cliques
all_cliques = set(cliques)
while True:
    new_cliques = set()
    clique_pairs = itertools.combinations(cliques, 2)
    merge_flag = 0
    for pair in clique_pairs:
        clique1, clique2 = pair
        if check_merge_cliques(clique1, clique2, connected):
            temp_merged_clique = clique1 + clique2
            temp_merged_clique = set(temp_merged_clique) # get rid of duplicate nodes
            temp_merged_clique = tuple(temp_merged_clique)
            temp_merged_clique = sorted(temp_merged_clique) # sorting creates a list
            temp_merged_clique = tuple(temp_merged_clique)
            new_cliques.add(temp_merged_clique)
            all_cliques.add(temp_merged_clique)
            merge_flag = 1
    if merge_flag == 0:
        break
    if verbose:
        print 'Merged {} cliques'.format(len(new_cliques))
    cliques = set(new_cliques)
cliques = set(all_cliques)  

if verbose:
    print 'The size of all the cliques after merging is {}'.format(len(cliques))

# remove cliques that are subsets
cliques_to_remove = set()
clique_list = list(cliques)
for i in xrange(len(clique_list)-1):
    clique1 = clique_list[i]
    for j in xrange(i+1,len(clique_list)):
        clique2 = clique_list[j]
        if check_subset(clique1, clique2):
            if len(clique1) < len(clique2):
                cliques_to_remove.add(clique1)
            elif len(clique2) < len(clique1):
                cliques_to_remove.add(clique2)
if verbose:
    print 'The number of cliques to remove is {}'.format(len(cliques_to_remove))

for i in cliques_to_remove:
    #if i not in cliques:
    #    print '{} not in cliques'.format(i)
    cliques.remove(i)
    
cliques = sorted(cliques)
for i in cliques:
    print ', '.join(i)
print

# convert list of tuples into a list of nodes
# another way to do this is go through connected keys and see if len(values) > 1
#nodes = [i[0] for i in recipricol_connected] + [i[1] for i in recipricol_connected]
#nodes = [i for i in nodes if nodes.count(i) > 1]
#nodes = set(nodes)
#print connected

#for node in nodes:
         
        
        
