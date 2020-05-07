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
    def __init__(self, value: int, x: int, y: int):
        self.value = value
        Point.__init__(self, x, y)

# Pacman
class Pacman (Point):
    def __init__(self, owner: int, id: int, type: int, speedTurnsLeft: int, abilityCooldown: int, x: int, y: int):
        self.owner = owner
        self.id = id
        self.type = type
        self.speedTurnsLeft = speedTurnsLeft
        self.abilityCooldown = abilityCooldown
        self.action = ''

        Point.__init__(self, x, y)

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
            unit.action = f'{unit.id} 1 2'
        return


    # debut du jeu, qu'au premier tour donc
    def init(self):
        # width: size of the grid
        # height: top left corner is (x=0, y=0)
        self.width, self.height = [int(i) for i in input().split()]
        for i in range(self.height):
            row = input()  # one line of the grid: space " " is floor, pound "#" is wall

        debugMsg(f'width={self.width},height={self.height}')
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


    def update(self):
        #self.units.clear()
        #self.OpponentUnits.clear()

        self.pastilles.clear()

        self.tour += 1

        # on reset pas l'action en cours d'un pacman, car il  l'a peut etre pas finie

        self.score, self.opponentScore = [int(j) for j in input().split()]
        self.startTime = time.time() ## after first input, to not count IA time


        visiblePacCount = int(input())

        for j in range(visiblePacCount):
            unit_id, owner, x, y, typeId, speedTurnsLeft, abilityCooldown =  input().split()
            if (owner == ME):
                obj = Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y)
                self.units.append(obj)
            else:
                self.OpponentUnits.append(Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y))

        visiblePelletCount = int(input())
        for j in range(visiblePelletCount):
            value, x, y = [int(j) for j in input().split()]
            self.pastilles.append(Pastille(value, x, y))


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
                print(unit.action)

        if output == False:
            print('MOVE 0 0 0') # anti crash
        
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
    return 0


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
