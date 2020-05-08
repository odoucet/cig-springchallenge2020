import sys
import time
import copy
import random
import math
from itertools import chain
import re

# MAP SIZE
WIDTH = 12
HEIGHT = 12

# OWNER
ME = 1
OPPONENT = 0


# TILE TYPE
WALL = "#"
FLOOR = " "

# Compilations re
# TRAIN_PATTERN = re.compile("^TRAIN ([0-9]*) ([0-9]*) ([0-9]*)$")

# On met notre distanceMap en global pour simplifier le code ... et désolé c'est dégueu :(
# distanceMap = [ [ None for y in range( HEIGHT ) ] for x in range( WIDTH ) ]

# debugTiming
debugTiming = dict()

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
            tmpDist = distance(entity, self)
            if nearest is None or tmpDist < nearestDist:
                nearest = entity
                nearestDist = tmpDist
        return nearest

    # Tri un tableau par distance, du plus proche au plus loin
    def sortNearest(self, srcArray):
        return sorted(srcArray, key = lambda src: distance(src, self))

# Pastilles
class Pastille (Point): 
    def __init__(self, points: int, x: int, y: int):
        self.points = points
        Point.__init__(self, x, y)

    def __str__(self):
        return f'O({self.x},{self.y})={self.points}'

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.points == other.points)

# Pacman
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
        

class Game:
    def __init__(self):
        self.units = []
        self.OpponentUnits = []
        self.pastilles = []
        self.score = 0
        self.opponentScore = 0
        self.tour = 0

        # init carte du jeu
        #self.map = [ [ None for y in range( HEIGHT ) ] for x in range( WIDTH ) ]


    # Strategie de deplacement des unites
    def move_units(self):
        # on commence simple : on va a la case vide/adversaire la plus proche
        for unit in self.units:
            # on sait deja où on va ? 
            if unit.currentDestination is not None:
                if distance(unit, unit.currentDestination) >= 1:
                    unit.action = f'MOVE {unit.id} {unit.currentDestination.x} {unit.currentDestination.y} CURDEST'
                    # pour eviter qu'un autre pacman aille aussi dessus, on vire la pastille: 
                    for pastille in self.pastilles:
                        if pastille == unit.currentDestination:
                            self.pastilles.remove(pastille)
                            break
                    continue
                else:
                    unit.currentDestination = None

            finalDestination = None
            destinations = unit.sortNearest(self.pastilles)

            dest: Pastille
            for dest in destinations:
                # on va a la plus grosse pastille la plus proche
                if dest.points > 1:
                    finalDestination = dest
                    break
            
            if finalDestination is None:
                for dest in destinations:
                    finalDestination = dest
                    break

            if finalDestination is not None:
                unit.currentDestination = finalDestination

                unit.action = f'MOVE {unit.id} {finalDestination.x} {finalDestination.y} NEW'
                # pour eviter qu'un autre pacman aille aussi dessus, on vire la pastille: 
                for pastille in self.pastilles:
                    if pastille == unit.currentDestination:
                        self.pastilles.remove(pastille)
                        break
        return


    # debut du jeu, qu'au premier tour donc
    def init(self):
        # width: size of the grid
        # height: top left corner is (x=0, y=0)
        self.width, self.height = [int(i) for i in input().split()]
        for i in range(self.height):
            row = input()  # one line of the grid: space " " is floor, pound "#" is wall
        return



    # Return false if timeout near and we should stop what we are doing
    def check_timeout(self)-> bool:
        if self.tour <= 1:
            timeout = 1
        else:
            timeout = 0.045
        if (time.time() - self.startTime) > timeout:
            return True
        return False


    # on verifie la cible: si un ami est plus proche, on lui file si elle est mieux
    def optimizeActionOnNewTurn(self):
        # Type: Pacman
        for unit in self.units:
            self.action = ''
            # on verifie la cible: si un ami est plus proche, on lui file si elle est mieux

            # proteger si currentDestination n'est pas une pastille
            if unit.currentDestination is not None:
                # combien de points ? 
                if unit.currentDestination.points > 1:
                    # oui, ça vaut le coup de regarder si qqu'un est mieux placé
                    dist = distance(unit, unit.currentDestination)
                    # Type: (Pacman)
                    for pote in unit.currentDestination.sortNearest(self.units):
                        # si il est plus loin, on s'en fout
                        if distance(pote,unit.currentDestination) >= dist:
                            break # on est en sortNearest, pas la peine de tester les autres
                        if pote.currentDestination is None:
                            debugMsg(f'Switch destination between {unit} and {pote} (noDest)=> {unit.currentDestination}')
                            pote.currentDestination = unit.currentDestination
                            unit.currentDestination = None
                            break
                        if pote.currentDestination.points < unit.currentDestination.points:
                            debugMsg(f'Switch destination between {unit} and {pote} => {unit.currentDestination}')
                            pote.currentDestination = unit.currentDestination
                            unit.currentDestination = None
                            break

    def update(self):
        self.optimizeActionOnNewTurn()  

        self.pastilles.clear()

        self.tour += 1

        self.score, self.opponentScore = [int(j) for j in input().split()]
        self.startTime = time.time() ## after first input, to not count IA time

        visiblePacCount = int(input())

        for j in range(visiblePacCount):
            inputs = input().split()
            unit_id, owner, x, y = map(int, inputs[:4])
            typeId = 0
            speedTurnsLeft = 0
            abilityCooldown = 0
            found = False

            if (int(owner) == ME):
                for unit in self.units:
                    if unit.id == unit_id:
                        unit.update(typeId, speedTurnsLeft, abilityCooldown, x, y, self.tour)
                        found = True
                        break
                if found is False:
                    self.units.append(Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y, self.tour))
            else:
                for unit in self.OpponentUnits:
                    if unit.id == unit_id:
                        unit.update(typeId, speedTurnsLeft, abilityCooldown, x, y, self.tour)
                        found = True
                        break
                if found is False:
                    self.OpponentUnits.append(Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y, self.tour))

        visiblePelletCount = int(input())
        for j in range(visiblePelletCount):
            x, y, value = map(int, input().split())
            self.pastilles.append(Pastille(value, x, y))

        # Remove our units not given - means they are dead :(
        for unit in self.units:
            if unit.lastRoundSeen != self.tour:
                self.units.remove(unit)

        # MAJ du temps:
        debugTiming['update'] = time.time() - self.startTime 



    def timingFunc(self, funcName):
        tmp = time.time()
        r = funcName()
        debugTiming[funcName.__name__] = time.time() - tmp
        return r

    def build_output(self):
        # deplacement des unites
        self.timingFunc(self.move_units)


    def output(self):
        # on affiche chaque action de pacman
        output = False
        for unit in self.units:
            if unit.action != "":
                output = True
                print(unit.action, end="|")

        if output == False:
            print('MOVE 0 0 0 ANTICRASH') # anti crash
        else:
            # final \n
            print('')

        # Temps mis dans chaque fonction: 
        totalTime = self.getTotalTime()

        sys.stderr.write("TOUR #"+str(self.tour)+": "+str(totalTime)+"ms - ")
        if totalTime == 0:
            return

        for key, value in sorted(debugTiming.items(), reverse=True, key=lambda x: x[1]):
            sys.stderr.write(key+": "+str(round(value*1000/totalTime*100))+"% ")
        
        # Si on veut recup la carte: 
        #debugPythonMap(self.map)

    # get total time in ms
    def getTotalTime(self)-> int:
        return round((time.time() - self.startTime)*1000)


def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def debugMap(macarte, loops = 0):
    sys.stderr.write("*** DEBUG CARTE (loops: "+str(loops)+")***\n")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if macarte[x][y] is None:
                sys.stderr.write(" **")
            else:
                sys.stderr.write(f" {str(macarte[x][y]):2s}")
        sys.stderr.write("\n")
    sys.stderr.write("\n")

def debugPythonMap(macarte):
    sys.stderr.write(str(macarte)+"\n")

def debugMsg(msg):
    sys.stderr.write(str(msg)+"\n")
