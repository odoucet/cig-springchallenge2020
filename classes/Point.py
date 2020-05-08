
## <DONTCOPY> ##
from Pathfinding import Pathfinding
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

    # Retourne le point dans srcArray le plus proche de point
    # srcArray: Point[]
    def nearest(self, srcArray):
        nearest = None
        nearestDist = None

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
