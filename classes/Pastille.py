## <DONTCOPY> ##
from classes.Point import Point
## </DONTCOPY> ##

class Pastille (Point): 
    def __init__(self, points: int, x: int, y: int):
        self.points = points
        Point.__init__(self, x, y)

    def __str__(self):
        return f'O({self.x},{self.y})={self.points}'

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.points == other.points)
