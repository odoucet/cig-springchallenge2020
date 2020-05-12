import sys
import numpy

class Debug:

    # debugTiming
    timing = dict()

    @staticmethod
    def map(macarte: numpy.array, loops = 0):
        sys.stderr.write("*** DEBUG CARTE (loops: "+str(loops)+") ***\n")

        caseType = None

        for y in range(len(macarte[0])):
            for x in range(len(macarte)):
                if macarte[x][y] is None:
                    # TODO: ecrire avec la bonne largeur
                    sys.stderr.write(" **")
                else:
                    if caseType is None:
                        caseType = type(macarte[0][0])
                        
                    if caseType is bool or caseType is numpy.bool_:
                        sys.stderr.write(f" {int(macarte[x][y])}")
                    elif caseType is str:
                        sys.stderr.write(f" {str(macarte[x][y]):4s}")
                    elif caseType is int:
                        sys.stderr.write(f" {str(macarte[x][y]):2s}")
                    else:
                        sys.stderr.write(f" {str(macarte[x][y]):2s}")
            sys.stderr.write("\n")
        sys.stderr.write("\n")

    @staticmethod
    def pythonMap(macarte):
        sys.stderr.write(str(macarte)+"\n")

    @staticmethod
    def msg(msg):
        sys.stderr.write(str(msg)+"\n")
