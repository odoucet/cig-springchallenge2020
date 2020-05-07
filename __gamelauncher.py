#############################################
############### Game launcher ###############

g = Game()

g.init()
while True:
    g.update()
    g.build_output()
    g.output()
