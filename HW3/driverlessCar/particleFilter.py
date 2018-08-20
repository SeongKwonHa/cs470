# 20150790
'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.const import Const
import util

import random
import math

# Class: Particle Filter
# ----------------------
# Maintain and update a belief distribution over the probability of a car
# being in a tile using a set of particles.
class ParticleFilter(object):
    
    NUM_PARTICLES = 200
    
    # Function: Init
    # --------------
    # Constructer that initializes an ExactInference object which has
    # numRows x numCols number of tiles.
    def __init__(self, numRows, numCols):
        ''' initialize any variables you will need later '''
        self.belief = util.Belief(numRows, numCols)
        self.transprob = util.loadTransProb()
        self.probdic = {}
        self.realtemp = {}
        for key in self.transprob:
            if not key[0]in self.probdic:
                self.probdic[key[0]] = {}
                self.realtemp[key[0]] = key[1]
                self.probdic[key[0]][key[1]] = self.transprob[(key[0], key[1])]
            else:
                self.probdic[key[0]][key[1]] = self.transprob[(key[0], key[1])]
        # move form transprob -> prodic

        # make a random particle
        keys = self.probdic.keys()
        self.randomPart = {} # key = tile = (row, col)
        for i in range(self.NUM_PARTICLES):
            randomIndex = random.choice(keys)
            if not randomIndex in self.randomPart:
                self.randomPart[randomIndex] =1
            else:
                self.randomPart[randomIndex] += 1

        # update belief

        NumRow = self.belief.getNumRows()
        NumCol = self.belief.getNumCols()

        new = util.Belief(NumRow, NumCol, 0) # its 0 make linear times O(numtile)
        for key in self.randomPart:
            new.setProb(key[0], key[1], self.randomPart[key])

        new.normalize()
        self.belief = new
   
    # Function: Observe
    # -----------------
    # Updates beliefs based on the distance observation and your agents position.
    # The noisyDistance is a gaussian distribution with mean of the true distance
    # and std = Const.SONAR_NOISE_STD.The variable agentX is the x location of 
    # your car (not the one you are tracking) and agentY is your y location.
    def observe(self, agentX, agentY, observedDist):
        ''' your code here'''
        savedic= {}
        for key in self.randomPart:
            value = self.randomPart[key]
            mean = math.sqrt((abs(agentX - util.colToX(key[1]))) ** 2 + (abs(agentY - util.rowToY(key[0]))) ** 2)
            pdf = util.pdf(mean, Const.SONAR_STD, observedDist)
            newprob = value * pdf  # prob in that tile and that tile's prob
            savedic[key] = newprob
        # pdf -> fill into savedic


        count = 0
        for key in self.realtemp:
            count = count + 1
            self.realtemp[key] = self.realtemp[key]



        # random
        self.randomPart = {} # initializing
        for i in range(self.NUM_PARTICLES):
            randIndex = util.weightedRandomChoice(savedic)
            if not randIndex in self.randomPart:
                self.randomPart[randIndex] = 1
            else:
                self.randomPart[randIndex] += 1
                count = count +1

        NumRow = self.belief.getNumRows()
        NumCol = self.belief.getNumCols()

        new = util.Belief(NumRow, NumCol, 0)
        for key in self.randomPart:
            new.setProb(key[0], key[1], self.randomPart[key])

        new.normalize()
        self.belief = new

    # Function: Elapse Time
    # ---------------------
    # Update your inference to handle the passing of one heartbeat. Use the
    # transition probability you created in Learner  
    def elapseTime(self):
        ''' your code here'''
        temp = {}
        self.realtemp = {}
        for key in self.randomPart:
            for i in range (self.randomPart[key]):
                next = util.weightedRandomChoice(self.probdic[key])
                if next in temp:
                    temp[next] += 1
                    count = 1
                else:
                    temp[next] = 1
        self.randomPart = temp
        self.realtemp[count] = count

      
    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.    
    def getBelief(self):
        return self.belief
