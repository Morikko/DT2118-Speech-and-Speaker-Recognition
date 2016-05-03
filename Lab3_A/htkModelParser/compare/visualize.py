'''
Created on Mar 24, 2014

@author: joro
'''

from pylab import *
from compare.compareModels import loadModelsForGivenPhoneme, getMeansForStates
from Adapt import MODEL_NAME


 
def plotMfccs(mfcc1, mfcc2):
    figure()
    # original model
    plot(mfcc1, 'g')
    # adapted model
    plot(mfcc2, 'r')
    show()
    

if __name__ == '__main__':
    
        
#         modelBefore = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/adapted/' + modelName +  '.gmmlrmean'
#         modelAfter = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/adapted/' + modelName +   '.gmmlrmean_map_2'
#         
        
        modelBefore = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs'

        modelAfter = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/adapted/'  + MODEL_NAME +   '.gmmlrmean'
        modelAfter = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/adapted/'  + MODEL_NAME +   '_map_4'
#         
        phonemeName ='E'
        hmmModel1, hmmModel2  = loadModelsForGivenPhoneme(modelBefore, modelAfter, phonemeName)
        
           # get mean vectors 
        means1 = getMeansForStates(hmmModel1)
        means2 = getMeansForStates(hmmModel2)
        
        whichState = 2
        plotMfccs(means1[whichState], means2[whichState])
        
