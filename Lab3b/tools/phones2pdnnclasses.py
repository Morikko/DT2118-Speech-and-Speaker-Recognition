#!/usr/bin/python
# From a list of phones, generates three states in the form ph_s2, ph_s3... and assigns
# unique numerical ids to be used for example in a neural network. The symbol "sp" is
# a special case and gets only one state. The script then generates the map-label string
# used in pdnn to map equivalent classes. All states in the same phoneme are equivalent.
# Used in Lab 3 in DT2118 Speech and Speaker Recognition
#
# Example:
# cat phones.lst
# sil
# ah
# sp
# ./phones2pdnnclasses.py phones.lst
# 0-2:0/3-5:1/6:2
#
# (C) 2016 Giampiero Salvi <giampi@kth.se>
import sys

filename = sys.argv[1]
f = open(filename)

statecount = 0
equivclass = 0
mappings = []
for line in f:
    ph = line.rstrip()
    if ph == 'sp':
        mappings.append(str(statecount)+':'+str(equivclass))
        statecount += 1
        equivclass += 1
    else:
        mappings.append(str(statecount)+'-'+str(statecount+2)+':'+str(equivclass))
        statecount += 3
        equivclass += 1
print('/'.join(mappings))
