#!/bin/bash
# Test script for the TIDIGIT database. Performs Viterbi decoding and evaluation
# Used for Lab 3 in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./test_g-hmm.sh feature_code
# Example:
# ./test_g-hmm.sh MFCC_0
#
# Note: it takes about 1:30 minutes to run on a i5 processor at 2.5GHz
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
function recho {
    tput setaf 1;
    echo $1;
    tput sgr0;
}


# read arguments
features=$1

config=config/features_$features.cfg
testdir=results_$features
mkdir -p $testdir
rm -f $testdir/results_g-hmm.txt

recho "Test started with features $features ..."
models=models_$features/hmm7/hmmdefs.mmf
config0=config/input_format.cfg
config=config/features_$features.cfg
testscp=workdir/test.lst
recho "...recognising test utterances in $testscp"
HVite -A -C $config0 -C $config -H $models -S $testscp -i $testdir/recout_test.mlf -w workdir/digitloop.lat -p -20.0 -s 1.0 workdir/recdict.dic workdir/phones1.lst
recho "Results stored in $testdir/recout_test.mlf"
recho "Calculating accuracy"
HResults -A -p -I workdir/test_word.mlf workdir/words.lst $testdir/recout_test.mlf | tee -a $testdir/results_g-hmm.txt
recho "Results stored in $testdir/results_g-hmm.txt"
recho "Test finished."
