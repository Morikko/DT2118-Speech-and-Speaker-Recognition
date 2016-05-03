#!/usr/bin/python
# Extract list of phonemes from dictionary and add sil symbol
# Used in Lab 3 in DT2118 Speech and Speaker Recognition
#
# Usage:
# ./dict2phones.py pron.dic > phones.lst
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
import sys

filename = sys.argv[1]
f = open(filename)

# we add the sil model that is always present
phones = set(['sil'])

# for each filename create transcription
for line in f:
    word, pron = line.rstrip().split('\t')
    for ph in pron.split(' '):
        phones.add(ph)
print '\n'.join(sorted(phones))
