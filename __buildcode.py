# concatenate cig.py and gamelauncher.py to codefinal.py
import re

filenames = ['Point', 'Pathfinding', 'Debug', 'Pacman', 'Pastille', 'Game']

with open('codefinal.py', 'w') as outfile:
    for fname in filenames:

        fp = open('classes/'+fname+'.py')
        buf = fp.read()
        buf = re.sub("## <DONTCOPY> ##(.*?)## </DONTCOPY> ##", "", buf, flags=re.S)
        outfile.write("\n\n# Class "+fname+"\n"+buf)
        fp.close()

    # Tests
    from shutil import copyfile
    copyfile('codefinal.py', 'codetests.py')

    fp = open('__gamelauncher.py')
    outfile.write("\n\n# LAUNCHER\n"+fp.read())
    fp.close()
