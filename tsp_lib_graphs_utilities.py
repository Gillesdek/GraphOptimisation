"""
Functionalities to load a graph from a tsplib format.

Possible ouputs:
- csv files
- networkx structure

"""

from os import linesep
import networkx as nx
import matplotlib.pyplot as plt

import tsplib95


def get_optimal_solution_value(problem, file_name):
    """
    This function loads (if possible) a solution file
    and returns the optimal value associated to the solution
    """

    solution_file_name = file_name + '.opt.tour'

    import os.path
    # if a solution file exists, load the solution
    if os.path.isfile(solution_file_name) and not problem.is_explicit():
        solution = tsplib95.load(solution_file_name)
        print("Number of solutions ", len(solution.tours))
        optimal_value = problem.trace_tours(solution.tours)[0]

        return optimal_value

    return None

def get_upper_bound_solution_value(problem):
    """
    This function calculates an upper bound for the optimal value
    taking the maximum weight and multiplying it by the number of nodes
    """

    problem_dict = problem.as_name_dict()

    # otherwise an upper bound is calculated using
    # the maximum edge weight (hp. all weights >= 0)
    if problem.is_explicit():
        max_weight = max(max(problem_dict['edge_weights']))
    else:
        max_weight = 0
        all_edges = problem.get_edges()
        for (i, j) in all_edges:
            weight = problem.get_weight(i, j)
            max_weight = max(weight, max_weight)

    max_weight *= problem_dict['dimension']

    return max_weight



def tsp_lib_to_csv(problem, print_on_screen=False):
    """
    Write graph in two csv separated files (nodes and arcs)

    problem contains an TSP instance loaded from tsplib95 format file (using tsplib95 library)
    get nodes and arcs (with their weights)
    save them in two separated csv files
    """

    # Reading nodes and saving them in a csv formated file
    nodes = list(problem.get_nodes())

    if print_on_screen:
        print(nodes)
        print("n")
        for i in nodes:
            print(nodes[i])

    with open("Nodes.csv", "w", newline=linesep) as filehandler:
        filebuffer = ["n"]
        for i in nodes:
            filebuffer.append(str(nodes[i]))
        filehandler.writelines("%s\n" %line for line in filebuffer)


    # Reading arcs (and weights) and saving them in a csv formated file
    arcs = list(problem.get_edges())

    with open("Arcs.csv", "w", newline=linesep) as filehandler:
        if print_on_screen:
            print("n1;n2;weight")
        filebuffer = ["n1;n2;weight"]
        for (i, j) in arcs:
            weight = problem.get_weight(i, j)
            if print_on_screen:
                print(i, ";", j, ";", weight)

            line = "%d;%d;%d" %(i, j, weight)
            filebuffer.append(line)
        filehandler.writelines("%s\n" %line for line in filebuffer)


def tsp_lib_to_networkx(problem):
    """
    Load graph in a networkx Directed Weighted graph

    problem contains an TSP instance loaded from tsplib95 format file (using tsplib95 library)
    get nodes and arcs (with their weights)
    create graph
    """

    #Reading nodes
    nodes = list(problem.get_nodes())

    #Reading arcs (and weights)
    arcs = list(problem.get_edges())

    #storing graph on networkx graph

    graph = nx.DiGraph()

    graph.add_nodes_from(nodes)

    arcs_w = []
    for (i, j) in arcs:
        if i != j: #removing auto-loops
            arcs_w.append((i, j, problem.get_weight(i, j)))

    graph.add_weighted_edges_from(arcs_w)

    return graph

def display_graph(graph):
    """
    Display a graph using spring_layout and node labels
    """

    # position all the nodes
    pos = nx.spring_layout(graph)

    # draw graph element, by element
    # nodes
    nx.draw_networkx_nodes(graph, pos)

    # edges
    nx.draw_networkx_edges(graph, pos)

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=15, font_family='sans-serif')

    plt.show()

def main():
    """
    This code allows to test the functions
    and provide an example of usage
    """

    # Loading a TSP problem
    problem = tsplib95.load('gr24.tsp')

    print(problem.name)
    print(problem.type)
    print(problem.dimension)

    # testing the save-on-file procedure
    tsp_lib_to_csv(problem)

    graph = tsp_lib_to_networkx(problem)


    # position all the nodes
    pos = nx.spring_layout(graph)

    # draw graph element, by element
    # nodes
    nx.draw_networkx_nodes(graph, pos)

    # edges
    nx.draw_networkx_edges(graph, pos)

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=15, font_family='sans-serif')

    plt.show()


if __name__ == "__main__":

    print("Testing functionalities of the current module")
    main()
