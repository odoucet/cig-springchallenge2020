import sys 
import os
import time

# Pour faire de beaux dessins
from PIL import Image, ImageDraw, ImageFont

from cig import Game, Point, Pacman, OPPONENT, ME, Pastille


def test_stub(): 
    assert 1 == 1

# Donne une action à un pote finalement plus prêt de la cible
def test_update_unit_flip_actions():
    g = Game()
    pac1 = Pacman(ME, 3, 0, 0, 0, 21, 5)
    pac2 = Pacman(ME, 2, 0, 0, 0, 13, 9)

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
