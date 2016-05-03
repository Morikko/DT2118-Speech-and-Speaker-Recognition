#!/usr/bin/python
# Reads an HTK Master Label File and uses HTK to generate speech features.
# Finally stores the results in PFile format with the help of the pfile_create
# program.
# Requires that the HTK tools are in the path and that the following
# configuration files are accessible:
# - config/features_<feature_kind>.conf
# - config/input_format.cfg
# In order to be useful, you also need to install the pfile tools:
# - ftp://ftp.icsi.berkeley.edu/pub/real/davidj/quicknet.tar.gz
# - http://www.icsi.berkeley.edu/ftp/pub/real/davidj/pfile_utils-v0_51.tar.gz
# Used in Lab 3 in DT2118 Speech and Speaker Recognition
#
# Usage:
# ./htk2pfile.py input.mlf states2ids.lst <feature_kind> out.pfile
#
# (C) 2016 Giampiero Salvi <giampi@kth.se>
from __future__ import print_function
import sys
import struct
from os import path
import subprocess
import numpy as np

def rows2labels(rows):
    labels=[]
    for j in range(len(rows)):
        fields = rows[j].split(' ')
        start = int(fields[0])/100000
        end = int(fields[1])/100000
        state = fields[2]
        if len(fields)>3:
            phone = fields[3]
        labels.append([start, end, phone, state])
    return labels

def raw2labels(rawlabels):
    rows = rawlabels.rstrip().split('\n')
    fname = rows[0].strip('\"').replace('.rec', '.wav')
    return fname, rows2labels(rows[1:])

mlffilename = sys.argv[1]
stateidfilename = sys.argv[2]
featurekind = sys.argv[3]
outputfilename = sys.argv[4]

htkcmd = 'HList -C config/input_format.cfg -C config/features_'+featurekind+'.cfg -r '
pfilecmd = ''

fin = open(stateidfilename)
states2ids = {}
for line in fin:
    statename, stateid = line.split()
    states2ids[statename] = stateid
fin.close()

fin = open(mlffilename)
labeldata = fin.read()[8:]           # disregard header
fin.close()
rawlabels = labeldata.split('.\n') # split into utterances
rawlabels = [x for x in rawlabels if x] # remove eventual empty items
nutts = len(rawlabels)

for sent_no in range(nutts):
    fname, labels = raw2labels(rawlabels[sent_no])
    htkp = subprocess.Popen(htkcmd+fname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    features = np.loadtxt(htkp.stdout)
    nframes, nfeatures = features.shape
    if pfilecmd == '':
        pfilecmd = 'pfile_create -i - -o '+outputfilename+' -f '+str(nfeatures)+' -l 1'
        #pfilecmd = 'cat'
        pfilep = subprocess.Popen(pfilecmd, shell=True, stdin=subprocess.PIPE)
        #print('Producing a (x, y) dataset file for: '+mlffilename, file=pfilep.stdin)
    print('processing '+fname, file=sys.stderr)
    labarr = []
    for start, end, phone, state in labels:
        stateid = states2ids[phone+'_'+state]
        for time in range(start, end):
            labarr.append(stateid)
    if len(labarr) != nframes:
        print("Warning: length mismatch, nframes=%d, nlabels=%d", nframes, len(labarr), file=sys.stderr)
        labarr = labarr[0:nframes]
    for frame_no in range(nframes):
        row = str(sent_no)+' '+str(frame_no)+' '+' '.join(map(str, features[frame_no,:]))+' '+labarr[frame_no]
        print(row, file=pfilep.stdin)
