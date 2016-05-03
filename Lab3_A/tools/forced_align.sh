#!/bin/bash
# Forced Alignment on the training set of the TIDIGIT database. Performs Viterbi
# decoding using the orthographic transcriptions and returns time-aligned phonetic
# transriptions. It uses the GMM-HMM models trained by train_mixup.sh
# Used for Lab 3 in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./forced_align.sh feature_code
# Example:
# ./forced_align.sh MFCC_0_D_A
#
# Note: it takes about 5 minutes to run on a i5 processor at 2.5GHz
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

recho "Running forced alignment with features $features ..."
recho "...training data"
HVite -A -o SW -b 'SENT-START' -C $config0 -C $config -a -H models_$features/hmm19/hmmdefs.mmf -i workdir/train_aligned.mlf -m -t 250.0 -I workdir/train_word.mlf -S workdir/train.lst workdir/recdict.dic workdir/phones1.lst
recho "...test data"
HVite -A -o SW -b 'SENT-START' -C $config0 -C $config -a -H models_$features/hmm19/hmmdefs.mmf -i workdir/test_aligned.mlf -m -t 250.0 -I workdir/test_word.mlf -S workdir/test.lst workdir/recdict.dic workdir/phones1.lst
recho "Finished, results stored in workdir/train_aligned.mlf and workdir/test_aligned.mlf"

