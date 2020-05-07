# concatenate cig.py and gamelauncher.py to codefinal.py

filenames = ['cig.py', '__gamelauncher.py']
with open('codefinal.py', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
