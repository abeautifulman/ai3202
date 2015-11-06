#Connor Davis
#CSCI3202: Artificial Intelligence
#Assignment 7: Sampling and Babe Nets

from __future__ import division
import random

#Calculate exact probability and error between it and prior sampling estimation

#Need to do rejection sampling
#Calculate exact probability and error between it and rejection sampling estimation

#P1
#a .48
#b .75
#c .4
#d 0

#P3
#a .49
#b .7037037037037..
#c .4
#d 0

############################################### #######


class node():
    def __init__(self, name):
        self.name = name

        #True/False conditions
        #Might need quick function to reset all of these if left global? Probably don't need to be global

        self.cloudy_condition = False
        self.rain_condition = False
        self.sprinkler_condition = False
        self.wet_grass_condition = False

        #List that will become "List of lists" for all of our calculated sample combinations via RhondaNumbers
        self.samples = []

    def reset_conditions(self):
        #Reset all conditions?
        self.cloudy_condition = False
        self.rain_condition = False
        self.sprinkler_condition = False
        self.wet_grass_condition = False
        self.samples = []
        return

######################################################

#Rejection?
'''
def rejection_sampling_calculation(node):
    #Always get a float between 0 and 1
    randomnumber = random.random()
    #print randomnumber

    #P(C=true)
    cloudy_true_counter = 0
    cloudy_false_counter = 0

    for x in Rhonda_Samples:
        if x < node.prob_cloudy_true:
            cloudy_true_counter = cloudy_true_counter + 1
        else:
            cloudy_false_counter = cloudy_false_counter + 1

    print cloudy_true_counter, "is number of Cloudy+'s"
    print cloudy_false_counter, "is number of Cloudy-'s"
    '''


def diagram_traversal(node):

    #Loop through all 100 of Rhonda_Numbers, generating 25 Samples in the process
    #these are combinations of true/false states for Cloudy, Sprinkler, Rain, and Wet Grass

    ###
    #Need to make list of lists to contain pairings of true/false conditions generated with every sample
    ###

    counter = 0
    i = 0

    while i < 100:
        counter = counter +1

        #print counter

        ##########
        #Cloudy
        #print Rhonda_Numbers[i]

        if Rhonda_Numbers[i] < .50:
            node.cloudy_condition = True
        else:
            node.cloudy_condition = False
        i = i+1

        ##########
        #Sprinkler
        #print Rhonda_Numbers[i]

        #Cloudy True
        if node.cloudy_condition == True:
            if Rhonda_Numbers[i] < .10:
                node.sprinkler_condition = True

        #Cloudy False
        elif node.cloudy_condition == False:
            if Rhonda_Numbers[i] < .50:
                node.sprinkler_condition = True
        i = i+1

        ##########
        #Rain
        #print Rhonda_Numbers[i]

        #Cloudy True
        if node.cloudy_condition == True:
            if Rhonda_Numbers[i] < .80:
                node.rain_condition = True

        elif node.cloudy_condition == False:
            if Rhonda_Numbers[i] < .20:
                node.rain_condition = True
        i = i+1

        ##########
        #Wet Grass
        #print Rhonda_Numbers[i]

        #Sprinkler True, Rain True
        if node.sprinkler_condition == True and node.rain_condition == True:
            if Rhonda_Numbers[i] < .99:
                node.wet_grass_condition = True

        #Sprinkler True, Rain False
        elif node.sprinkler_condition == True and node.rain_condition == False:
            if Rhonda_Numbers[i] < .90:
                node.wet_grass_condition = True

        #Sprinkler False, Rain True
        elif node.sprinkler_condition == False and node.rain_condition == True:
            if Rhonda_Numbers[i] < .90:
                node.wet_grass_condition = True

        #Sprinkler False, Rain False
        #elif node.sprinkler_condition == False and node.rain_condition == False:
        #    node.wet_grass_condition = False
        i = i+1

        #Print statement for samples generated
        #print "C", node.cloudy_condition, "\n", "S", node.sprinkler_condition, "\n", "R", node.rain_condition, "\n", "WG", node.wet_grass_condition, "\n"

        superSampleList.append([node.cloudy_condition, node.sprinkler_condition, node.rain_condition, node.wet_grass_condition])

        node.reset_conditions()

def prior_sampling(masterList):

    #Initialize counters for each event
    cloudy_counter = 0
    sprinkler_counter = 0
    rain_counter = 0
    wetgrass_counter = 0

    #extra counters for special events
    cloudy_given_rainy_counter = 0
    sprinkler_given_wetgrass_counter = 0
    sprinkler_given_cloudy_and_wetgrass_counter = 0

    #Count number of times an event occurs in the sample list
    for item in masterList:
        #Cloudy
        if item[0] == True:
            cloudy_counter += 1
        #Sprinkler
        if item[1] == True:
            sprinkler_counter += 1
        #Rain
        if item[2] == True:
            rain_counter += 1
            if item[0] == True:
                cloudy_given_rainy_counter += 1
        #Wetgrass
        if item[3] == True:
            wetgrass_counter += 1
            if item[1] == True:
                sprinkler_given_wetgrass_counter += 1
        #Last Probability
        #Are Cloudy and Wetgrass true?
        if item[0] == True and item[3] == True:
            #is sprinkler true?
            if item[1] == True:
                sprinkler_given_cloudy_and_wetgrass_counter += 1


    #Calculating Prior Sampling Answers
    #Divide by total number of samples
    prob_cloudy = cloudy_counter/25
    prob_cloudy_given_rainy = cloudy_given_rainy_counter / rain_counter
    prob_sprinkler_given_wetgrass = sprinkler_given_wetgrass_counter / wetgrass_counter

    if sprinkler_given_cloudy_and_wetgrass_counter == 0:
        print 'No events where (s=true|c=true, wg=true), it is therefore 0'
    #prob_sprinkler_given_cloudy_and_wetgrass = sprinkler_counter / sprinkler_given_cloudy_and_wetgrass_counter
    prob_sprinkler_given_cloudy_and_wetgrass = 0

    #Printing out Prior Sampling answers
    print "Prior Sampling Answers:"
    print "P(c) is ", prob_cloudy
    print "P(c = true|r = true) is", prob_cloudy_given_rainy
    print "P(s = true|wg = true) is", prob_sprinkler_given_wetgrass
    print "P(s = true|c=true, wg = true) is", prob_sprinkler_given_cloudy_and_wetgrass, '\n'


def rejection_sampling():

    cloudy_true_counter = 0
    cloudy_false_counter = 0
    sprinkler_true_counter = 0
    sprinkler_false_counter = 0
    i = 0

    sprinkler_condition = False
    rain_condition = False

    #P(C)
    while i < 100:
        if Rhonda_Numbers[i] < .50:
            cloudy_true_counter += 1
        else:
            cloudy_false_counter += 1
        i = i+1

    cloudy_true_counter = cloudy_true_counter/100

    print "Rejection Sampling Answers:"
    print "P(c) is ", cloudy_true_counter

    ####################
    #P(C|R)
    i = 0
    rain_and_cloudy_true_counter = 0
    rain_true_counter = 0

    #You will use 2 of Rhonda's numbers for each iteration

    while i < 100:
        #Cloudy
        #Check if odd number gives cloudy a True or False.
        if Rhonda_Numbers[i] < .50:
            cloudy_condition = True
            i += 1

        else:
            cloudy_condition = False
            i += 1

        #Rain
        if cloudy_condition == True:
                if Rhonda_Numbers[i] < .80:
                    rain_true_counter += 1
                    rain_and_cloudy_true_counter += 1
                    rain_condition = True

        elif cloudy_condition == False:
                if Rhonda_Numbers[i] < .20:
                    rain_true_counter += 1
                    rain_condition = True
        i += 1

    print "P(c = true|r = true) is", rain_and_cloudy_true_counter/rain_true_counter

    ####################
    #P(S|WG)
    i = 0
    rain_and_cloudy_true_counter = 0
    rain_true_counter = 0
    wet_grass_counter = 0
    sprinkler_and_cloudy_true_counter = 0
    sprinkler_true_cloudy_false_counter = 0
    sprinkler_true_wet_grass_true_counter = 0

    sprinkler_true_rain_true = False
    sprinkler_true_rain_false = False
    sprinkler_false_rain_true = False
    sprinkler_false_rain_false = False

    while i < 100:
        #Cloudy
        #Check if odd number gives cloudy a True or False.
        if Rhonda_Numbers[i] < .50:
            cloudy_condition = True
            i += 1
        else:
            cloudy_condition = False
            i += 1

        #sample Sprinkler as a result of Cloudy
        if cloudy_condition == True:
                if Rhonda_Numbers[i] < .10:
                    sprinkler_true_counter += 1
                    #sprinkler_and_cloudy_true_counter += 1
                    sprinkler_condition = True
                    i += 1
                else:
                    i += 1

        elif cloudy_condition == False:
                if Rhonda_Numbers[i] < .50:
                    sprinkler_true_counter += 1
                    #sprinkler_true_cloudy_false_counter += 1
                    sprinkler_condition = True
                    i += 1
                else:
                    i += 1
        else:
            sprinkler_condition = False
            i += 1

        #sample Rain, keeping track of when sprinkler has also been true
        if cloudy_condition == True:
                if Rhonda_Numbers[i] < .80:
                    rain_true_counter += 1
                    rain_condition = True
                    if sprinkler_condition == True:
                        sprinkler_true_rain_true = True
                        i += 1
                    else:
                        sprinkler_false_rain_true = True
                        i += 1
                else:
                    if sprinkler_condition == True:
                        sprinkler_true_rain_false = True
                        i += 1
                    else:
                        i += 1

        elif cloudy_condition == False:
                if Rhonda_Numbers[i] < .20:
                    rain_true_counter += 1
                    rain_condition = True
                    if sprinkler_condition == True:
                        sprinkler_true_rain_true = True
                        i += 1
                    else:
                        sprinkler_false_rain_true = True
                        i += 1
                else:
                    if sprinkler_condition == True:
                        sprinkler_true_rain_false = True
                        i += 1
                    else:
                        sprinkler_false_rain_false = True
                        i += 1

        #Wet Grass
        if sprinkler_true_rain_true == True:
            if Rhonda_Numbers[i] < .99:
                wet_grass_condition = True
                wet_grass_counter += 1
                sprinkler_true_wet_grass_true_counter += 1
                i += 1
            else:
                i += 1

        elif sprinkler_true_rain_false == True:
            if Rhonda_Numbers[i] < .90:
                wet_grass_condition = True
                wet_grass_counter += 1
                sprinkler_true_wet_grass_true_counter += 1
                i += 1
            else:
                i += 1

        elif sprinkler_false_rain_true == True:
            if Rhonda_Numbers[i] < .90:
                wet_grass_condition = True
                wet_grass_counter += 1
                i += 1
            else:
                i += 1

        elif sprinkler_false_rain_false == True:
            if Rhonda_Numbers[i] < .00:
                wet_grass_condition = True
                wet_grass_counter += 1
                i += 1
            else:
                i += 1
        else:
            i += 1

        #Reset conditions for next loop
        cloudy_condition = False
        sprinkler_condition = False
        rain_condition = False
        wet_grass_condition = False
        sprinkler_true_rain_true = False
        sprinkler_true_rain_false = False
        sprinkler_false_rain_false = False
        sprinkler_false_rain_true = False



        #Sample cloudy first

    #print "Rejection Sampling Answers:"
    #print "P(c) is ", cloudy_true_counter
    #print "P(c = true|r = true) is", rain_and_cloudy_true_counter/rain_true_counter
    print "P(s = true|wg = true) is", sprinkler_true_wet_grass_true_counter / wet_grass_counter
    print "P(s = true|c=true, wg = true) is", 0


######################################################

def main():
    diagram_traversal(test_node)

    #Print statements for samples generated
    #print "Cloudy, Sprinkler, Rain, Wet Grass"
    #print '\n'.join(str(row) for row in superSampleList)

    #Prior Sampling
    prior_sampling(superSampleList)

    #Rejection Sampling
    rejection_sampling()

Rhonda_Numbers = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,
0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	0.8,	0.97,
0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 0.6,	0.68,	0.36,	0.67,
0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	0.83,	0.96,	0.41,	0.65,
0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	0.97,	0.95,	0.01,	0.62,	0.32,
0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,
0.9,	0.0,	0.91,	0.01]

######################################################

#initialize the nodes we'll need
test_node = node("test")

#List of Lists for all samples generated
superSampleList = []

main()

#print Rhonda_Samples