import sys
import time
import copy
import random
import math
from itertools import chain
import re
import numpy as np
#import pandas as pd

## <DONTCOPY> ##
from Pastille import Pastille
from Point import Point
from Pacman import Pacman
from Pathfinding import Pathfinding
from Debug import Debug
## </DONTCOPY> ##

# debugTiming
debugTiming = dict()

class Game: 

    # owner
    ME = 1
    OPPONENT = 0

    # Tile
    WALL = "#"
    FLOOR = " "

    def __init__(self):
        self.units = []
        self.OpponentUnits = []
        self.pastilles = []
        self.score = 0
        self.opponentScore = 0
        self.tour = 0
        self.barycentre = {"x":0, "y":0}

        # init carte du jeu
        #self.map = [ [ None for y in range( HEIGHT ) ] for x in range( WIDTH ) ]


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

            if (int(owner) == self.ME):
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
        x_array = np.zeros(visiblePelletCount)
        y_array = np.zeros(visiblePelletCount)
        value_array = np.zeros(visiblePelletCount)
        for j in range(visiblePelletCount):
            x, y, value = map(int, input().split())
            self.pastilles.append(Pastille(value, x, y))
            x_array[j] = x
            y_array[j] = y
            value_array[j] = value

        # Remove our units not given - means they are dead :(
        for unit in self.units:
            if unit.lastRoundSeen != self.tour:
                self.units.remove(unit)

        # Calcul barycentre : pondéré par le poids des pastilles
        self.barycentre = {
            "x": np.average(x_array, weights=value_array),
            "y": np.average(y_array, weights=value_array)
        }

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
