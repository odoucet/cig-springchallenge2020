import math
import numpy

class Pathfinding:

    distanceMap = []

    ## <DONTCOPY> ##
    from classes.Point import Point
    ## </DONTCOPY> ##

    @staticmethod
    def distance(a: Point, b: Point) -> int:
        if Pathfinding.distanceMap[a.x][a.y] is None:
            #sys.stderr.write(f"distanceAB test {Pathfinding.distanceMap[b.x][b.y]}")
            #if Pathfinding.distanceMap[b.x][b.y][a.x][a.y] is not numpy.nan:
            #    return Pathfinding.distanceMap[b.x][b.y][a.x][a.y]
            
            # TODO: voir si on peut calculer la distanceMap
            return abs(a.x - b.x) + abs(a.y - b.y)
        return Pathfinding.distanceMap[a.x][a.y][b.x][b.y]

    # construit une carte des distances basé sur macarte, par rapport à position.
    # on la veut générique, donc si position n'est pas un angle faut que ça marche quand même.
    # argument facultatif: maxDist pour calculer qu'un bout de la carte
    @staticmethod
    def buildDistanceMap(macarte: numpy.array, position: Point, murs) -> numpy.array:
        # cannot store NoneType with Python
        tmpcarte = numpy.empty( (len(macarte), len(macarte[0]))) # , dtype=numpy.int8 
        tmpcarte.fill(numpy.nan)
        maxDist = 99

        #sys.stderr.write(f"Start {position} = 0")
        
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
            
            cases = element.getAdjacentes(macarte)
            #print(f"Les cases adjacentes de {element} sont :")
            for case in cases:
                # si c'est un mur on passe: 
                if macarte[case.x][case.y] in murs:
                    continue
                
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
        myx: int
        myy: int

        for x in range(len(macarte)):
            Pathfinding.distanceMap[x] = {}
            for y in range(len(macarte[0])):
                 Pathfinding.distanceMap[x][y] = {}

        for myx in range(len(macarte)):
            for myy in range(len(macarte[0])):
                if macarte[myx][myy] in murs:
                    Pathfinding.distanceMap[myx][myy] = None
                else:
                    if not Game.check_timeout():
                        #tmp = time.time()
                        tmp = Pathfinding.buildDistanceMap(macarte, Point(myx, myy), [False])
                        assert tmp[myx][myy] == 0

                        Pathfinding.distanceMap[myx][myy] = tmp
                        nbCalcMap += 1
                        #Debug.msg(f"checkDistanceMap({x},{y}): {round((time.time() - tmp)*100000)} us")
                    else:
                        Debug.msg(f"checkDistanceMap stopped at {myx},{myy} with  {time.time() - Game.startTime}")
                        return nbCalcMap
        return nbCalcMap
