from helper import *
import os
import neat

#makes easier to see
setShowColors(True)

generation = 0
highscore = 0

def main(genomes, config):

    global generation
    global highscore

    generation += 1

    myinfo = Info()

    #NEAT stuff
    nets = []
    ge = []
    myinfo.dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        d = Dino(myinfo)
        g.fitness = 0
        ge.append(g)

    sand = Sand(myinfo)
    sky = Sky(myinfo)
    ### GAME LOOP ###
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        ### Quit program ###
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            pygame.quit()
            exit()

        #make dinos jump
        for x, d in enumerate(myinfo.dinos):

            if len(ge) > 0:
                #give dinos some fitness just cuz...
                ge[x].fitness += 0.1

            #provide AI with info:
            #ditance to cacti
            distance1 = -1
            distance2 = -1
            distance3 = -1
            height1 = -1
            height2 = -1
            height3 = -1

            if len(d.distanceToCacti) >= 3:
                distance1 = d.distanceToCacti[0]
                distance2 = d.distanceToCacti[1]
                distance3 = d.distanceToCacti[2]
                height1 = d.cactiHeight[0]
                height2 = d.cactiHeight[1]
                height3 = d.cactiHeight[2]
            elif len(d.distanceToCacti) == 2:
                distance1 = d.distanceToCacti[0]
                distance2 = d.distanceToCacti[1]
                distance3 = 800
                height1 = d.cactiHeight[0]
                height2 = d.cactiHeight[1]
                height3 = 0
            elif len(d.distanceToCacti) == 1:
                distance1 = d.distanceToCacti[0]
                distance2 = 800
                distance3 = 800
                height1 = d.cactiHeight[0]
                height2 = 0
                height3 = 0
            else:
                distance1 = 800
                distance2 = 800
                distance3 = 800
                height1 = 0
                height2 = 0
                height3 = 0

            #allow AI to make dinos jump
            output = nets[x].activate((d.y, distance1, distance2, distance3, height1, height2, height3))
            if output[0] > 0.50 and d.y == d.defaulty:
                print(output[0])
                d.jumping = True
                #add fitness for jumping (jk)
                ge[x].fitness -= 0.1
            elif output[0] <= 0.5:
                print("WOah: " + str(output[0]))


        #check if obstical should spawn
        myinfo.makeObstical()
        addedfitness = myinfo.removeObstical()
        #dinos that make it past obsticals
        # get rewarded
        for g in ge:
            g.fitness += addedfitness


        #check if game should be faster
        myinfo.makeHarder()

        #check dino collisions
        for x, d in enumerate(myinfo.dinos):
            d.calculateDistances()
            state = d.checkCollision()
            if state == True:
                #if dino collides, remove fitness
                ge[x].fitness -= 5
                myinfo.dinos.remove(d)
                nets.pop(x)
                ge.pop(x)

        #check if game is over
        if len(myinfo.dinos) == 0:
            break

        #display hs
        if myinfo.score > highscore:
            highscore = myinfo.score
                
        myinfo.drawScreen(sand, sky)
        myinfo.displayStats(len(myinfo.dinos), generation, highscore)
        pygame.display.update()
        time.sleep(0.025)

    

def runai(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    #create population
    p = neat.Population(config)

    #stats reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    #set fitness function
    winner = p.run(main, 100)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    runai(config_path)

#for iDtech
def activateMachineLearning():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    runai(config_path)
