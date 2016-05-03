#!/usr/bin/python
# From a list of phones, generates three states in the form ph_s2, ph_s3... and assigns
# unique numerical ids to be used for example in a neural network. The symbol "sp" is
# a special case and gets only one state. State names are in accordance with HTK definitions.
# Used in Lab 3 in DT2118 Speech and Speaker Recognition
#
# Example:
# cat phones.lst
# sil
# ah
# sp
# ./dict2phones.py phones.lst > states2ids.lst
# cat states2ids.lst
# sil_s2 0
# sil_s3 1
# sil_s4 2
# ah_s2 3
# ah_s3 4
# ah_s4 5
# sp_s2 6
# 
# (C) 2016 Giampiero Salvi <giampi@kth.se>
import sys

filename = sys.argv[1]
f = open(filename)

count = 0
for line in f:
    ph = line.rstrip()
    if ph == 'sp':
        print('sp_s2 ' + str(count))
        count = count+1
    else:
        for state in ['s2', 's3', 's4']:
            print(ph + '_' + state + ' ' + str(count))
            count = count+1
