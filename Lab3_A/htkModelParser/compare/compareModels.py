'''
Created on Mar 24, 2014

@author: joro
'''
from htk_converter import HtkConverter
from htk_models import Hmm
import matplotlib as plt
from matplotlib.pyplot import plot
from pylab import *
from numpy.lib.utils import deprecate
from Adapt import HMM_LIST
import os.path
import sys
import numpy

path_to_hmm_defs_before_adapt='/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs_edited_for_wout'



path_to_hmm_defs_after_adapt='/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_edited_for_wout'

path_to_hmm_defs_after_adapt = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs.gmmlrmean_test'

# japanese female voice model: 
path_to_hmm_defs_after_adapt='/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/HTS_japan_female/hmmdefs.gmmlrmean_map_2'


PATH_TO_HMMLIST='/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/'

HMMLIST_NAME = 'monophones0'

MODEL_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'

HMM_LIST_URI =  os.path.join(PATH_TO_HMMLIST + HMMLIST_NAME)


def _computeDiffForaPhonemeModel(means1, means2):
    
    distances = []
      
    ######## find diff. 
    for mean1, mean2 in zip(means1, means2):    
        mean1Array = numpy.asarray(mean1)
        mean2Array = numpy.asarray(mean2)

        euclDist = numpy.linalg.norm(mean1Array - mean2Array)
        norm2meanOriginalModel = numpy.linalg.norm(mean1Array)
        distances.append(euclDist/norm2meanOriginalModel)
   
    # compute ratio to first model    
    return distances


'''
get the means for the three states of a phoneme model
'''

def getMeansForStates(hmmModel1):
    means = []
    
    for i in range(len(hmmModel1.states)):
        currState1 = hmmModel1.states[i][1]
        
        # only one mixture
        mixture = currState1.mixtures[0][2]
        mean1 = mixture.mean.vector
        
        means.append(mean1)
    
    return  means



    '''
    for the two loaded models computes l2-distance between mean of each state
    Can be done for all models or only for a given phoneme. edit in the function the var phonemeName
    '''
    #@deprecate change num of params to make it work. not finished 
def findDiffMean(phonemeName):
    
    hmmModel1, hmmModel2  = loadModelsForGivenPhoneme(phonemeName)
    
    
    # get mean vectors 
    means1 = getMeansForStates(hmmModel1)
    means2 = getMeansForStates(hmmModel2)
   
   
    distances = _computeDiffForaPhonemeModel(means1, means2)
    print "phoneme name: %s"  % phonemeName
    print "distances: " , distances[0], distances[1], distances[2]


    

'''
get the hmm model for a given phoneme from the two trained models 
'''    
def loadModelsForGivenPhoneme(modelBefore, modelAfter, phonemeName):
    
    
    # load models
    conv_before = HtkConverter()
    conv_before.load(modelBefore, HMM_LIST_URI)
    conv_after = HtkConverter()
    conv_after.load(modelAfter, HMM_LIST_URI)
    
    # get models for given phoneme:
   
    hmmModels = [hmm for hmm in conv_before.hmms if hmm.name == phonemeName]
    hmmModel1 = hmmModels[0]
    hmmModels = [hmm for hmm in conv_after.hmms if hmm.name == phonemeName]
    hmmModel2 = hmmModels[0]
    return hmmModel1, hmmModel2




def printModelsMiddleState(hmmModel1, pathOutput):
    '''

    prints models to a .txt file easy to load for gmdistribution function in matlab 
    only middle state of a model
    k - num muxtures, 
    d - feature dim
    mu in format k x d
    stdev in format: 1 x d x k 
    p : mixture weights: k x 1 
    '''
    mixtureWeigths = []
    means = []
    vars = []
    
    if len(hmmModel1.states) <2:
        print  'model {0} has only 1 state'.format(hmmModel1.name)
        middleState1 = hmmModel1.states[0][1]
    else: 
        middleState1 = hmmModel1.states[1][1]
    
#     middleState1.display()
    # iterate in  mixtures
    for currMix in range(len(middleState1.mixtures)):
        
        mixture = middleState1.mixtures[currMix][2]
        
        mixtureWeigth = middleState1.mixtures[currMix][1]
        mixtureWeigths.append(mixtureWeigth)
        
        mean1 = mixture.mean.vector
        means.append(mean1)
#         mean1.display()
        
        var =  mixture.var.vector
#         var.display()
        vars.append(var)
        
        
#     means.append(mean1)
    meansURI = os.path.join(pathOutput , hmmModel1.name  + '.means')
    varsURI = os.path.join(pathOutput , hmmModel1.name  + '.vars')
    weightsURI = os.path.join(pathOutput , hmmModel1.name  + '.weights')
    
    writeListOfListToTextFile(means, None, pathToOutputFile=meansURI)
    writeListOfListToTextFile(vars, None, pathToOutputFile=varsURI)
    writeListToTextFile(mixtureWeigths, None, pathToOutputFile=weightsURI) 

    
    
    
def printModelsAllStates(hmmModel1, pathOutput):
    '''

prints models to a .txt file easy to load for gmdistribution function in matlab 
only middle state of a model
k - num muxtures, 
d - feature dim
mu in format k x d
stdev in format: 1 x d x k 
p : mixture weights: k x 1 
'''
    mixtureWeigths = []
    means = []
    vars = []
    
    for j in range(len(hmmModel1.states)):
#         print  'model {0} has only 1 state'.format(hmmModel1.name)
        currState = hmmModel1.states[j][1];
#     middleState1.display()

        # iterate in  mixtures
        for currMix in range(len(currState.mixtures)):
            
            mixture = currState.mixtures[currMix][2]
            
            mixtureWeigth = currState.mixtures[currMix][1]
            mixtureWeigths.append(mixtureWeigth)
            
            mean1 = mixture.mean.vector
            means.append(mean1)
    #         mean1.display()
            
            var =  mixture.var.vector
    #         var.display()
            vars.append(var)
            
            
    #     means.append(mean1)
        meansURI = os.path.join(pathOutput , hmmModel1.name  + str(j)  + '.means')
        varsURI = os.path.join(pathOutput , hmmModel1.name  + str(j) + '.vars')
        weightsURI = os.path.join(pathOutput , hmmModel1.name + str(j)  + '.weights')
        
        writeListOfListToTextFile(means, None, pathToOutputFile=meansURI)
        writeListOfListToTextFile(vars, None, pathToOutputFile=varsURI)
        writeListToTextFile(mixtureWeigths, None, pathToOutputFile=weightsURI) 

    
    
    ##################################################################################
def writeListOfListToTextFile(listOfList,headerLine, pathToOutputFile):    
    outputFileHandle =  open(pathToOutputFile, 'w')
    
    if not headerLine == None:
        outputFileHandle.write(headerLine)
    
    for listLine in listOfList:
        
        output = ""
        for element in listLine:
            output = output + str(element) + "\t"
        output = output.strip()
        output = output + '\n'
        outputFileHandle.write(output)
    
    outputFileHandle.close()


##################################################################################
def writeListToTextFile(inputList,headerLine, pathToOutputFile):    
        outputFileHandle = open(pathToOutputFile, 'w')
    
        if not headerLine == None:
            outputFileHandle.write(headerLine)
    
        output = ""
        for element in inputList:
            output = output + str(element) + "\t"
        output = output.strip()
        output = output + '\n'
        outputFileHandle.write(output)
    
        outputFileHandle.close()




if __name__ == '__main__':
#     findDiffMean(phonemeName)

    
    
    conv_before = HtkConverter()
    conv_before.load(MODEL_URI, HMM_LIST_URI)
    
    # one phoneme
    phonemeName = 'A'
    hmmModels = [hmm for hmm in conv_before.hmms if hmm.name == phonemeName]
    hmmModel1 = hmmModels[0]
    
    # all phonemes
    for currHmmModel in conv_before.hmms:
#         printModelsMiddleState(currHmmModel, PATH_TO_HMMLIST);
        
        printModelsAllStates(currHmmModel, PATH_TO_HMMLIST);



    
    
    
    