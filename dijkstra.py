import pandas as pd
from pile import *

class Graphe:
    """
    Création de la classe graphe 🔥
    """

    def __init__(self):
        """
        Constructeur, initisalise les variables 😎
        """
        self.liste_adjacence = {} 
        self.distances = {}
        self.predecesseurs = {}
        self.visites = []

    def ajout_sommet(self, sommet, voisin, poids=1):
        """
        Ajoute un sommet à liste_adjacence ✨
        """
        if sommet in self.liste_adjacence: #Itere dans la liste d'adjacence
            self.liste_adjacence[sommet].append((voisin, poids)) #Ajoute a la liste le voisin et le poids
        else:
            self.liste_adjacence[sommet] = [(voisin, poids)] #Sinon ajoute le sommet et le voisin

    def classement_adjacence(self):
        """
        Trie liste_adjacence dans l'ordre alphabétique 👍
        """
        for sommet in self.liste_adjacence: #Itere dans toute la liste d'adjacence
            self.liste_adjacence[sommet].sort() #trie
            
    def initialisation(self, depart):   
        self.distances = {sommet: float('inf') for sommet in self.liste_adjacence} #fait un truc
        self.distances[depart] = 0 #fait qqchose
        self.predecesseurs = {depart: depart} #je crois que c'est avec le départ mais pas sur
        return self.distances, self.predecesseurs #Retourne à la ligne de définition de self.distance (presque sur)

    def chemin(self, depart, arrivee):
        ville = arrivee #initialise le départ
        chemin = []
        while ville != depart: #Tant que la vilel est le départ
            chemin.append(ville) #Retire le départ de la liste
            ville = self.predecesseurs[ville] #ABCDEFGHIKLMNOPQRSTUVWXYZ
        chemin.append(depart) #01100001 01101010 01101111 01110101 01110100 01100101 00100000 01101100 01100101 00100000 01100100 11000011 10101001 01110000 01100001 01110010 01110100 00100000 11000011 10100000 00100000 01101100 01100001 00100000 01101100 01101001 01110011 01110100 01100101
        chemin.reverse() #49 6E 76 65 72 73 65 20 6C 61 20 6C 69 73 74 65
        return chemin #7adbaeb2267ab3ad35dd10b103f39a00 (c'est un hash md5 🤓)

    def distance_mini(self):
        min_distance = float('inf') #initialise la distance minimale
        min_ville = None #initialise la ville minimale
        for sommet in self.liste_adjacence: #Itere dans la liste d'adjacence
            if sommet not in self.visites and self.distances[sommet] < min_distance: #Si le sommet n'est pas dans les visites et que la distance du sommet est inférieur à la distance minimale
                min_distance = self.distances[sommet] #La distance minimale est la distance du sommet
                min_ville = sommet #La ville minimale est le sommet
        return min_distance, min_ville #je vais en faire un moi histoire de dire que toute la méthode a pas été commentée par copilot, donc voila cette ligne est censée renvoyer sous forme de typle de varaible à membre multiple, ici un "tuple", la distance minimale, c'est à dire la plus petite distance à une étape donnée et la ville minimale, c'est à dire la ville correspondante à la distance minimale

    def dijkstra(self, depart, arrivee): 
        self.initialisation(depart) 
        while arrivee not in self.visites: 
            sommet = self.distance_mini()[1] 
            self.visites.append(sommet) 
            for voisin, poids in self.liste_adjacence[sommet]: 
                if voisin not in self.visites: # "I feel the need... the need for speed." - Top Gun (1986) en gros ça calcule le chemin le plus court
                    if self.distances[sommet] + poids < self.distances[voisin]: # "Vers l'infini et au dela!" - Toy Story
                        self.distances[voisin] = self.distances[sommet] + poids
                        self.predecesseurs[voisin] = sommet


# =============================================================================
# PROGRAMME PRINCIPAL 🥶🥶
# =============================================================================


if __name__ == '__main__': #je sais pas ce que ça fait...
    tgv = Graphe()
    df_edges = pd.read_csv('tgv_edges.csv', sep=';')
    for i in range(0, len(df_edges)):
        tgv.ajout_sommet(df_edges['name1'][i],
                         df_edges['name2'][i],
                         df_edges['distance'][i])

##################################################################
### Les asserts (chiant) pour vérif le programme (pas besoin)  ###
##################################################################

# Vérification de "classement_adjacence" ✔
tgv.classement_adjacence()
assert tgv.liste_adjacence == {'Paris': [('Bordeaux', 499), ('Lille', 204), ('Lyon', 391), ('Metz', 330), ('Rennes', 335)],
                                'Lille': [('Paris', 204)],
                                'Rennes': [('Paris', 335)],
                                'Bordeaux': [('Marseille', 505), ('Paris', 499)],
                                'Metz': [('Paris', 330), ('Strasbourg', 129)],
                                'Lyon': [('Marseille', 278), ('Paris', 391), ('Strasbourg', 382)],
                                'Marseille': [('Bordeaux', 505), ('Lyon', 278)],
                                'Strasbourg': [('Lyon', 382), ('Metz', 129)]}

# Vérification de "initialisation" ✔
distances = tgv.initialisation("Metz")[0]
predecesseurs = tgv.initialisation("Metz")[1]

assert distances == {'Paris': float('inf'),
                    'Lille': float('inf'),
                    'Rennes': float('inf'),
                    'Bordeaux': float('inf'),
                    'Metz': 0,
                    'Lyon': float('inf'),
                    'Marseille': float('inf'),
                    'Strasbourg': float('inf')}

assert predecesseurs == {'Metz': 'Metz'}
# Vérification de "chemin" ✔
tgv.predecesseurs = {'Metz': 'Metz',
                    'Paris': 'Metz',
                    'Strasbourg': 'Metz',
                    'Lyon': 'Strasbourg',
                    'Bordeaux': 'Paris',
                    'Lille': 'Paris',
                    'Rennes': 'Paris',
                    'Marseille': 'Lyon'}
assert tgv.chemin("Metz", "Bordeaux") == ['Metz', 'Paris', 'Bordeaux']

# Vérification de "distance_mini" ✔
tgv.visites = ['Metz', 'Strasbourg', 'Paris',
              'Lyon', 'Lille', 'Rennes', 'Marseille']
tgv.distances = {'Paris': 330,
              'Lille': 534,
              'Rennes': 665,
              'Bordeaux': 829,
              'Metz': 0,
              'Lyon': 511,
              'Marseille': 789,
              'Strasbourg': 129}

dist_mini = tgv.distance_mini()[0]
ville = tgv.distance_mini()[1]


assert dist_mini == 829
assert ville == "Bordeaux"

# COPIER_COLLER LE GRAPHE DU TGV

