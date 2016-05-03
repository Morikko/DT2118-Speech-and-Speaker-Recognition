#!/bin/bash
# Test script for the TIDIGIT database. Performs Viterbi decoding and evaluation
# on the GMM-HMM models trained by train_mixup.sh
# Used for Lab 3 in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./test_gmm-hmm.sh feature_code
# Example:
# ./test_gmm-hmm.sh MFCC_0
#
# Note: it takes about 12 minutes to run on a i5 processor at 2.5GHz
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
function recho {
    tput setaf 1;
    echo $1;
    tput sgr0;
}

# read arguments
features=$1

config0=config/input_format.cfg
config=config/features_$features.cfg
testdir=results_$features
testscp=workdir/test.lst
mkdir -p $testdir
rm -f $testdir/results_gmm-hmm.txt

NMIX=(2 4 8 16)
# iteration corresponding to above number of mixtures
ITER=(10 13 16 19)
recho "Test started with features $features ..."
for n in {0..3}
do
    recho "...testing models with ${NMIX[$n]} Gaussian components"
    models=models_$features/hmm${ITER[$n]}/hmmdefs.mmf
    recho "...recognising test utterances in $testscp"
    HVite -A -C $config0 -C $config -H $models -S $testscp -i $testdir/recout_test_nmix${NMIX[$n]}.mlf -w workdir/digitloop.lat -p -20.0 -s 1.0 workdir/recdict.dic workdir/phones1.lst

    recho "...calculating accuracy"
    HResults -A -p -I workdir/test_word.mlf workdir/words.lst $testdir/recout_test_nmix${NMIX[$n]}.mlf | tee -a $testdir/results_gmm-hmm.txt
done
recho "Test finished, results stored in $testdir/results_gmm-hmm.txt"

