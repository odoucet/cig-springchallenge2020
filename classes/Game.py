import sys
import time
import copy
import random
import math
from itertools import chain
import re
import numpy
#import pandas as pd

## <DONTCOPY> ##
from classes.Pastille import Pastille
from classes.Point import Point
from classes.Pacman import Pacman
from classes.Pathfinding import Pathfinding
from classes.Debug import Debug
## </DONTCOPY> ##

# debugTiming
debugTiming = dict()

class Game: 

    # owner
    ME = 1
    OPPONENT = 0

    # Tile - easier to store bool instead of char
    WALL = False  # "#"
    FLOOR = True  # " "

    # Current map, bool
    map: numpy.array

    WIDTH: int
    HEIGHT: int

    tour = 0
    startTime = 0


    def __init__(self):
        self.units = []
        self.OpponentUnits = []
        self.pastilles = []
        self.score = 0
        self.opponentScore = 0
        Game.tour = 0


    # Strategie de deplacement des unites
    def move_units(self):
        # on commence simple : on va a la case vide/adversaire la plus proche
        for unit in self.units:
            # on sait deja où on va ? 
            if unit.currentDestination is not None:
                if Pathfinding.distance(unit, unit.currentDestination) >= 1:
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
        Game.WIDTH, Game.HEIGHT = [int(i) for i in input().split()]
        Game.startTime = time.time()

        self.map = numpy.zeros( (Game.WIDTH, Game.HEIGHT), dtype=numpy.bool )

        # On pose la carte des valeurs de Pastille, en partant du principe qu'il y en a une par case libre.
        # on stockera zéro si pas de pastille
        self.internalPastilleMap = numpy.zeros( (Game.WIDTH, Game.HEIGHT), dtype=numpy.int8 )

        for i in range(Game.HEIGHT):
            row = input()  # one line of the grid: space " " is floor, pound "#" is wall
            j = 0
            for superchar in list(row):
                if superchar == "#":
                    self.map[j][i] = self.WALL
                else:
                    self.map[j][i] = self.FLOOR
                    self.internalPastilleMap[j][i] = 1
                j += 1

        # Calculate distanceMap complete
        tmp = time.time()
        Pathfinding.calculateDistanceMap(self.map, [False])
        debugTiming['calculateDistanceMap'] = time.time() - tmp

        return


    # Return true if timeout near and we should stop what we are doing
    @staticmethod
    def check_timeout()-> bool:
        if Game.tour <= 1:
            timeout = 0.995
        else:
            timeout = 0.045
        if (time.time() - Game.startTime) > timeout:
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
                    dist = Pathfinding.distance(unit, unit.currentDestination)
                    # Type: (Pacman)
                    for pote in unit.currentDestination.sortNearest(self.units):
                        # si il est plus loin, on s'en fout
                        if Pathfinding.distance(pote,unit.currentDestination) >= dist:
                            break # on est en sortNearest, pas la peine de tester les autres
                        if pote.currentDestination is None:
                            Debug.msg(f'Switch destination between {unit} and {pote} (noDest)=> {unit.currentDestination}')
                            pote.currentDestination = unit.currentDestination
                            unit.currentDestination = None
                            break
                        if pote.currentDestination.points < unit.currentDestination.points:
                            Debug.msg(f'Switch destination between {unit} and {pote} => {unit.currentDestination}')
                            pote.currentDestination = unit.currentDestination
                            unit.currentDestination = None
                            break

    def update(self):
        Game.tour += 1
        # reset timings
        debugTiming.clear()
        self.score, self.opponentScore = [int(j) for j in input().split()]

        # else already started
        if Game.tour > 1:
            Game.startTime = time.time() ## after first input, to not count IA time

        self.optimizeActionOnNewTurn()  
        self.pastilles.clear()

        visiblePacCount = int(input())

        for j in range(visiblePacCount):
            inputs = input().split()
            unit_id, owner, x, y = map(int, inputs[:4])
            typeId = 0
            speedTurnsLeft = 0
            abilityCooldown = 0
            found = False

            # plus de pastille sur soi-même ou un ennemi
            self.internalPastilleMap[x][y] = 0

            if (int(owner) == self.ME):
                for unit in self.units:
                    if unit.id == unit_id:
                        unit.update(typeId, speedTurnsLeft, abilityCooldown, x, y, Game.tour)
                        found = True
                        break
                if found is False:
                    self.units.append(Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y, Game.tour))
            else:
                for unit in self.OpponentUnits:
                    if unit.id == unit_id:
                        unit.update(typeId, speedTurnsLeft, abilityCooldown, x, y, Game.tour)
                        found = True
                        break
                if found is False:
                    self.OpponentUnits.append(Pacman(owner, unit_id, typeId, speedTurnsLeft, abilityCooldown, x, y, Game.tour))

        visiblePelletCount = int(input())
        x_array = numpy.zeros(visiblePelletCount)
        y_array = numpy.zeros(visiblePelletCount)
        value_array = numpy.zeros(visiblePelletCount)
        for j in range(visiblePelletCount):
            x, y, value = map(int, input().split())
            self.pastilles.append(Pastille(value, x, y))
            # update pastille
            self.internalPastilleMap[x][y] = value

            x_array[j] = x
            y_array[j] = y
            value_array[j] = value

        # Remove our units not given - means they are dead :(
        for unit in self.units:
            if unit.lastRoundSeen != Game.tour:
                self.units.remove(unit)
                continue
                
            # TODO: mettre à jour self.internalPastilleMap en effacant les cases actuellement visibles et sans pastille
            # code à faire ici (faut incrementer / decrementer X/Y sur soi jusqu'à voir un mur)


        # MAJ du temps:
        debugTiming['update'] = time.time() - Game.startTime 



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
        totalTime = Game.getTotalTime()

        sys.stderr.write("TOUR #"+str(Game.tour)+": "+str(totalTime)+"ms - ")
        if totalTime == 0:
            return

        for key, value in sorted(debugTiming.items(), reverse=True, key=lambda x: x[1]):
            sys.stderr.write(key+": "+str(round(value*1000/totalTime*100))+"% ")
        
        # Si on veut recup la carte: 
        #debugPythonMap(self.map)

    # get total time in ms
    @staticmethod
    def getTotalTime()-> int:
        return round((time.time() - Game.startTime)*1000)
