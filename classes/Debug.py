import sys

class Debug:

    # debugTiming
    timing = dict()

    @staticmethod
    def map(macarte, loops = 0):
        sys.stderr.write("*** DEBUG CARTE (loops: "+str(loops)+")***\n")
        #for y in range(HEIGHT):
        #    for x in range(WIDTH):
        #        if macarte[x][y] is None:
        #            sys.stderr.write(" **")
        #        else:
        #            sys.stderr.write(f" {str(macarte[x][y]):2s}")
        #    sys.stderr.write("\n")
        #sys.stderr.write("\n")

    @staticmethod
    def pythonMap(macarte):
        sys.stderr.write(str(macarte)+"\n")

    @staticmethod
    def msg(msg):
        sys.stderr.write(str(msg)+"\n")
