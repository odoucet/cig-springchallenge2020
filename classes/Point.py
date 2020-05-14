from typing import List
import numpy
import math
## <DONTCOPY> ##
from classes.Pathfinding import Pathfinding
from classes.Game import Game
## </DONTCOPY> ##

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash(('x', self.x,
                 'y', self.y))

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    # Retourne les cases adjacentes, avec un filtre 
    def getAdjacentes(self, map: numpy.array, filtre = None, filtreExcluded = None) -> List:
        cases = []

        #                 droite              bas                 haut                 gauche               
        combinaisons = [  [self.x+1, self.y], [self.x, self.y+1] ]
        combinaisons.extend(([self.x, self.y-1],  [self.x-1, self.y]))

        for x,y in combinaisons:
            # comm inter grille
            if x < 0:
                # rewrite x
                x = Game.WIDTH + x
            elif x >= Game.WIDTH:
                x = x - Game.WIDTH

            if x >= 0 and x < Game.WIDTH and y >= 0 and y < Game.HEIGHT:
                if (filtre is None or map[x][y] in filtre) and (filtreExcluded is None or  map[x][y] not in filtreExcluded):
                    cases.append(Point(x, y))
        return cases

    # Retourne le point dans srcArray le plus proche de point
    # srcArray: Point[]
    def nearest(self, srcArray):
        nearest = None
        nearestDist = None

        ## <DONTCOPY> ##
        from classes.Pathfinding import Pathfinding
        ## </DONTCOPY> ##

        for entity in srcArray:
            # on stocke l'appel a distance() car c'est une fction couteuse en CPU
            tmpDist = Pathfinding.distance(entity, self)
            if nearest is None or tmpDist < nearestDist:
                nearest = entity
                nearestDist = tmpDist
        return nearest

    # Tri un tableau par distance, du plus proche au plus loin
    def sortNearest(self, srcArray):
        return sorted(srcArray, key = lambda src: Pathfinding.distance(src, self))
