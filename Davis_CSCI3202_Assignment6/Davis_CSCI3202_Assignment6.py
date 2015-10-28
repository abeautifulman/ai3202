#Connor Davis
#CSCI 3202: Artificial Intelligence
#Assignment 6: Bayesian Networks

import Queue
import argparse


#Create our node class
#Keep track of all parentList, childList, and related conditional probabilities

class Node():
    def __init__(self,name):

        self.name = name
        self.parentList = []
        self.childList = []
        self.related_conditional_probabilities = {}

#Create a table that contains all related conditional probabilities for the given node

    def create_related_conditional_probabilities(self):

        origin =["pHigh", "pLow", "sTrue", "sFalse", "pLow_sTrue", "pLow_sFalse", "pHigh_sTrue", "pHigh_sFalse", "cTrue", "cFalse", "xTrue", "xFalse", "dTrue", "dFalse"]

        #Create a dictionary with the above info
        self.related_conditional_probabilities = dict.fromkeys(origin, None)

        #Mark up all possible related conditional probabilities
        #These will be hard coded values

        #Pollution - High or Low
        if self.name == "pollutionNode":
            self.related_conditional_probabilities["pHigh"] = P
            self.related_conditional_probabilities["pLow"] = p

        #Smoker? Yes or No
        elif self.name == "smokerNode":
            self.related_conditional_probabilities["sTrue"] = s
            self.related_conditional_probabilities["sFalse"] = S

        #Cancer? Yes or No
        elif self.name == "cancerNode":
            self.related_conditional_probabilities["pLow_sTrue"] = 0.03
            self.related_conditional_probabilities["pHigh_sTrue"] = 0.05

            self.related_conditional_probabilities["pLow_sFalse"] = 0.001
            self.related_conditional_probabilities["pHigh_sFalse"] = 0.02

            self.related_conditional_probabilities["pLsT_parentList"] = 0.03 * p * s
            self.related_conditional_probabilities["pHsT_parentList"] = 0.05 * P * s

            self.related_conditional_probabilities["pLsF_parentList"] = 0.001 * p * S
            self.related_conditional_probabilities["pHsF_parentList"] = 0.02 * P * S

        #Was the xRay positive? Yes or No
        elif self.name == "xrayNode":
            self.related_conditional_probabilities["cTrue"] = 0.90
            self.related_conditional_probabilities["cFalse"] = 0.20

        #Does the subject have breathing difficulty? Yes or No
        elif self.name == "dyspnoeaNode":
            self.related_conditional_probabilities["cTrue"] = 0.65
            self.related_conditional_probabilities["cFalse"] = 0.30



#For parsing characters
class parsingQueue():
    def __init__(self,size):
        self.queue = Queue.Queue()
        self.size = size
    def addChar(self,char):
        self.queue.put(char)


#Function to parse given arguments
def argumentParser():

    parser = argparse.ArgumentParser(description='Decide which form of reasoning to use')
    parser.add_argument('-g', action="store", dest="conditional_probability", help="Incorrect syntax - must use quotes")
    parser.add_argument('-j', action="store", dest="joint_probability")
    parser.add_argument('-m', action="store", dest="marginal_probability")
    parser.add_argument('-p', action="store", dest="set_prior")
    args=parser.parse_args()
    return args

def pickReasoning(arguments):

    #Prior Flag set?
    if arguments.set_prior != None:
        setPrior(arguments.set_prior)

    #Conditional Probabilitiy?
    if arguments.conditional_probability != None:
        conditionalProbability(arguments.conditional_probability)

    #Joint Probability?
    if arguments.joint_probability != None:
        jointProbability(arguments.joint_probability)

    #Marginal Probabiliity?
    if arguments.marginal_probability != None:
        marginalProbability(arguments.marginal_probability)

def argParser(args):

    bool = False
    argumentList = []

    for char in args:
        if char.isupper():
            argumentList.append((char,"distribution"))
        else:
            if char == '~':
                bool = True
            else:
                if bool == True:
                    argumentList.append((char,"false"))
                    bool = False
                else:
                    argumentList.append((char,"true"))
    return argumentList

def parseConditionalArguments(args):
    bool = False
    a = []
    b = []
    a1 = True
    for char in args:
        if char == "|":
            a1 = False
        else:
            if a1 == True:
                if char == '~':
                    bool = True
                else:
                    if bool == True:
                        a.append((char,"false"))
                        bool = False
                    else:
                        a.append((char,"true"))
            else:
                if char == '~':
                    bool = True
                else:
                    if bool == True:
                        b.append((char,"false"))
                        bool = False
                    else:
                        b.append((char,"true"))
    return a,b

def getReasoningname(case):
    reasoningname = None
    if case == [("d","true")]:
        reasoningname = "diagnostic"
    elif case == [("s","true")]:
        reasoningname = "predictive"
    elif case == [("c","true")] or case == [("c","true"),("s","true")] or case == [("s","true"),("c","true")]:
        reasoningname = "intercausal"
    elif case == [("d","true"),("t","true")] or [("t","true"),("d","true")]:
        reasoningname = "intercausal"
    return reasoningname

def conditionalProbability(args):
    cP = 0
    a,b = parseConditionalArguments(args)
    reasoningname = getReasoningname(b)
    if reasoningname == None:
        print "Incorrect input: please try again"
    else:
        print 'Conditional probability for:',args,"using",reasoningname,"reasoning."
    for arg in a:
        for arg2 in b:
            if arg == arg2:
                cP = 1
                reasoningname = None

    #Predictive Reasoning
    if reasoningname == "predictive":
        if a == [("p","false")]:
            cP = network_graph_bayes[0].related_conditional_probabilities["pHigh"]
        elif a == [("x","true")]:
            cP = mProbCalculation([("x","sTrue")])
            #p(x=pos | smokerNode) = p(x,s,c,p) / p(s,c,p)
        elif a == [("d","true")]:
            cP = mProbCalculation([("d","sTrue")])
        elif a == [("c","true")]:
            cP = mProbCalculation([("c","sTrue")])

    #Diagnostic Reasoning
    elif reasoningname == "diagnostic":
        if a == [("c","true")]:
            #cancerNode given dyspnoeaNodepnoea
            cP = (network_graph_bayes[4].related_conditional_probabilities["cTrue"] * mProbCalculation([("c","true")])) / mProbCalculation([("d","true")])


    #Intercausal Reasoning
    elif reasoningname == "intercausal":
        if ("s","true") not in b:
            if a == [("p","false")]:
                cP = (mProbCalculation([("c","pHigh")]) * network_graph_bayes[0].related_conditional_probabilities["pHigh"]) / mProbCalculation([("c","true")])


            elif a == [("s","true")]:
                cP = (mProbCalculation([("c","sTrue")]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"]) / mProbCalculation([("c","true")])


            elif a == [("x","true")]:
                cP = network_graph_bayes[3].related_conditional_probabilities["cTrue"]


            elif a == [("d","true")]:
                cP = network_graph_bayes[4].related_conditional_probabilities["cTrue"]

        else:
            if a == [("p","false")]:
                cP = (network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]) / mProbCalculation([("c","sTrue")])

            elif a == [("x","true")]:
                cP = network_graph_bayes[3].related_conditional_probabilities["cTrue"]

            elif a == [("d","true")]:
                cP = network_graph_bayes[4].related_conditional_probabilities["cTrue"]

    print "The conditional probability is:",cP

def jointProbability(args):
    print 'Computing joint probability for:', args
    #Multiply all children by possible variants of their parents

    jP = -1.0
    argumentList = argParser(args)

    jP = jProbCalculation(argumentList)

    print 'The joint probability is:',jP

def whatIsParentStatus(args):
    combinations = []
    related_conditional_probabilities_entries = []

    for item in args:
        if item == ("p","false"):
            combinations.append("pHigh")
            related_conditional_probabilities_entries.append("pHigh")
        elif item == ("p","true"):
            combinations.append("pLow")
            related_conditional_probabilities_entries.append("pLow")
        elif item == ("s","false"):
            combinations.append("sFalse")
            related_conditional_probabilities_entries.append("sFalse")
        elif item == ("s","true"):
            combinations.append("sTrue")
            related_conditional_probabilities_entries.append("sTrue")
        elif item == ("c","true"):
            combinations.append("cTrue")
        elif item == ("c","false"):
            combinations.append("cFalse")

    if "pHigh" in combinations and "sTrue" in combinations:
        related_conditional_probabilities_entries.append("pHigh_sTrue")
    if "pHigh" in combinations and "sFalse" in combinations:
        related_conditional_probabilities_entries.append("pHigh_sFalse")
    if "pLow" in combinations and "sTrue" in combinations:
        related_conditional_probabilities_entries.append("pLow_sTrue")
    if "pLow" in combinations and "sFalse" in combinations:
        related_conditional_probabilities_entries.append("pLow_sFalse")
    if "cTrue" in combinations:
        related_conditional_probabilities_entries.append("cTrue")
    if "cFalse" in combinations:
        related_conditional_probabilities_entries.append("cFalse")
    return related_conditional_probabilities_entries

def defineAbsentParents(args):
    missing = []

    #No Polluiton
    if ("p","true") not in args and ("p","false") not in args:
        missing.append("pollutionNode")

    #No Smoking
    if ("s","true") not in args and ("s","false") not in args:
        missing.append("smokerNode")

    #No Cancer
    if ("c","true") not in args and ("c","false") not in args:
        missing.append("cancerNode")

    #Don't have to worry about Breathing Difficulty and Xray because they can never be parents!
    return missing

def jProbCalculation(args):

    checkParentStatus = whatIsParentStatus(args)
    absentParents = defineAbsentParents(args)
    total = 1

    for item in args:
        if item == ("p","false"):
            if "smokerNode" not in absentParents:
                total *= network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            if "smokerNode" in absentParents and "cancerNode" in absentParents:
                total *= network_graph_bayes[0].related_conditional_probabilities["pHigh"] * 0.1


        elif item == ("p","true"):
            if "smokerNode" not in absentParents:
                total *= network_graph_bayes[0].related_conditional_probabilities["pLow"]
            if "smokerNode" in absentParents and "cancerNode" in absentParents:
                total *= network_graph_bayes[0].related_conditional_probabilities["pLow"] * 0.1


        if item == ("s","false"):
            if "pollutionNode" not in absentParents:
                total *= network_graph_bayes[1].related_conditional_probabilities["sFalse"]
            if "pollutionNode" in absentParents and "cancerNode" in absentParents:
                total *= network_graph_bayes[1].related_conditional_probabilities["sFalse"] * 0.1
        elif item == ("s","true"):
            if "pollutionNode" not in absentParents:
                total *= network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            if "pollutionNode" in absentParents and "cancerNode" in absentParents:
                total *= network_graph_bayes[1].related_conditional_probabilities["sTrue"] * 0.1


        elif item == ("c","true"):
            if "pHigh_sTrue" in checkParentStatus:
                total *= network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]
            elif "pHigh_sFalse" in checkParentStatus:
                total *= network_graph_bayes[2].related_conditional_probabilities["pHigh_sFalse"]
            elif "pLow_sTrue" in checkParentStatus:
                total *= network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]
            elif "pLow_sFalse" in checkParentStatus:
                total *= network_graph_bayes[2].related_conditional_probabilities["pLow_sFalse"]
            else:
                if "pollutionNode" in absentParents and "smokerNode" in absentParents:
                    total *= mProbCalculation([("c","true")])
                elif "pollutionNode" in absentParents:
                    if ("sTrue") in checkParentStatus:
                        total *= mProbCalculation([("c","sTrue")])
                    if ("s","false") in checkParentStatus:
                        total *= mProbCalculation([("c","sFalse")])
                elif "smokerNode" in absentParents:
                    if ("pLow") in checkParentStatus:
                        total *= mProbCalculation([("c","pLow")])
                    if ("pHigh") in checkParentStatus:
                        total *= mProbCalculation([("c","pHigh")])


        elif item == ("c","false"):
            if "pHigh_sTrue" in checkParentStatus:
                total *= 1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]
            elif "pHigh_sFalse" in checkParentStatus:
                total *= 1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sFalse"]
            elif "pLow_sTrue" in checkParentStatus:
                total *= 1-network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]
            elif "pLow_sFalse" in checkParentStatus:
                total *= 1-network_graph_bayes[2].related_conditional_probabilities["pLow_sFalse"]
            else:
                if "pollutionNode" in absentParents and "smokerNode" in absentParents:
                    total *= mProbCalculation([("c","false")])
                elif "pollutionNode" in absentParents:
                    if ("sTrue") in checkParentStatus:
                        total *= mProbCalculation([("~c","sTrue")])
                    if ("sFalse") in checkParentStatus:
                        total *= mProbCalculation([("~c","sFalse")])
                elif "smokerNode" in absentParents:
                    if ("pLow") in checkParentStatus:
                        total *= mProbCalculation([("~c","pLow")])
                    if ("pHigh") in checkParentStatus:
                        total *= mProbCalculation([("~c","pHigh")])


        elif item == ("x","true"):
            if "cTrue" in checkParentStatus:
                total *= network_graph_bayes[3].related_conditional_probabilities["cTrue"]
            elif "cFalse" in checkParentStatus:
                total *= network_graph_bayes[3].related_conditional_probabilities["cFalse"]
            else:
                total *= mProbCalculation([("x","true")])
        elif item == ("x","false"):
            if "cTrue" in checkParentStatus:
                total *= 1-network_graph_bayes[3].related_conditional_probabilities["cTrue"]
            elif "cFalse" in checkParentStatus:
                total *= 1-network_graph_bayes[3].related_conditional_probabilities["cFalse"]
            else:
                total *= mProbCalculation([("x","false")])

        elif item == ("d","true"):
            if "cTrue" in checkParentStatus:
                total *= network_graph_bayes[4].related_conditional_probabilities["cTrue"]
            elif "cFalse" in checkParentStatus:
                total *= network_graph_bayes[4].related_conditional_probabilities["cFalse"]
            else:
                total *= mProbCalculation([("d","true")])
                print "marg d true", mProbCalculation([("d","true")])
        elif item == ("d","false"):
            if "cTrue" in checkParentStatus:
                total *= 1-network_graph_bayes[4].related_conditional_probabilities["cTrue"]
            elif "cFalse" in checkParentStatus:
                total *= 1-network_graph_bayes[4].related_conditional_probabilities["cFalse"]
            else:
                total *= mProbCalculation([("d","false")])
    return total

def marginalProbability(args):
    print 'Computing marginal probability for:', args
    #sum out unwanted variables
    argumentList = argParser(args)
    mP = mProbCalculation(argumentList)
    print "Marginal Probability:",mP

def mProbCalculation(args):
    total = 0
    for item in args:
        if item == ("P","distribution"):
            print "Marginal probability distribution of pollutionNode:"
            print "Low:",mProbCalculation([("p","true")]),"High:",mProbCalculation([("p","false")])
        elif item == ("S","distribution"):
            print "Marginal probability distribution of smokerNode:"
            print "True:",mProbCalculation([("s","true")]),"False:",mProbCalculation([("s","false")])
        elif item == ("C","distribution"):
            print "Marginal probability distribution of cancerNode:"
            print "True:",mProbCalculation([("c","true")]),"False:",mProbCalculation([("c","false")])
        elif item == ("X","distribution"):
            print "Marginal probability distribution of xrayNode:"
            print "True:",mProbCalculation([("x","true")]),"False:",mProbCalculation([("x","false")])
        elif item == ("D","distribution"):
            print "Marginal probability distribution of dyspnoeaNodepnoea:"
            print "True:",mProbCalculation([("d","true")]),"False:",mProbCalculation([("d","false")])

        elif item == ("p","true"):
            total += network_graph_bayes[0].related_conditional_probabilities["pLow"]
        elif item == ("p","false"):
            total = 1-mProbCalculation([("p","true")])

        elif item == ("s","true"):
            total += network_graph_bayes[1].related_conditional_probabilities["sTrue"]
        elif item == ("s","false"):
            total = 1-mProbCalculation([("s","true")])

        elif item == ("c","true"):
            total += network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total += network_graph_bayes[2].related_conditional_probabilities["pHigh_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]
            total += network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total += network_graph_bayes[2].related_conditional_probabilities["pLow_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]


        elif item == ("c","pLow"):
            total += network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total += network_graph_bayes[2].related_conditional_probabilities["pLow_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]


        elif item == ("c","pHigh"):
            total = network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total += network_graph_bayes[2].related_conditional_probabilities["pHigh_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]
            total = total / mProbCalculation([("p","false")])


        elif item == ("c","sTrue"):
            total = network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total += network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"]
            total = total / mProbCalculation([("s","true")])


        elif item == ("c","sFalse"):
            total += network_graph_bayes[2].related_conditional_probabilities["pHigh_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]
            total += network_graph_bayes[2].related_conditional_probabilities["pLow_sFalse"] * network_graph_bayes[0].related_conditional_probabilities["pLow"] * network_graph_bayes[1].related_conditional_probabilities["sFalse"]


        elif item == ("~c","pLow"):
            total = 1-mProbCalculation([("c","pLow")])
        elif item == ("~c","pHigh"):
            total = 1-mProbCalculation([("c","pHigh")])
        elif item == ("~c","sTrue"):
            total = 1-mProbCalculation([("c","sTrue")])
        elif item == ("~c","sFalse"):
            total = 1-mProbCalculation([("c","sFalse")])
        elif item == ("c","false"):
            total = 1-mProbCalculation([("c","true")])

        elif item == ("x","true"):
            total += network_graph_bayes[3].related_conditional_probabilities["cTrue"] * mProbCalculation([("c","true")])
            total += network_graph_bayes[3].related_conditional_probabilities["cFalse"] * mProbCalculation([("c","false")])

        elif item == ("x","false"):
            total = 1-mProbCalculation([("x","true")])

        elif item == ("x","sTrue"):
            total += network_graph_bayes[3].related_conditional_probabilities["cTrue"] * network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            total += network_graph_bayes[3].related_conditional_probabilities["cTrue"] * network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            total += network_graph_bayes[3].related_conditional_probabilities["cFalse"] * (1-network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            total += network_graph_bayes[3].related_conditional_probabilities["cFalse"] * (1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            divideBy = network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            divideBy += network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            divideBy += (1-network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            divideBy += (1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            total = total / divideBy


        elif item == ("d","true"):
            total += network_graph_bayes[4].related_conditional_probabilities["cTrue"] * mProbCalculation([("c","true")])
            total += network_graph_bayes[4].related_conditional_probabilities["cFalse"] * mProbCalculation([("c","false")])


        elif item == ("d","false"):
            total = 1-mProbCalculation([("d","true")])


        elif item == ("d","sTrue"):
            total += network_graph_bayes[4].related_conditional_probabilities["cTrue"] * network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            total += network_graph_bayes[4].related_conditional_probabilities["cTrue"] * network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            total += network_graph_bayes[4].related_conditional_probabilities["cFalse"] * (1-network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            total += network_graph_bayes[4].related_conditional_probabilities["cFalse"] * (1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            divideBy = network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            divideBy += network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"] * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            divideBy += (1-network_graph_bayes[2].related_conditional_probabilities["pLow_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pLow"]
            divideBy += (1-network_graph_bayes[2].related_conditional_probabilities["pHigh_sTrue"]) * network_graph_bayes[1].related_conditional_probabilities["sTrue"] * network_graph_bayes[0].related_conditional_probabilities["pHigh"]
            total = total / divideBy

    return total

def setPrior(args):
    print 'Setting prior for:', args
    priorQueue = parsingQueue(len(args))


    for char in args:
        priorQueue.addChar(char)
    first = True
    dest = ''
    val = ''
    while first:
        current = priorQueue.queue.get()
        if current != '=':
            dest += current
        else:
            first = False
    while not priorQueue.queue.empty():
        val += priorQueue.queue.get()
    val = float(val)
    if dest == 'P':
        for node in network_graph_bayes:
            node.related_conditional_probabilities["pHigh"] = val
            node.related_conditional_probabilities["pLow"] = 1-val
        P = val
        p = 1-P
        print 'Set pLow to',p,'and pHigh to',P
    elif dest == 'S':
        for node in network_graph_bayes:
            node.related_conditional_probabilities["sFalse"] = 1-val
            node.related_conditional_probabilities["sTrue"] = val
        s = val
        S = 1-s
        print 'Set sTrue to',s,'and sFalse to',S
    else:
        print 'Must set P or S.'

def main():

    #Attain arguments through parsing
    args = argumentParser()

    #Use related method of processing to perform correct reasoning with inputs
    pickReasoning(args)

if __name__=="__main__":


    #pollutionNode
    P = 0.1 #high pollutionNode
    p = 1-P #0.9 #low pollutionNode
    pDist = [P,p]

    #smokerNode
    S = 0.70 #smokerNode false
    s = 1-S #0.30 #smokerNode true
    sDist = [S,s]

    #cancerNode
    cPs = 0.05 #pollutionNode high, smokerNode true
    cPs_cond = cPs * P * s
    cPS = 0.02 #pollutionNode high, smokerNode false
    cPS_cond = cPS * P * S
    cps = 0.03 #pollutionNode low, smokerNode true
    cps_cond = cps * p * s
    cpS = 0.001 #pollutionNode high, smokerNode false
    cpS_cond = cpS * p * S
    #cancerNode distributions
    cDist = [cPs,cPS,cps,cpS]
    cDist_cond = [cPs_cond,cPS_cond,cps_cond,cpS_cond]

    #xrayNode
    xCT = 0.90 #cancerNode true
    xCF = 0.20 #cancerNode false
    xDist = [xCT,xCF]

    #BREATHING DIFFICULTY
    dCT = 0.65 #cancerNode true
    dCF = 0.30 #cancerNode false
    dDist = [dCT,dCF]

    #Make the graph
    network_graph_bayes = []

    #Make all necessary nodes
    pollutionNode = Node("pollutionNode")
    smokerNode = Node("smokerNode")
    cancerNode = Node("cancerNode")
    xrayNode = Node("xrayNode")
    dyspnoeaNode = Node("dyspnoeaNode")

    #Make all parent/child connections
    pollutionNode.childList = [cancerNode]
    smokerNode.childList = [cancerNode]
    cancerNode.parentList = [pollutionNode,smokerNode]
    cancerNode.childList = [xrayNode,dyspnoeaNode]
    xrayNode.parentList = [cancerNode]
    dyspnoeaNode.parentList = [cancerNode]

    #Add all nodes to the network
    network_graph_bayes = [pollutionNode,smokerNode,cancerNode,xrayNode,dyspnoeaNode]


    #Make all related conditional probabilities
    for node in network_graph_bayes:
        node.create_related_conditional_probabilities()

    main()



