# Implémentation de l'algorithme de Kruskal, pour résoudre le problème 
# d'arbre de couverture à cout minimal (MST)

import networkx as nx
import tsplib95

from tsp_lib_graphs_utilities import (tsp_lib_to_networkx, display_graph)
import operator


def Kruskal(G) :
    """
    Implémentation de l'algorithme de Kruskal sur un graphe non orienté (networkx), où chaque arc possède un poids 
    Retourne un arbre
    """
    ## Etape a : Initialisation
    T = nx.Graph()                # T est l'arbre qui sera retourné à la fin ; il est vide pour l'instant
    S = G.edges(data='weight')    # S est un ensemble networkx contenant les tuples avec le premier noeud, le deuxième et le poids de l'arc formé par les deux noeuds
    
    ## Etape b : Tri des arêtes
    # Création d'une liste arc_list, contenant les données de l'ensemble S. La liste est ensuite triée par poids croissants
    arc_list=[]
    for (node_1, node_2, weight) in S:
        arc_list.append((node_1, node_2, weight))
    arc_list.sort(key=operator.itemgetter(2))
    
    linked_nodes = []   # Liste qui contient les noeuds qu'on a déjà ajouté à T,  et qui sont reliés entre eux par un chemin
    compteur = 0
    
    ## Etape c : Construction de l'arbre de couverture T
    while len(T.edges) < len(G.nodes)-1 and compteur < len(S):
        if arc_list[compteur][0] in T.nodes and arc_list[compteur][1] in T.nodes :
                        
            if not nx.has_path(T, arc_list[compteur][0], arc_list[compteur][1]) :             #La fonction has_path renvoit vrai s'il existe un chemin dans le graphe T entre les deux sommets fournis en argument
                ajoute_arc(T, arc_list[compteur][0], arc_list[compteur][1], arc_list[compteur][2])
            
        else:
            if arc_list[compteur][0] in linked_nodes :
                ajoute_noeud(T, arc_list, compteur, 1, linked_nodes)
                
            elif arc_list[compteur][1] in linked_nodes :
                ajoute_noeud(T, arc_list, compteur, 0, linked_nodes)
                
            else :
                ajoute_noeud(T, arc_list, compteur, 0, linked_nodes)
                ajoute_noeud(T, arc_list, compteur, 1, linked_nodes)
            
            ajoute_arc(T, arc_list[compteur][0], arc_list[compteur][1], arc_list[compteur][2])
            
        compteur +=1
        
    return T


def ajoute_arc(graph, noeud_1, noeud_2, poids = 0) :
    """ 
    Fonction qui ajoute un arc au graphe entre le noeud_1 et le noeud_2, avec un poids 
    """
    graph.add_edge(noeud_1, noeud_2)
    graph[noeud_1][noeud_2]['weight'] = poids   
    
    
def ajoute_noeud(graph, liste, compteur, index, linked_nodes) :
    """
    Fonction qui ajoute un noeud contenu dans le tuple liste[compteur], à un certain index
    De plus, elle ajoite ce même noeud à la liste linked_nodes 
    """
    graph.add_node(liste[compteur][index])
    linked_nodes.append(liste[compteur][index])    
    
    
def main() :
    """
    Test de la fonction Kruskal sur des exemples issus de tsplib95 :
    trouver l'arbre de couverture minimum associé à un graphe non orienté
    """   
    
    instance_dir = './tsp_data_files/'
    instance_name = 'gr24' #'gr17', 'eil51', 'bier127', 'ch130'

    # Chargement du problème et des données
    problem = tsplib95.load(instance_dir + instance_name + '.tsp')    
    
    G = tsp_lib_to_networkx(problem)   
    
    # Résolution du problème
    T= Kruskal(G)
    
    # Test pour vérifier que le nombre d'arc dans l'arbre est correct
    assert len(T.edges) + 1 == len(T.nodes)
    
    # Si on a un doute sur la présence d'un cycle, on peut également regarder la commande suivante. Elle renverra 'No cycle found' si elle ne trouve pas de cycle, ce qui permet de vérifier la correction de l'algorithme
    # nx.find_cycle(T)
    
    # Affichage du cout
    S=0
    for (node1,node2,weight) in T.edges(data='weight'):
        S += weight
    
    print("Le cout du problème de MST est : ", S)
    
    display_graph(T)                # Affichage du graphe T


if __name__ == "__main__" :
    # Test de la fonction Kruskal
    main()