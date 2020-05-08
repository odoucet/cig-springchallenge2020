## <DONTCOPY> ##
from Point import Point
## </DONTCOPY> ##

class Pacman (Point):
    def __init__(self, owner: int, id: int, type: int, speedTurnsLeft: int, abilityCooldown: int, x: int, y: int, tour: int):
        self.owner = owner
        self.id = id
        self.type = type
        self.speedTurnsLeft = speedTurnsLeft
        self.abilityCooldown = abilityCooldown
        self.action = ''
        self.currentDestination = None

        # Type: int
        self.lastRoundSeen = tour 

        Point.__init__(self, x, y)

    def __str__(self):
        return f'P#{self.id}({self.x},{self.y})={self.type}'


    def update(self, type: int, speedTurnsLeft: int, abilityCooldown: int, x: int, y: int, tour: int):
        self.type = type
        self.speedTurnsLeft = speedTurnsLeft
        self.abilityCooldown = abilityCooldown
        self.x = x
        self.y = y
        self.lastRoundSeen = tour
        