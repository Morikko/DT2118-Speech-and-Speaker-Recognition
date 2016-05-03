#!/usr/bin/python
# Example on how to use Georgi Dzhambazov's HTK model parser to analyse the parameters of
# HMM models. The script just outputs some information about the input model, but should
# be used mainly to learn how to handle the Hmm class and its content.
# Used in Lab 3 in DT2118 Speech and Speaker Recognition
#
# Usage:
# ./htkModelParserExample.py hmmdefinition
# Example:
# tools/htkModelParserExample.py models_MFCC/hmm7/hmmdefs.mmf
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
import sys
sys.path.append("htkModelParser/")
from ply import yacc

import htk_lexer
import htk_parser
from htk_models import *

hmmfile = sys.argv[1]

print('Example usage for Georgi Dzhambazov\'s HTK model parser')
print('opening HTK model file: '+hmmfile)
file = open(hmmfile)
print('parsing the data')
data = file.read()
hmms = yacc.parse(data)

print('the number of HMM models is: ' + str(len(hmms)))
m=10
thishmm = hmms[m]
print('model number '+str(m+1)+' is called '+thishmm.name+' and has '+str(len(thishmm.states))+' states')
s=1
thisstate = thishmm.states[s][1]
print('state number '+str(s+1)+' has '+str(len(thisstate.mixtures))+' mixture component(s)')
thiscomponent = thisstate.mixtures[0][2]
print('the zero\'th Gaussian term has:')
thismean = thiscomponent.mean.vector
print('...mean of length '+str(len(thismean))+':')
print(thismean)
thisvar = thiscomponent.var.vector
print('...and variance of length '+str(len(thisvar))+':')
print(thisvar)
