import pygame
from pygame.locals import *
import time
import random

# constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 350
# colors
WHITE = (255, 255, 255)

# set up pygame
pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Dinosaur Game")
pygame.font.init()

#modes
showcolors = False

def setShowColors(b):
    global showcolors
    showcolors = b

#variables
font = pygame.font.Font('freesansbold.ttf', 28)

class Info:

    def __init__(self):

        self.c = []
        self.dinos = []
        self.score = 0
        self.multiplier = 1
        self.highscore = -1
        self.gamespeed = 15
        self.spawnrate = 1

    def countScore(self):
      

        self.score += (1 * self.multiplier)

        currentscore = font.render(str(self.score), True, (0,0,0))
        screen.blit(currentscore, (700, 100))

        self.setNewHS()
        # hscore = font.render("H.S. " + str(self.highscore), True, (0,0,0))
        # screen.blit(hscore, (640, 10))

    def makeObstical(self):
        #return true if obstical is created

        #randomly spawn in cacti
        num = random.randint(0, 1000)
        if(num < 40 *self.spawnrate):

            #make sure not too close or far from previous cactus
            if len(self.c) == 0 or (1200 - self.c[len(self.c)-1].x < 40 or 1200 - self.c[len(self.c)-1].x > 150):
                
                if num > 30:
                #make bird
                    if len(self.c) == 0 or 1200 - self.c[len(self.c)-1].x > 250:
                        bird = Bird(self)
                        self.c.append(bird)
    
                else: 
                    #check to make sure there are no birds
                    birdpresent = False
                    for cactus in self.c:
                        if cactus.type == "bird" and cactus.x < 600 and cactus.x > 200:
                            birdpresent = True

                    #make cactus
                    if birdpresent == False:
                        cactus = Cactus(self)
                        self.c.append(cactus)


    def removeObstical(self):
        #if dino made it to this point, it is rewarded
        addedfitness = 0
        for cactus in self.c:
            if cactus.x < -100:
                self.c.remove(cactus)
                addedfitness += 0.1

        return addedfitness


    def getHS(self):
        with open('highscore.txt') as file:
            hs = file.readlines()
            hs = hs[0]
            return int(hs)

    def setNewHS(self):

        file = open("highscore.txt", "w")
        if self.score > self.highscore:
            self.highscore = self.score
            file.write(str(self.score))
        else:
            file.write(str(self.highscore))
        file.close()


    #draw screen
    def drawScreen(self, sand, sky):
        #background
        screen.fill(WHITE)
        #sand
        if sand != None:
            sand.drawSand()
        #sky
        if sky != None:
            sky.drawSky()
        #dino
        for dino in self.dinos:
            dino.checkJump()
            dino.drawDino()
        #cactus
        for cactus in self.c:
            cactus.draw()
        #score
        self.countScore()

    def gameOver(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            ### Quit program ###
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                exit()

            ### Restart program ###
            if keys[pygame.K_TAB]:
                running = False
                rungame()

            pygame.display.update()

    #increases game difficulty over time
    def makeHarder(self):

        # max spawn rate
        if self.score > 150000:
            self.spawnrate = 2.2
        elif self.score > 10000:
            self.spawnrate = 2
        elif self.score > 5000:
            self.spawnrate = 1.8
        #fastest
        elif self.score > 3000:
            self.gamespeed = 24
            self.multiplier = 4
            self.spawnrate = 1.6
        #medium
        elif self.score > 1500:
            self.gamespeed = 21
            self.multiplier = 3
            self.spawnrate = 1.4
        #medium-slow
        elif self.score > 500:
            self.gamespeed = 18
            self.multiplier = 2
            self.spawnrate = 1.2

    def displayStats(self, l, gen, hs):

        n = font.render("Gen: " + str(gen), True, (0,0,0))
        screen.blit(n, (500, 60))

        num = font.render("Alive: " + str(l), True, (0,0,0))
        screen.blit(num, (640, 60))

        hscore = font.render("H.S. " + str(hs), True, (0,0,0))
        screen.blit(hscore, (640, 10))


#classes
class Dino:

    def __init__(self, info):

        self.info = info

        self.x = 50
        self.y = 200
        self.width = 80
        self.height = 80
        self.defaulty = 200
        self.jumping = False
        self.jumpheight = 64
        self.up = True
        self.imgstill = pygame.image.load('images/dino_still.png')
        self.img1 = pygame.image.load('images/dinomove1.png')
        self.img2 = pygame.image.load('images/dinomove2.png')
        self.currentDino = self.imgstill
        self.info.dinos.append(self)
        self.distanceToCacti = []
        self.cactiHeight = []
        self.step = -1

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)


        self.color = (r, g, b)
        
    def drawDino(self):

        self.step += 1

        if self.step >= 6:
            self.step = 0

        if self.y != self.defaulty:
            self.currentDino = self.imgstill

        if self.step < 3:
            self.currentDino = self.img1
        elif self.step < 6:
            self.currentDino = self.img2

        d = pygame.transform.scale(self.currentDino, (125, 125))
        if showcolors:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x+self.width/3, self.y+10, self.width*2/3, self.height))
        self.drawLines()
        #pygame.draw.circle(screen, (0 ,255, 0), (self.x+10+self.width/2, self.y+10+self.height/2), self.width/2, 5)
        screen.blit(d, (self.x, self.y))


    def checkJump(self):
        if self.jumping == True:
            self.jump()

    def jump(self):

        MULTIPLIER = 2
        
        #check if starting jump
        if self.y == self.defaulty and self.up == True:
            self.jumpheight = 64
            self.up = True
            self.y -= self.jumpheight
            self.jumpheight /= MULTIPLIER

        #check if going up
        elif self.up and self.jumpheight > 1:
            self.y -= self.jumpheight
            self.jumpheight /= MULTIPLIER

        #check if at top of jump
        elif self.up and self.jumpheight == 1:
            self.up = False
            self.jumpheight = MULTIPLIER
            self.y += self.jumpheight
            self.jumpheight *= MULTIPLIER
        
        #check if going down
        elif self.up == False and self.y < self.defaulty:
            self.y += self.jumpheight
            self.jumpheight *= MULTIPLIER

        #check if jump done
        elif self.up == False and self.y == self.defaulty:
            self.jumping = False
            self.up = True

    def checkCollision(self): 

        #real dino position
        x1 = self.x+25
        x2 = x1 + self.width/2 - 15
        y1 = self.y+10
        y2 = y1 + self.height
        
        #loop through all obsticals
        for cactus in self.info.c:

            if cactus.type == "cactus":

                #real cactus position
                cx1 = cactus.x
                cx2 = cx1 + cactus.width
                cy1 = cactus.y + abs(100-cactus.height)
                cy2 = cy1 + cactus.height

                #check if bottom corners of dino are in cactus
                #bottom left corner collision
                if x1 > cx1 and x1 < cx2 and y2 > cy1 and y2 <= cy2:
                    return True
                elif x2 > cx1 and x2 < cx2 and y2 > cy1 and y2 <= cy2:
                    return True
            
            else:

                #real cactus position
                cx1 = cactus.x + 10
                cx2 = cx1 + 60
                cy1 = cactus.y + 30
                cy2 = cy1 + 40

                #check if bottom corners of dino are in cactus
                #bottom left corner collision
                if x1 > cx1 and x1 < cx2 and y2 > cy1 and y2 <= cy2:
                    return True
                elif x2 > cx1 and x2 < cx2 and y2 > cy1 and y2 <= cy2:
                    return True

                #top corners
                if x1 > cx1 and x1 < cx2 and y1 > cy1 and y1 <= cy2:
                    return True
                elif x2 > cx1 and x2 < cx2 and y1 > cy1 and y1 <= cy2:
                    return True

            
        return False


    def calculateDistances(self):
        for cactus in self.info.c:
            distance = cactus.x - self.x
            height = cactus.height

            if distance < 750:
                self.distanceToCacti.append((distance))
                self.cactiHeight.append(height)
            else:
                try:
                    self.distanceToCacti.remove(cactus)
                except ValueError:
                    pass  # do nothing!

    def drawLines(self):
        if showcolors:
            #create line between dino and cactus
            for cactus in self.info.c:
                if cactus.x <= 800 and cactus.x >= 50:
                    
                    if cactus.type == "cactus":

                        cactusx = -1
                        if cactus.img == cactus.medium:
                            cactusy = cactus.y+67
                        else:
                            cactusy = cactus.y+50

                        pygame.draw.line(screen, self.color, (self.x+self.width/2, self.y+self.height/2), (cactus.x, cactusy), width=3)

                    else:

                        pygame.draw.line(screen, self.color, (self.x+self.width/2, self.y+self.height/2), (cactus.x+40, cactus.y+40), width=3)
                

class Cactus:

    def __init__(self, info):
        
        self.info = info

        self.x = 1200
        self.y = 200
        self.medium = pygame.image.load('images/mediumcactus.png')
        self.big = pygame.image.load('images/bigcactus.png')
        self.img = None
        self.height = 0
        self.width = 50
        self.type = "cactus"

        num = random.randint(0,100)
        if(num < 90):
            self.img = self.medium
            self.height = 65
        else:
            self.img = self.big
            self.height = 100


    def draw(self):
        self.moveCactus()
        if showcolors:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y + abs(100-self.height), self.width, self.height))
        screen.blit(self.img, (self.x, self.y))

    def moveCactus(self):
        self.x -= self.info.gamespeed

class Bird:

    def __init__(self, info):
        self.info = info
        self.x = 1200
        #bird y is random
        num = random.randint(120, 240)
        if num < 160:
            num = 120
        else:
            num = 200
        self.y = num
        self.height = self.y
        self.bird1 = pygame.image.load('images/bird1.png')
        self.bird2 = pygame.image.load('images/bird2.png')
        self.currentBird = self.bird1
        self.flap = -1
        self.type = "bird"

    def draw(self):
        self.moveBird()
        if self.flap >= 8:
            self.flap = 0

        if self.flap < 4:
            self.currentBird = self.bird1
        elif self.flap < 8:
            self.currentBird = self.bird2

        b = pygame.transform.scale(self.currentBird, (100, 100))
        if showcolors:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x+10, self.y+30, 60, 40))
        #pygame.draw.circle(screen, (0 ,255, 0), (self.x+10+self.width/2, self.y+10+self.height/2), self.width/2, 5)
        screen.blit(b, (self.x, self.y))

        

    def moveBird(self):
        self.x -= self.info.gamespeed
        self.flap += 1
        

class Sand:

    def __init__(self, info):
        self.info = info
        self.x = 0
        self.y = 200
        self.rawimg = pygame.image.load('images/ground.png')
        self.img = pygame.transform.scale(self.rawimg, (2800, 100))

    def drawSand(self):
        self.moveSand()
        screen.blit(self.img, (self.x, self.y))

    def moveSand(self):
        global gamespeed
        if self.x > -1900:
            self.x -= self.info.gamespeed
        else:
            self.x = 0

class Sky:

    def __init__(self, info):
        self.info = info
        self.x = 0
        self.y = 130
        self.rawimg = pygame.image.load('images/sky.png')
        self.img = pygame.transform.scale(self.rawimg, (2800, 100))

    def drawSky(self):
        self.moveSky()
        screen.blit(self.img, (self.x, self.y))

    def moveSky(self):
        if self.x > -1900:
            self.x -= 3
        else:
            self.x = 0

#functions and globals for iD tech main.py 
dinobool = False
sandbool = False
cloudsbool = False
obsticalesbool = False

def makeDino():
    global dinobool
    dinobool = True

def makeSand():
    global sandbool
    sandbool = True

def makeClouds():
    global cloudsbool
    cloudsbool = True

def makeObsticales():
    global obsticalesbool
    obsticalesbool = True

        
#functions
def rungame():
    #iD tech globals
    global dinobool
    global sandbool
    global cloudsbool
    global obsticalesbool

    info = Info()

    if dinobool:
        mydino = Dino(info)

    if sandbool:
        sand = Sand(info)

    if cloudsbool:
        sky = Sky(info)

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
            exit()

        ### Restart program ###
        if keys[pygame.K_TAB]:
            running = False
            rungame()

        if keys[pygame.K_SPACE] and dinobool:
            if mydino.y == mydino.defaulty:
                print("jump!")
                mydino.jumping = True

        #check if obstical should spawn
        if obsticalesbool:
            info.makeObstical()
            info.removeObstical()

        #check if game should be faster
        info.makeHarder()

        #check dino collisions
        if dinobool and obsticalesbool:
            for d in info.dinos:
                d.calculateDistances()
                state = d.checkCollision()
                if state == True:
                    info.gameOver()

        if not sandbool:
            sand = None
        if not cloudsbool:
            sky = None
        info.drawScreen(sand, sky)
        pygame.display.update()
        time.sleep(0.025)

    pygame.quit()

if __name__ == "__main__":
#run program
    rungame()