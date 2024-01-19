"""
This module contains algorithms to solve the minimum spanning tree problem
"""
import tsplib95
import networkx as nx

from tsp_lib_graphs_utilities import (tsp_lib_to_networkx, display_graph)

def kruskal(graph, print_on_screen=False):
    """
    Naive Kruskal implementation on a undirected weighted graph (networkx)

    returns a new graph (MST)
    """

    arc_list = []
    for (node_1, node_2, weight) in graph.edges(data='weight'):
        arc_list.append((node_1, node_2, weight))

    import operator

    arc_list.sort(key=operator.itemgetter(2))

    # creating a graph only using the nodes
    tree = nx.create_empty_copy(graph)

    if print_on_screen:
        print(tree.nodes())

    #until all nodes are connected
    #i.e. until n-1 arcs are added
    count = 0
    #tree_edges = []
    cost = 0

    for (i, j, weight) in arc_list:
        if count < nx.number_of_nodes(tree):
            # check if arcs form loop
            add = False
            if not (nx.has_path(tree, i, j) or nx.has_path(tree, j, i)):
                add = True
            if add:
                cost = cost + weight
                edge = [(i, j, weight)]
                tree.add_weighted_edges_from(edge)
                count = count + 1
        else:
            break

    if print_on_screen:
        print(nx.number_of_edges(tree), cost)
    
    return (tree, cost)

def main():
    """
    Testing Kruskal to examples of tsplib95:

    - find the minimum spanning tree (mst) associated to the unoriented graph

    """

    instance_dir = './tsp_data_files/'
    instance_name = 'gr24' #'gr17', 'eil51', 'bier127', 'ch130'

    # Loading a TSP problem
    problem = tsplib95.load(instance_dir + instance_name + '.tsp')

    if not problem.is_symmetric():
        print("Chosen data file does not correspond to a symmetric graph!")
        return None

    print(problem.name)
    print(problem.type)
    print(problem.dimension)

    orig_graph = tsp_lib_to_networkx(problem)

    ind_graph = orig_graph.to_undirected()

    (tree, value) = kruskal(ind_graph)

    print("MST with cost ", value)

    display_graph(tree)

if __name__ == "__main__":

    print("Testing functionalities of the current module")
    main()
