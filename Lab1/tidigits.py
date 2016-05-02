# Script to collect examples from the TIDIGITS database, compatible with python3
# To be able to run you need:
# - libsndfile development package (libsndfile1-dev in Ubuntu)
# - pysndfile (https://pypi.python.org/pypi/pysndfile/0.2.1)
# - access to KTH afs cell nada.kth.se
# - access rights to the TIDIGITS database
#
# Usage:
# python3 tidigitsCollectExamples_python3.py
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
# DT2118 Speech and Speaker Recognition
import numpy as np
import os
import sys
from pysndfile import sndio

for tidigitsroot in ['/home/giampi/corpora/tidigits/disc_4.1.1/tidigits/train/',
                     '/afs/nada.kth.se/dept/tmh/corpora/tidigits/disc_4.1.1/tidigits/train/']:
    if os.path.exists(tidigitsroot):
        break
    else:
        continue
    raise NameError('TIDIGITS root directory not found on system')

genders = ["man", "woman"]
speakers = ["ae", "ac"]

digits = ["o", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
repetitions = ["a", "b"]

tidigits = []
for idx in range(len(speakers)):
    for digit in digits:
        for repetition in repetitions:
            filename = os.path.join(tidigitsroot, genders[idx], speakers[idx], digit+repetition+'.wav')
            sndobj = sndio.read(filename)
            # libsndfile scales the values down to the -1.0 +1.0 range
            # here we convert back to the range of 16 bit linear PCM
            # to get similar results as from Kaldi or HTK
            samples = np.array(sndobj[0])*np.iinfo(np.int16).max
            samplingrate = sndobj[1]
            tidigits.append({"filename": filename,
                             "samplingrate": samplingrate,
                             "gender": genders[idx],
                             "speaker": speakers[idx],
                             "digit": digit,
                             "repetition": repetition,
                             "samples": samples})

if sys.version_info.major==3:
    np.savez('tidigits_python3.npz', tidigits=tidigits)
else:
    np.savez('tidigits.npz', tidigits=tidigits)
