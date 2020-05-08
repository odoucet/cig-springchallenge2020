## <DONTCOPY> ##
from Point import Point
import math
## </DONTCOPY> ##

class Pathfinding:
    distanceMap = []

    @staticmethod
    def distance(a: Point, b: Point) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)
        #return Pathfinding.distanceMap[a.x][a.y][b.x][b.y]