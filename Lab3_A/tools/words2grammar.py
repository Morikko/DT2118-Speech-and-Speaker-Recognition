#!/usr/bin/python
# Creates a recognition grammar based on a list of words. The grammar allows a free loop
# of the words. Saved in HTK format for imput to HParse. Used in Lab 3 in DT2118 Speech
# and Speaker Recognition
#
# Usage:
# ./words2grammar.py words.lst > loop.grm
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
import sys
import re

filename = sys.argv[1]
f = open(filename)
words = f.read()
words = re.sub('\n', ' | ', words.rstrip())

print('$digit = ' + words + ";")
print('(SENT-START <$digit> SENT-END )')
