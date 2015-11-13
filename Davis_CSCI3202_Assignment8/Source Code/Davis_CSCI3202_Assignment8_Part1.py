#Connor Davis
#CSCI 3202: Artificial Intelligence
#Assignment 8: Hidden Markov Models

from collections import Counter
from collections import OrderedDict

#List of every pair of state/evidence
state_evidence_list = []

#Parse the given file for string pairs
def fileio():
    charstring = ''
    with open("typos20.data", "r") as openedfile:

        #i is a line in the file
        for i in openedfile.readlines():

            #Add characters to charstring
            for char in i:
                if char != " " and char != '\n':
                    charstring += char

            #Append charstring to state_evidence combo list
            if charstring != '':
                state_evidence_list.append(charstring)
            charstring = ''

def emission_counter():

    #Emission probability numerator
    state_evidence_counter = (Counter(state_evidence_list))

    #List comprehension to create list of ONLY states
    temp_state_list = [x[0] for x in state_evidence_list]
    #List comprehension to create list of ONLY evidence
    temp_evidence_list = [x[1] for x in state_evidence_list]

    #print (temp_evidence_list)

    #Emission probability denominator
    state_counter = (Counter(temp_state_list))

    return state_evidence_counter, state_counter, temp_state_list, temp_evidence_list

def emission_probabilities(sec, sc):

    temp_dictionary = {}

    #Look at state/evidence list
    for key,value in sec.iteritems():
        #Gets first letter of key (the state)
        extract = list(key)[0]
        #Finds denominator value in sec
        denom = sc[extract]

        #Normalize
        printable_combo_variable = (1 + float(value)) / (27 + float(denom))

        #Add to temp_dictionary for printing
        temp_dictionary[key] = printable_combo_variable

    #List of emission probabilities, just need to format!!!!!!!!!!!!!!!!!!!!!!!!!!
    print("Emission Probabilities:")
    for key,value in temp_dictionary.items():
        print (key, value)
    #print(temp_dictionary.value, '\n')
    #print ('\n'.join(str(row) for row in temp_dictionary))

def transition_counter():

    #List of all current_state/future_state combos
    superTransitionList = []

    #Loop through state_evidence_list, getting "state" letter from each entry
    temp_state_list = [x[0] for x in state_evidence_list]

    #Record the current_state + future_state combos that we see in data
    i = 0
    for i in range(len(temp_state_list)-1):

        now = temp_state_list[i]
        future = temp_state_list[i+1]
        charstring = now + future

        superTransitionList.append(charstring)
        charstring = []

    #Counter for number of times a given current_state/future_state combo occurs
    #Numerator for Transition Probabilities
    current_state_future_state_counter = (Counter(superTransitionList))

    #print(current_state_future_state_counter)
    return current_state_future_state_counter


def transition_probabilities(uopl, sc):

    probability_transition_dictionary = OrderedDict()
    #value pair of uopl = numerator

    superAlphabetList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']

    #Loop through all possible combinations of letter pairs
    #aa, ab, ac...
    for item in superAlphabetList:
        for item2 in superAlphabetList:
            numerator = float(uopl[item + item2])
            denom = sc[item]

            printable_combo_variable = (numerator + 1) / float(denom + 27)

            probability_transition_dictionary[item + item2] = printable_combo_variable

    print ("Transitional probabiltiies in the following format:")
    print ("P( kr)  == P(r | k)")
    for key,value in probability_transition_dictionary.iteritems():
        #print(key,value)
        print("P(",key,") =",value)

def initial_probabilities(tsl, tel):

    #times a letter occurs + 1
    #-------------------------
    # total number of letters

    letter_occurs_counter = 0
    letter_occurs_master_dict = {}
    totalcounter = 0

    superAlphabetList = ['_','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    final_dict_temp_list = []
    final_dict = dict.fromkeys(superAlphabetList,0)

    #print (state_evidence_list)

    for anything in tsl:
        totalcounter += 1

    for item in superAlphabetList:

        for letter in tsl:
            if item == letter:
                letter_occurs_counter += 1
                connor = 1

        letter_occurs_master_dict[item] = letter_occurs_counter

        letter_occurs_counter = 0

    #print (letter_occurs_master_dict)

    for item in letter_occurs_master_dict.values():
        init_prob = float(item + 1) / float(totalcounter + 27)
        final_dict_temp_list.append(init_prob)
        init_prob = 0


    q = 0
    print ("Initial Probabilities:")
    for letter in superAlphabetList:
        #A
        for i in final_dict_temp_list:
            print("P("+letter+") =", final_dict_temp_list[q])
            q += 1
            break




#Format print strings


#END OF PART 1
############################################################################


def main():
    fileio()
    sec, sc, tsl, tel = emission_counter()
    emission_probabilities(sec, sc)
    uopl = transition_counter()
    transition_counter()
    transition_probabilities(uopl, sc)
    initial_probabilities(tsl, tel)

    print
main()