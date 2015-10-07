#Connor Davis
#CSCI 3202: Artificial Intelligence
#Assignment 5: Markov Decision Processes

import numpy
import math
import sys


### Define system arguments ###

print '\n'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv), '\n'


### Define node properties ###
class nodeProperties():
    def __init__(self):

        #Open square, Mountain, or Wall?
        #0 is an open square, 1 is moutain, 2 is a wall
        #3 is Snake, 4 is Barn, 50 is Apples
        #Used to calculate self.reward
        self.tileValue = None

        #X and Y coordinates
        #NOTE: X counts up from 0 left->right, Y counts up from 0 top->bottom
        self.locationX = None
        self.locationY = None

        #List of neighboring nodes
        self.neighbors = []

        #Utility and Reward innate to Square
        #All nodes start with Utility of zero
        #newUtility is updated via valueIteration()
        self.currentUtility = 0
        self.newUtility = 0
        self.reward = 0

        #Directional stuff
        self.isNorth = False
        self.isSouth = False
        self.isEast = False
        self.isWest = False

    ## GET LOCATION ##
    def setLocation(self, xValue, yValue):
        self.locationX = xValue
        self.locationY = yValue

    def setDisplay(self):
        #Display[self.locationY][self.locationX] = str(self.newUtility).zfill(9)
        Display[self.locationY][self.locationX] = str(self.newUtility)


###################################################


## Find all neighboring nodes that might be accessed in making a move ##
def findNeighbors(node):

    neighborList = []

    for z in locationList:

        #Row above
        if node.locationY - 1 == z.locationY:
            #Node Above
            if node.locationX == z.locationX:
                z.isNorth = True
                neighborList.append(z)

        #Same row
        if node.locationY == z.locationY:
            #Left
            if node.locationX - 1 == z.locationX:
                z.isWest = True
                neighborList.append(z)
            #Right
            elif node.locationX + 1 == z.locationX:
                z.isEast = True
                neighborList.append(z)

        #Row below
        if node.locationY + 1 == z.locationY:
            #Node Below
            if node.locationX == z.locationX:
                z.isSouth = True
                neighborList.append(z)

    return neighborList


### Get innate rewards from node tile values (mountain, snake, etc.)
def calcInnateReward(node):

    #Value 1 = Mountain = Reward -1
    if node.tileValue == 1:
        node.reward = -1

    #Value 2 = Wall = Reward 0
    elif node.tileValue == 2:
        node.reward = 0

    #Value 3 = Snake = Reward -2
    elif node.tileValue == 3:
        node.reward = -2

    #Value 4 = Barn = Reward +1
    elif node.tileValue == 4:
        node.reward = 1

    #Value 50 = APPLES = Reward +50
    elif node.tileValue == 50:
        node.reward = 50


### Calculate a node's utility ###
def calcUtility(node, utilityList):

    #Crunches numbers to determine node utility
    #New utility = Innate reward + Living Reward * Best Move

    node.newUtility = node.reward + (gamma * max(utilityList))

    #Returns "node.newUtility"
    #Also need to return direction - could be stored in dictionary?


    #Need to return node's utility and max


### Determine best possible move after getting neighbors ###
def calcNeighborMoves(node):

    # Reset neighbors so that old North/South/East/West values don't remain between node evaluations
    resetNeighbors()

    # Get neighbors to North, South, East, and West.
    neighbors = []
    neighbors = findNeighbors(node)

    #initialize directional rewards in case the node does not exist
    northUtility = 0
    southUtility = 0
    eastUtility = 0
    westUtility = 0

    #Make variables for moving in each direction and get innate reward
    for nodes in neighbors:
        if nodes.isNorth == True:
            northUtility = nodes.currentUtility
        elif nodes.isSouth == True:
            southUtility = nodes.currentUtility
        elif nodes.isEast == True:
            eastUtility = nodes.currentUtility
        elif nodes.isWest == True:
            westUtility = nodes.currentUtility

    #Calculate % chance of actually moving in the desired direction, for each direction

    northUtility = (.8 * northUtility) + (.1 * eastUtility) + (.1 * westUtility)
    southUtility = (.8 * southUtility) + (.1 * eastUtility) + (.1 * westUtility)
    eastUtility = (.8 * eastUtility) + (.1 * northUtility) + (.1 * southUtility)
    westUtility = (.8 * westUtility) + (.1 * northUtility) + (.1 * southUtility)

    #Add final reward for each move (N,S,E,W) to a list so finding the max is ez
    utilityList = []

    utilityList.append(northUtility)
    utilityList.append(southUtility)
    utilityList.append(eastUtility)
    utilityList.append(westUtility)

    return utilityList

def resetNeighbors():
    for node in locationList:
        node.isNorth = False
        node.isSouth = False
        node.isEast = False
        node.isWest = False


### Function that looks at all nodes and iterates their values (utilities) ###
def valueIteration():

    convCounter = 0

    #Termination Condition
    #while delta > E * ((1-gamma)/gamma):
    while True:

        #U = U_PRIME
        for nodes in locationList:
            nodes.currentUtility = nodes.newUtility

        delta = 0

        #For state in states...
        for nodes in locationList:
            #Check all of possible neighbor moves for best move
            rewardList = calcNeighborMoves(nodes)
            #Update Utility
            calcUtility(nodes, rewardList)

            #print("Value:", nodes.tileValue, "Current Utility:", nodes.currentUtility, "New Utility:", nodes.newUtility, "Reward:", nodes.reward)
            #makeDisplay()

            if abs(nodes.currentUtility - nodes.newUtility) > delta:
                delta = abs(nodes.currentUtility - nodes.newUtility)

        convCounter += 1

        if delta < E * ((1-gamma)/gamma):
            print "# of Value Iterations =",convCounter
            #Testing to see if utility values iterate as intended
            #makeDisplay()
            break

def makeDisplay():
    print
    for node in locationList:
        node.setDisplay()
    for x in range(8):
        print (Display[x])


#Pathing to end -
    #Find Starting node = DONE
    #Print his x,y = DONE
    #Find ALL of his neighbors = DONE
    #Of the neighbors, make a list that does not contain walls = DONE

    #Change his x,y to the max neighbor value variable
    #repeat

def finalPath(node):

    print "Currently at node:", "(", node.locationX, ",", node.locationY, ") with utility", node.currentUtility

    #Set variable to hold best neighboring node
    bestNeighbor = None
    bestNeighborUtility = None

    #Set list to hold possible neighbors that are NOT walls
    kosherNeighbors = []
    kosherNeighborUtilities = []

    #Get neighbors, set best neighbor to bestNeighbor value
    neighbors = findNeighbors(node)

    #Testing to make sure it finds all of the neighbors
    '''
    print ("Neighbors are:")
    for q in neighbors:
        print "(", q.locationX,",",q.locationY, ")"
    '''

    #Make sure it's not a wall
    for x in neighbors:
        if x.tileValue != 2:
            kosherNeighbors.append(x)
            kosherNeighborUtilities.append(x.currentUtility)

    #Testing to make sure node doesn't add walls to list
    '''
    print("Kosher neighbors are:")
    for m in kosherNeighbors:
        print "(", m.locationX, "," ,m.locationY, ")"
    '''

    bestNeighborUtility = max(kosherNeighborUtilities)

    for y in locationList:
        if y.currentUtility == bestNeighborUtility:
            bestNeighbor = y

    #print "Moving to node:", "(", bestNeighbor.locationX, "," ,bestNeighbor.locationY, ")"

    #Find the best neighbor in the list
    for z in locationList:
        if z.currentUtility == bestNeighborUtility:
            print "Move to node:", "(", z.locationX, ",", z.locationY, ")" '\n'#, "with utility:", z.currentUtility
            if z.locationX == 9 and z.locationY == 0:
                print "Utility of terminal node is:", z.currentUtility
                print "The terminal node has been found!! Yay!"

                break
            finalPath(z)



####################################################################


## MAIN ##

### Initialize the map into a 2D grid ###
whichMap = sys.argv[1]
worldMap = numpy.genfromtxt(whichMap)

#List of all nodes in 2D Array
locationList = []

#Global Gamma, Delta values for calculating Utility
#Delta = Threshold
delta = 0
#Gamma = "Discout Factor"
gamma = 0.9
#Default Epsilon is .5, but want as argument to change if needed
E = float(sys.argv[2])

#Starting node
startingNode = None

#Starting X and Y values
x = -1
y = -1

### Get all of the nodes into a graph ###
### y increases as we move down the rows, x increases as we move across the rows from left to right ###

for row in worldMap:

    #Reset x value for each row change
    x = -1
    #Increment y value as we move down
    y = y+1

    for item in row:

        #Increment x value as we move across
        x = x+1

        #Create node, set location
        node = nodeProperties()
        node.setLocation(x, y)
        #print (node.locationX , node.locationY)

        #Set tile value
        node.tileValue = item

        locationList.append(node)

print worldMap, '\n'


### Set up stuff for pretty printing ###
Display = [[0 for x in range(10)] for x in range(8)]

### Get all innate Reward ###
for node in locationList:
    calcInnateReward(node)

### Call the bad boy ###
valueIteration()

#Get starting node
for nodes in locationList:
        #Update utility one last time
        nodes.currentUtility = nodes.newUtility
        if nodes.locationX == 0 and nodes.locationY == 7:
            startingNode = nodes

print '\n', "Printing path from beginning to end and node utility...", '\n'

finalPath(startingNode)