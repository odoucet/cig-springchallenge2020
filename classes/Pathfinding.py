import math
import numpy
import sys

class Pathfinding:

    distanceMap = []

    ## <DONTCOPY> ##
    from classes.Point import Point
    from classes.Debug import Debug
    ## </DONTCOPY> ##

    @staticmethod
    def distance(a: Point, b: Point) -> int:
        # verification d'erreur de la mort qui tue: 
        if bool(Pathfinding.distanceMap) is False:
            Debug.msg(f"WARN: distanceMap not init")
            return abs(a.x - b.x) + abs(a.y - b.y)

        if Pathfinding.distanceMap[a.x][a.y] is None or numpy.isnan(Pathfinding.distanceMap[a.x][a.y][b.x][b.y]):
            # on inverse
            if Pathfinding.distanceMap[b.x][b.y] is None:
                # carte pas calculee
                return abs(a.x - b.x) + abs(a.y - b.y)
            elif numpy.isnan(Pathfinding.distanceMap[b.x][b.y][a.x][a.y]):
                # trop loin
                return abs(a.x - b.x) + abs(a.y - b.y)+10
            else:
                return Pathfinding.distanceMap[b.x][b.y][a.x][a.y]
        else:
            return Pathfinding.distanceMap[a.x][a.y][b.x][b.y]

    # construit une carte des distances basé sur macarte, par rapport à position.
    # on la veut générique, donc si position n'est pas un angle faut que ça marche quand même.
    # argument facultatif: maxDist pour calculer qu'un bout de la carte
    @staticmethod
    def buildDistanceMap(macarte: numpy.array, position: Point, murs, maxDist = 30) -> numpy.array:
        # cannot store NoneType with Python
        tmpcarte = numpy.empty( (len(macarte), len(macarte[0]))) # , dtype=numpy.int8 
        tmpcarte.fill(numpy.nan)
        
        # en itératif on incremente en partant du QG
        aTraiter = [ [position, 0] ]
        debugi = 0
        while len(aTraiter) > 0 and debugi < 500:
            debugi += 1
            element, distance = aTraiter.pop(0)

            # si on a deja fait en mieux
            if not numpy.isnan(tmpcarte[element.x][element.y]) and tmpcarte[element.x][element.y] <= distance:
                continue
            
            tmpcarte[element.x][element.y] = distance

            # si distance max atteinte, on quitte
            if (distance >= maxDist):
                continue
            
            cases = element.getAdjacentes(macarte, None, murs)
            #print(f"Les cases adjacentes de {element} sont :")
            for case in cases:                
                if numpy.isnan(tmpcarte[case.x][case.y]) or tmpcarte[case.x][case.y] > distance and [ case, distance + 1] not in aTraiter:
                    aTraiter.append([ case, distance + 1])
        return tmpcarte
    
    @staticmethod
    def calculateDistanceMap(macarte: numpy.array, murs) -> int:
        ## <DONTCOPY> ##
        from classes.Point import Point
        from classes.Game import Game
        from classes.Debug import Debug
        import time
        ## </DONTCOPY> ##

        #Pathfinding.distanceMap = {{None} * len(macarte[0])} * len(macarte)
        #Pathfinding.distanceMap = numpy.empty((len(macarte), len(macarte[0]), len(macarte), len(macarte[0])), dtype=object)
        Pathfinding.distanceMap = {}
        
        nbCalcMap = 0

        totalCalcExpected = 0

        casesOk = []

        for x in range(len(macarte)):
            Pathfinding.distanceMap[x] = {}
            for y in range(len(macarte[0])):
                if macarte[x][y] not in murs:
                    Pathfinding.distanceMap[x][y] = None
                    casesOk.append((x,y))
                    totalCalcExpected += 1
                else:
                    Pathfinding.distanceMap[x][y] = None

        for x,y in casesOk: 
            if not Game.check_timeout():
                tmp = Pathfinding.buildDistanceMap(macarte, Point(x, y), [False], 15)
                assert tmp[x][y] == 0

                Pathfinding.distanceMap[x][y] = tmp
                nbCalcMap += 1
            else:
                Debug.msg(f"checkDistanceMap stopped at {x},{y} ({round(nbCalcMap*100/totalCalcExpected)} %) with  {time.time() - Game.startTime}")
                return nbCalcMap
        return nbCalcMap
