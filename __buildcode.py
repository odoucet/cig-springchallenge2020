# concatenate cig.py and gamelauncher.py to codefinal.py
import re

filenames = ['Point', 'Pathfinding', 'Debug', 'Pacman', 'Pastille', 'Game']

with open('codefinal.py', 'w') as outfile:
    for fname in filenames:

        fp = open('classes/'+fname+'.py')
        buf = fp.read()
        buf = re.sub("## <DONTCOPY> ##(.*)## </DONTCOPY> ##", "", buf, flags=re.S)
        outfile.write(buf)
        fp.close()

    fp = open('__gamelauncher.py')
    outfile.write(fp.read())
    fp.close()
