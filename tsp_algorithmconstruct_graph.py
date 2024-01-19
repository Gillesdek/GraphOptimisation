import tsplib95
import networkx as nx
from mst_algorithms import kruskal
from tsp_lib_graphs_utilities import display_graph,tsp_lib_to_networkx


def tsp(graph):
    """ 
    Implementation d'un algorithme heuristique pour la résolution du problème du voyage de commerce ( TSP problem )
    Entrée : 
    - Graphe orienté (networkx)
    
    Sortie : 
    le truple (solution, cost, V) où :
    - solution est le graphe (networkx) trouvé
    - cost est le coût total du parcours de ce graphe
    - V est la liste des noeuds parcourus 
    
    """
    
    arc_list = dict()
    for (i, j, weight) in graph.edges(data='weight'):
        arc_list[str(i) + str(j)] = weight    
    
    
    ## Étape 1 : On transforme le graphe de base en graphe non orienté
    ind_graph = graph.to_undirected() 
    
    
    ## Étape 2 : On lui applique l'algorithme de Kruskal résolvant le MST
    (mst_graph,value) = kruskal(ind_graph)
    
    
    ## Étape 3 : On retransforme le graphe en graphe orienté symétrique
    dir_mst_graph = mst_graph.to_directed()
    
    
    ## Étape 4 : on utilise la stratégie "shortcut" pour créer un cycle
    solution = nx.DiGraph() 
    V = [] 
    O = [list(graph.nodes)[0]] 
    compteur = 0
    cost = 0
    
    while len(O) != 0 : # Si O est vide alors tous les noeuds ont été visités
        
        node = O[-1] 
        
        ## Construction de la solution sous forme de liste de noeuds
        O.remove(node)
        V.append(node)
        
        for neigbour in dir_mst_graph.neighbors(node) :
            if neigbour not in V and neigbour not in O :
                O += [neigbour]        
        
        ## Construction au fur et à mesure de la solution en graphe et calcul du coût
        if compteur >= 1 :
            
            i = V[compteur-1]
            j = V[compteur]
            weight = arc_list[str(i) + str(j)]
            edge = [(i,j,weight)]
            solution.add_weighted_edges_from(edge)
            cost += weight
        
        compteur += 1
        
    ## On crée un arc entre le dernier et le premier noeud pour finir le cycle   
    i = V[-1]
    j = V[0]
    weight = arc_list[str(i) + str(j)]
    edge = [(i,j,weight)]    
    
    solution.add_weighted_edges_from(edge) 
    cost += weight
  
    return (solution, cost, V)


            
            
def main():
    """
    Test de l'algorithme de TSP sur des exemples de tsplib95:
    trouver le chemin minimum qui parcourt tous les noeuds et revient à son point de départ
    """    
    
    instance_dir = "./tsp_data_files/"
    instance_name = 'gr24' #'eil51', 'bier127', 'ch130'
     

    # Chargement d'un problème de TSP
    problem = tsplib95.load(instance_dir + instance_name + '.tsp')
    

    if not problem.is_symmetric():
        print("Chosen data file does not correspond to a symmetric graph!")
        return None

    print("Nom du problème : ", problem.name)
    print("Type du problème : ", problem.type)
    print("Nombre de noeuds dans le graphe : ", problem.dimension)

    orig_graph = tsp_lib_to_networkx(problem)
    
    (tree, value, V) = tsp(orig_graph)
    (mst_tree, mst_value) = kruskal(orig_graph)
    
    print(V)
    
    print("tsp with cost ", value)
    
    display_graph(tree)
    
    # Tester qu'il n'y a qu'un seul cycle
    
    assert (len(sorted(nx.simple_cycles(tree)))) == 1
    
    # tester si c(mst) < c(tsp_)
    
    assert mst_value <= value
    



if __name__ == "__main__":

    print("Test de l'algorithme heuristique résolvant le TSP")
    main()
    


