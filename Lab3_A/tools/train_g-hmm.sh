#!/bin/bash
# Training script for the TIDIGIT database. Performs flat-start initialization
# and a number of iterations of Embedded Baum-Welch training. Used for Lab 3
# in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./train_g-hmm.sh feature_code
# Example:
# ./train_g-hmm.sh MFCC_0
#
# Note: it takes about 6 minutes to run on a i5 processor at 2.5GHz
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
trainscp=workdir/train.lst

mkdir -p models_$features

traindir=models_$features
mkdir -p $traindir
for iter in {0..7}
do
    mkdir -p $traindir/hmm$iter
done
recho "Monophone training started with feature kind $features ..."
recho "...performing flat initialization (global means and variances)"
cp config/proto_$features.mmf $traindir/proto
HCompV -A -C $config0 -C $config -f 0.01 -m -S $trainscp -M $traindir/hmm0 $traindir/proto
recho "Global means and variances in $traindir/proto"
recho "...cloning prototype model for each phone"
head -n 3 $traindir/hmm0/proto > $traindir/hmm0/hmmdefs.mmf
cat $traindir/hmm0/vFloors >> $traindir/hmm0/hmmdefs.mmf
for ph in `cat workdir/phones1.lst`
do
    sed "1d;2d;3d;s/proto/$ph/g" $traindir/hmm0/proto >> $traindir/hmm0/hmmdefs.mmf
done
recho "Model set with equal means and variances in $traindir/hmm0/hmmdefs.mmf"
recho "...first three iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone0.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm0/hmmdefs.mmf -M $traindir/hmm1 workdir/phones0.lst
recho "Model $traindir/hmm1/hmmdefs.mmf ready."
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone0.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm1/hmmdefs.mmf -M $traindir/hmm2 workdir/phones0.lst
recho "Model $traindir/hmm2/hmmdefs.mmf ready."
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone0.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm2/hmmdefs.mmf -M $traindir/hmm3 workdir/phones0.lst
recho "Model $traindir/hmm3/hmmdefs.mmf ready."
recho "...adding short pause model"
cp $traindir/hmm3/hmmdefs.mmf $traindir/hmm4/hmmdefs.mmf
tools/makesp.pl $traindir/hmm3/hmmdefs.mmf >> $traindir/hmm4/hmmdefs.mmf
recho "...tying middle state of sil with sp"
HHEd -H $traindir/hmm4/hmmdefs.mmf -M $traindir/hmm5 config/sil.hed workdir/phones1.lst
recho "...two more iterations of Embedded Baum-Welch"
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm5/hmmdefs.mmf -M $traindir/hmm6 workdir/phones1.lst
recho "Model $traindir/hmm6/hmmdefs.mmf ready."
HERest -A -C $config0 -C $config -m 1 -I workdir/train_phone1.mlf -t 250.0 150.0 1000.0 -S $trainscp -H $traindir/hmm6/hmmdefs.mmf -M $traindir/hmm7 workdir/phones1.lst
recho "Model $traindir/hmm7/hmmdefs.mmf ready."
recho "Training succesfully terminated."
