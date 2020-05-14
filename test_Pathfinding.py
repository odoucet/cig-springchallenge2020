import sys 
import os
import time
import numpy

# Pour faire de beaux dessins
from PIL import Image, ImageDraw, ImageFont

#from classes.Pathfinding import Pathfinding
#from classes.Pacman import Pacman
#from classes.Pastille import Pastille
#from classes.Game import Game
from codetests import *

# Donne une action à un pote finalement plus prêt de la cible
def test_update_unit_flip_actions():
    g = Game()
    pac1 = Pacman(Game.ME, 3, 0, 0, 0, 21, 5, 5)
    pac2 = Pacman(Game.ME, 2, 0, 0, 0, 13, 9, 5)

    pac1.currentDestination = Pastille(1, 23, 2)
    pac2.currentDestination = Pastille(10, 23, 7)
    
    g.units = [pac1, pac2]

    # avant optim:
    assert pac2.currentDestination is not None
    assert pac1.currentDestination is not None
    assert pac1.currentDestination.points == 1
    assert pac2.currentDestination.points == 10

    g.optimizeActionOnNewTurn()

    assert pac1.currentDestination is not None
    assert pac1.currentDestination == Pastille(10, 23, 7)
    assert pac2.currentDestination is None

def test_point_getadjacentes():
    Game.WIDTH = 33
    Game.HEIGHT = 16

    pt = Point(0, 5)
    adj = pt.getAdjacentes([])
    assert len(adj) == 4
    assert Point(1, 5) in adj
    assert Point(0, 6) in adj
    assert Point(0, 4) in adj
    assert Point(32, 5) in adj

    pt = Point(32, 5)
    adj = pt.getAdjacentes([])
    assert len(adj) == 4
    assert Point(0, 5) in adj
    assert Point(32, 6) in adj
    assert Point(32, 4) in adj
    assert Point(31, 5) in adj

    pt = Point(32, 15)
    adj = pt.getAdjacentes([])
    assert len(adj) == 3
    assert Point(32, 14) in adj
    assert Point(31, 15) in adj
    assert Point(0, 15) in adj

    pt = Point(0, 15)
    adj = pt.getAdjacentes([])
    assert len(adj) == 3
    assert Point(0, 14) in adj
    assert Point(1, 15) in adj
    assert Point(32, 15) in adj

def test_build_distancemap():
    g = Game()

    Game.startTime = time.time()
    Game.WIDTH = 33
    Game.HEIGHT = 16

    map = ["#################################",
"### # # # # #   #   # # # # # ###",
"### # # # # # ##### # # # # # ###",
"### #   #   #   #   #   #   # ###",
"### ### # ### # # # ### # ### ###",
"                                 ",
"### ##### # # ##### # # ##### ###",
"        #   #       #   #        ",
"### # # # ##### # ##### # # # ###",
"#   #       #       #       #   #",
"# ##### # # # ##### # # # ##### #",
"#       # #   #####   # #       #",
"# # # # # # # ##### # # # # # # #",
"# #   #   # #       # #   #   # #",
"### ### ### # ##### # ### ### ###",
"#################################"]

    newMap = prepareMap(map)

    # Type: int
    tmp = time.time()
    nbMapCalc = Pathfinding.calculateDistanceMap(newMap, [False])
    sys.stderr.write(f"Calc {nbMapCalc}/242 in {(time.time() - tmp)*1000}ms")

    # combien de cases ? 
    nbCases = 0
    for x in range(Game.WIDTH):
        for y in range(Game.HEIGHT):
            if newMap[x][y] in [Game.FLOOR]:
                nbCases +=1
                if Pathfinding.distanceMap[x][y] is not None:
                    drawMap(Pathfinding.distanceMap[x][y], f'pathfinding_{x}_{y}', "distance", f"Distance depuis ({x},{y})")
        break

    nbCases = 242
    # on veut avoir tout calculé en 1s
    assert nbMapCalc/nbCases > 0.8 # 80%
    assert nbMapCalc/nbCases <= 1 # max 100%

    drawMap(Pathfinding.distanceMap[2][5], 'pathfinding_2_5', "distance", "Distance depuis (2,5)")
    drawMap(Pathfinding.buildDistanceMap(newMap, Point(2, 5), [False]), 'pathfinding_2_5bis', "distance", "Distance depuis (2,5)")

    # pas de carte sur des murs
    assert Pathfinding.distanceMap[0][0] is None
    assert Pathfinding.distanceMap[2][4] is None
    assert Pathfinding.distanceMap[20][8] is None
   
    # distance 0 sur le point de départ
    assert Pathfinding.distance(Point(2, 5), Point(2, 5))   == 0
    assert Pathfinding.distance(Point(9, 13), Point(9, 13)) == 0

    # distances
    assert Pathfinding.distance(Point(2, 5), Point(5, 5)) == 3
    assert Pathfinding.distance(Point(21, 5), Point(13, 11)) == 14
    assert Pathfinding.distance(Point(21, 5), Point(31, 10)) == 15

def prepareMap(strMap) -> numpy.array:
    finalmap = numpy.zeros( (Game.WIDTH, Game.HEIGHT), dtype=numpy.bool )

    i = 0
    for row in strMap:
        # one line of the grid: space " " is floor, pound "#" is wall
        j = 0
        for superchar in list(row):
            if superchar == "#":
                finalmap[j][i] = Game.WALL
            else:
                finalmap[j][i] = Game.FLOOR
            j += 1
        i += 1
    return finalmap

## Draw
DRAWZOOM=20
def drawMap(macarte, name, type="map", texte=None): 

    assert macarte.ndim == 2

    # no draw on Travis-CI
    if 'TRAVIS' in os.environ:
        return
    
    r = Image.new('RGBA', [Game.WIDTH*DRAWZOOM,Game.HEIGHT*DRAWZOOM])

    # get a drawing context
    d = ImageDraw.Draw(r)

    # On écrit la carte qu'on nous donne
    fnt = ImageFont.truetype("arial.ttf", 12)

    for x in range(Game.WIDTH):
        for y in range(Game.HEIGHT):
            if type == "map":
                if macarte[x][y] == "#":
                    fillColor=(50,50,50)
                elif macarte[x][y] == "o":
                    fillColor=(100,0,0)
                elif macarte[x][y] == "O":
                    fillColor=(255,0,0)
                elif macarte[x][y] == "X":
                    fillColor=(0,0,255)
                elif macarte[x][y] == "x":
                    fillColor=(0,0,100)
                elif macarte[x][y] == ".":
                    fillColor=(200,200,200)
                else:
                    fillColor=(0,0,0)

                d.rectangle([x*DRAWZOOM, y*DRAWZOOM, x*DRAWZOOM+DRAWZOOM, y*DRAWZOOM+DRAWZOOM], fill=fillColor)
            elif type == "distance":
                if macarte[x][y] is None:
                    fillColor=(50,50,50)
                elif numpy.isnan(macarte[x][y]):
                    fillColor=(255,255,255)
                elif numpy.isreal(macarte[x][y]):
                    if macarte[x][y] == 0:
                        fillColor=(255,255,100)
                    elif macarte[x][y] > 10:
                        fillColor=(int(255-((macarte[x][y]-10)*10)),100, 100)
                    else:
                        fillColor=(100,int(255-macarte[x][y]*10),100)
                else:
                    fillColor=(0,0,0)
                
                d.rectangle([x*DRAWZOOM, y*DRAWZOOM, x*DRAWZOOM+DRAWZOOM, y*DRAWZOOM+DRAWZOOM], fill=fillColor)
                if macarte[x][y] >= 0:
                    d.text((DRAWZOOM+x*DRAWZOOM-DRAWZOOM/2-3, DRAWZOOM+y*DRAWZOOM-DRAWZOOM/2-5), str(int(macarte[x][y])), font=fnt, fill=(80,0,100))
            else:
                d.text((DRAWZOOM+x*DRAWZOOM-DRAWZOOM/2-3, DRAWZOOM+y*DRAWZOOM-DRAWZOOM/2-5), str(macarte[x][y]), font=fnt, fill=(0,0,100))

    # on écrit les x,y
    legend = ImageFont.truetype("arial.ttf", 8)
    for x in range(len(macarte)+1):
        d.text((x*DRAWZOOM-DRAWZOOM/2, 3), str(x-1), font=legend, fill=(0,0,0))
        d.text((3, x*DRAWZOOM-DRAWZOOM/2,), str(x-1), font=legend, fill=(0,0,0))

    # Quadrillage
    for x in range(len(macarte)):
        d.line([(x*DRAWZOOM, 0), (x*DRAWZOOM, DRAWZOOM*len(macarte))], fill=(0,0,0))
        d.line([(0, x*DRAWZOOM), (DRAWZOOM*len(macarte), x*DRAWZOOM)], fill=(0,0,0))
    d.line([(len(macarte)*DRAWZOOM-1, 0), (len(macarte)*DRAWZOOM-1, DRAWZOOM*len(macarte)-1)], fill=(0,0,0))
    d.line([(0, len(macarte)*DRAWZOOM-1), (DRAWZOOM*len(macarte)-1, len(macarte)*DRAWZOOM-1)], fill=(0,0,0))

    if texte is not None:
        d.text([10, len(macarte)*DRAWZOOM-10], texte, font=legend, fill=(0,0,0))

    r.save('tests/'+name+'.png', 'PNG')