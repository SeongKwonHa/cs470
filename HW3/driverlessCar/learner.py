# 20150790
'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
import util

# Class: Learner
# ---------------
# This class is in charge of observing cars drive around and figuring out a
# probability distribution over transitions that cars make.
class Learner(object):

    # Function: Init
    # ---------------
    # Create any extra variables that you need to calculate the transition
    # probabilities for each tile.
    def __init__(self):
        ''' your code here '''
        self.info = {}


    # Function: Note Car Mode
    # ----------------------
    # This function is called once for each car on every heart beat of the
    # program. OldPos was the old position of the car and newPos is the position
    # of the car after the heartbeat. The code provided takes these positions
    # and extracts the corresponding tiles. Update any relevant variables with
    # this new datapoint.
    def noteCarMove(self, oldPos, newPos):
        oldRow, oldCol = util.yToRow(oldPos.y), util.xToCol(oldPos.x)
        newRow, newCol = util.yToRow(newPos.y), util.xToCol(newPos.x)
        oldTile = (oldRow, oldCol)
        newTile = (newRow, newCol)
        ''' your code here '''

        if not oldTile in self.info:
            self.info[oldTile] = {}
            self.info[oldTile][newTile] = 1
        else:
            if not newTile in self.info[oldTile]:
                self.info[oldTile][newTile] = 1
            else:
                self.info[oldTile][newTile] += 1


    # Function: Save Transition Prob
    # ------------------------------
    # After the algorithm has finished running, saveTransitionProb is called.
    # Put any relevant data you have into the transProb dictionary and call
    # util.saveTransProb. You will be using this dictionary in your inference
    # algorithms.
    def saveTransitionProb(self, transFile):
        transProb = {}
        ''' your code here '''

        for oldTile in self.info.keys():
            sum = (float)(0)
            for newTile in self.info[oldTile].keys():
                sum += self.info[oldTile][newTile]

            for newTile in self.info[oldTile].keys():
                val = self.info[oldTile][newTile]/sum
                self.info[oldTile][newTile] = val

        for oldTile in self.info.keys():
            for newTile in self.info[oldTile].keys():
                transProb[(oldTile,newTile)] = self.info[oldTile][newTile]

        util.saveTransProb(transProb, transFile)
