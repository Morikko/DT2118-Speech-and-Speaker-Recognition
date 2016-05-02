#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import proto
import tools

example = np.load('example.npz')['example'].item()
tidigits = np.load('tidigits.npz')['tidigits']

plt.figure(1)

# Compute 4.1 Enframe
result1 = proto.enframe(example['samples'], 400, 200)


# Plot signal
plt.subplot(811)
plt.plot(example['samples'])
# Plot frames
# True answer
#plt.imshow(example['frames'], origin='lower', interpolation='nearest', aspect='auto')
plt.subplot(812)
plt.imshow(result1.transpose().astype(np.int), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4.2: Pre-Emphasis
plt.subplot(813)
result2 = proto.preemp(result1)
plt.imshow(result2.transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4.3 : Hamming Window
plt.subplot(814)
result3 = proto.windowing(result2)
plt.imshow(result3.transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4.4 : Fast Fourier Transform
plt.subplot(815)
result4 = proto.powerSpectrum(result3, 512)
plt.imshow(result4.transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4.5 : Mel filterbank log spectrum
plt.subplot(816)
result5 = proto.logMelSpectrum(result4, 20000)
plt.imshow(result5.transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4.6 : Cosine Transform and Liftering
plt.subplot(817)
result6 = proto.cepstrum(result5, 13)
plt.imshow(result6.transpose(), origin='lower', interpolation='nearest', aspect='auto')
plt.subplot(818)
result7 = tools.lifter(result6)
plt.imshow(result7.transpose(), origin='lower', interpolation='nearest', aspect='auto')

## Compute 5 : MFCC for all tidigits and concanate them
#tidiMfcc = tools.mfcc(tidigits[0]['samples']) 
#for i in range(1, len(tidigits)):
#    tidiMfcc = np.append(tidiMfcc, tools.mfcc(tidigits[i]['samples']), axis=0 )
#
## Correlation
#corMfcc = np.corrcoef(tidiMfcc.transpose())
#
#tidiMspec = tools.mspec(tidigits[0]['samples']) 
#for i in range(1, len(tidigits)):
#    tidiMspec = np.append(tidiMspec, tools.mspec(tidigits[i]['samples']), axis=0 )

# Correlation
#corMspec = np.corrcoef(tidiMspec.transpose())

# Examples for verifying in course 4
#tidi2 = tidigits[17]['samples']
#tidi1 = tidigits[16]['samples']
#mfcc2 = tools.mfcc(tidi2)
#mfcc1 = tools.mfcc(tidi1)

#D = np.zeros([44, 44])
#for i in range(len(tidigits)):
#    for j in range(len(tidigits)):
#        a = tools.mfcc(tidigits[i]['samples'])
#        b = tools.mfcc(tidigits[j]['samples'])
#        ld = proto.localDistances(a, b)
#        D[i][j] = proto.dtw(ld)
