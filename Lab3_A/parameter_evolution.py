#!/usr/bin/python

import sys
sys.path.append("htkModelParser/")
from ply import yacc

import htk_lexer
import htk_parser
from htk_models import *

#models = sys.argv[1]
def getParameter(models):
    """
    Get through the folder models and analyse each hmm
    Take the phone m ans the state s
    Get the mean and the variance of the first gaussian
    Return all the mean and var
    """
    m = 2
    s =1

    mean = []
    var = []

    # Get the values of the 3rd phones for each hmm
    for i in range(8):
        hfile = open(models + "/hmm" + str(i) + "/hmmdefs.mmf")
        data = hfile.read()
        hmms = yacc.parse(data)
        if i == 0:
            m = 10
        else:
            m = 2
        thishmm = hmms[m]        

        print('Iteration: ' + str(i))
        print('model number '+str(m+1)+' is called '+thishmm.name+' and state '+str(s+1))

        thisstate = thishmm.states[s][1]
        thiscomponent = thisstate.mixtures[0][2]

        mean.append(thiscomponent.mean.vector)
        var.append(thiscomponent.var.vector)
    
    return mean, var
    
def comparePhonemes():
    s =0

    mean = []
    phonemes = []

    hfile = open("models_MFCC_0/hmm7/hmmdefs.mmf")
    data = hfile.read()
    hmms = yacc.parse(data)
    for m in range(len(hmms)):
        thishmm = hmms[m]        

        print('model number '+str(m+1)+' is called '+thishmm.name+' and state '+str(s+1))

        phonemes.append(thishmm.name)

        thisstate = thishmm.states[s][1]
        thiscomponent = thisstate.mixtures[0][2]

        mean.append(thiscomponent.mean.vector)
    return phonemes, mean      
