#!/bin/bash
# Training script for the TIDIGIT database. Starts with models with a single
# Gaussian per state and incrementally doubles the number of Gaussians and
# retrains the models.
# Used for Lab 3 in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./train_gmm-hmm.sh feature_code
# Example:
# ./train_gmm-hmm.sh MFCC_0
#
# Note: it takes about 11 minutes to run on a i5 processor at 2.5GHz
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
function recho {
    tput setaf 1;
    echo $1;
    tput sgr0;
}

# read arguments
features=$1

if [ ! -e models_$features ]
then
    echo "You need to run \"tools/train.sh $features\" first, aborting"
    exit
fi

config0=config/input_format.cfg
config=config/features_$features.cfg

traindir=models_$features
mkdir -p $traindir
for iter in {8..19}
do
    mkdir -p $traindir/hmm$iter
done
recho "Training started for features $features ..."
trainscp=workdir/train.lst
recho "...increasing number of mixture components to 2"
HHEd -A -H $traindir/hmm7/hmmdefs.mmf -M $traindir/hmm8 config/nmix2.hed workdir/phones1.lst
recho "...two iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm8/hmmdefs.mmf -M $traindir/hmm9 workdir/phones1.lst
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm9/hmmdefs.mmf -M $traindir/hmm10 workdir/phones1.lst
recho "..increasing number of mixture components to 4"
HHEd -A -H $traindir/hmm10/hmmdefs.mmf -M $traindir/hmm11 config/nmix4.hed workdir/phones1.lst
recho "..two iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm11/hmmdefs.mmf -M $traindir/hmm12 workdir/phones1.lst
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm12/hmmdefs.mmf -M $traindir/hmm13 workdir/phones1.lst
recho "...increasing number of mixture components to 8"
HHEd -A -H $traindir/hmm13/hmmdefs.mmf -M $traindir/hmm14 config/nmix8.hed workdir/phones1.lst
recho "...two iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm14/hmmdefs.mmf -M $traindir/hmm15 workdir/phones1.lst
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm15/hmmdefs.mmf -M $traindir/hmm16 workdir/phones1.lst
recho "...increasing number of mixture components to 16"
HHEd -A -H $traindir/hmm16/hmmdefs.mmf -M $traindir/hmm17 config/nmix16.hed workdir/phones1.lst
recho "...two iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm17/hmmdefs.mmf -M $traindir/hmm18 workdir/phones1.lst
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm18/hmmdefs.mmf -M $traindir/hmm19 workdir/phones1.lst
recho "Training finished."
