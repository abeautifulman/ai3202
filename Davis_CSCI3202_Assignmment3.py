#Connor Davis
#CSCI 3202: Artificial Intelligence
#Assignment 3: A* Search

import numpy
import math
import sys

## DEFINE NODE PROPERTIES ##

#NODE PROPERTIES
#Location: (int, int)
#distanceToStart: int
#heuristic: int
#f: int
#parent: Node

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

class nodeProperties():
    def __init__(self):

        #Start and End variables
        self.isStart = False
        self.isEnd = False

        #Open square, Mountain, or Wall?
        #0 is an open square, 1 is moutain, 2 is a wall
        self.tileValue = None

        #Set to the cost of the chosen move
        self.moveCost = 0

        #X and Y coordinates
        #NOTE: X counts up from 0 left->right, Y counts up from 0 top->bottom
        self.locationX = None
        self.locationY = None

        #Distance from start node & heuristic values
        self.distanceToStart = None
        self.heuristic = None
        self.f = None

        #Parent node and list of neighbors
        self.parent = None
        self.neighbors = []

        #Determine cost via Horizontal/Vertical or Diagonal
        self.isHV = False
        self.isDiag = False

## GET LOCATION ##
    def setLocation(self, xValue, yValue):
        self.locationX = xValue
        self.locationY = yValue

###################################################

## FIND NEIGHBORS ##
def findNeighbors(node):

    neighborList = []

    for z in locationList:

        #Row above
        if node.locationY - 1 == z.locationY:
            #Top Left
            if node.locationX - 1 == z.locationX:
                z.isDiag = True
                neighborList.append(z)
            #Node Above
            elif node.locationX == z.locationX:
                z.isHV = True
                neighborList.append(z)
            #Top Right
            elif node.locationX + 1 == z.locationX:
                z.isDiag = True
                neighborList.append(z)

        #Same row
        if node.locationY == z.locationY:
            #Left
            if node.locationX - 1 == z.locationX:
                z.isHV = True
                neighborList.append(z)
            #Right
            elif node.locationX + 1 == z.locationX:
                z.isHV = True
                neighborList.append(z)

        #Row below
        if node.locationY + 1 == z.locationY:
            #Bottom Right
            if node.locationX - 1 == z.locationX:
                z.isDiag = True
                neighborList.append(z)
            #Node Below
            elif node.locationX == z.locationX:
                z.isHV = True
                neighborList.append(z)
            #Bottom Right
            elif node.locationX + 1 == z.locationX:
                z.isDiag = True
                neighborList.append(z)

    return neighborList

###################################################

# A STAR SEARCH

def aStarSearch(node, heuristicType, totalCost):

    print "Searching from: [", node.locationX, ",", node.locationY, "]"

    print "Current total cost:", totalCost

    #Make a list to keep track of how much every move costs
    costList = []

    neighbors = []
    neighbors = findNeighbors(node)

    #Set bestMove to obnoxious value to begin with
    bestMove = 1000000

    #Loops through list of neighbors
    for z in neighbors:

        #print z.locationX, z.locationY, "Neighbor Coordinates"

        #Reset cost to 0 for each node
        cost = 0

        #The end node is within reach
        if z.locationX == 9 and z.locationY == 0:
        #if z.isEnd == True:

            ######
            if z.isDiag == True:
                z.f = 14
                cost = 14
                if z.tileValue == 1:
                    z.f = 24
                    cost = 24
            #Horizontal/Vertical moves
            elif z.isHV == True:
                z.f = 10
                cost = 10
                if z.tileValue == 1:
                    z.f = 20
                    cost = 20
            ######

            print "Sweet! We found the goal.", "\n"
            totalCost = totalCost + z.f
            print "The total cost of the search is", totalCost


            #TESTCODE FOR PARENTS AND PATHS
            z.parent = node

            #Get the path
            algorithmPath(z)

            countNodesVisited(z)


            return

        #We haven't found the end yet, keep looking
        #Make sure it's not a wall

        else:
            if z.tileValue != 2:

                #Calculate base cost without heuristic
                #Cost of 10 for vert/horiz movements, 14 for diagonals (non-mountain)

                #Diagonal moves
                if z.isDiag == True:
                    z.f = 14
                    cost = 14
                    if z.tileValue == 1:
                        z.f = 24
                        cost = 24

                #Horizontal/Vertical moves
                elif z.isHV == True:
                    z.f = 10
                    cost = 10
                    if z.tileValue == 1:
                        z.f = 20
                        cost = 20

                cost = cost + heuristic(z, heuristicType)

                z.moveCost = cost
                costList.append(z)

                #print costList

                for nodes in costList:
                    if nodes.moveCost < bestMove:
                        bestMove = nodes.moveCost
                       # print bestMove, "This is the best move"

                '''
                #loop through nodes in costList
                for node in costList:
                    #If cost of move is cheaper than current "Best" cost


                    if node.moveCost < bestMove:
                        #Update the bestMove to reflect this
                        bestMove = node.moveCost
                        #print bestMove, "This is the best move"
                    '''


    #Loop through nodes in costList
    for nodes in costList:
        #If we find the best move
        if nodes.moveCost == bestMove:
            break # End the for loop here. In cases where two equal options exist, we were not taught how to determine which node to analyze
    nodes.parent = node
    totalCost = totalCost + nodes.f
    print  "After the best move, we still need to go:", bestMove, '\n'
    #print "[" , node.locationX, ",", node.locationY, "]" #PRINT PATH???????????
    aStarSearch(nodes, heuristicType, totalCost)




def heuristic(node, type):

   #Manhattan Distance
   if type == 1:

       xDistance = (9 - node.locationX) * 10
       yDistance = (0 + node.locationY) * 10
       manhattan = xDistance + yDistance
       return manhattan

   #Pythagorean Theorem
   if type == 2:

       xDistance = (9 - node.locationX) * 10
       yDistance = (0 + node.locationY) * 10
       pythag = math.sqrt(math.pow(xDistance, 2) + (math.pow(yDistance, 2)))
       return pythag * (1 + 1/10)

def algorithmPath(item):

    if item.locationX == 0 and item.locationY == 7:
        algoSearchPath.append(item)
        return
    else:
        algoSearchPath.append(item)
        algorithmPath(item.parent)

def countNodesVisited(item):
    if item.locationX == 0 and item.locationY == 7:
        nodesVisited.append(item)
        return
    else:
        nodesVisited.append(item)
        countNodesVisited(item.parent)
####################################################################


## MAIN ##

## INITIALIZING THE WORLD STATE IN A 3D GRAPH ##

whichMap = sys.argv[1]
whichHeuristic = int(sys.argv[2])

worldMap = numpy.genfromtxt(whichMap)

#List of all nodes in 2D Array
locationList = []

#Algorithm Search Path
algoSearchPath = []

#Total Cost Variable
totalCost = 0

#List to count nodes visited
nodesVisited = []

#Starting X and Y values
x = -1
y = -1

#Get all of the nodes into a graph
#Counting up as we move down the rows, and across the rows from left to right, we set x and y

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

#RUN A STAR SEARCH

aStarSearch(locationList[70], whichHeuristic, totalCost)

print "This is the path that was taken from start to end:"

while algoSearchPath != []:
    z = algoSearchPath.pop()
    print 'x:', z.locationX, ' y:', z.locationY

print "The number of nodes visited was:"
print len(nodesVisited)


    #Document explanation of what arguments do in README
    #README must also explain how results vary for 2 heuristics


#Output
#Cost of path, locations along the path, and # of locations evaluated
