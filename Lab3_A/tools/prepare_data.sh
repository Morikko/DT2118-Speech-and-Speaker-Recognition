#!/bin/bash
# Data preparation for training and testing on the TIDIGIT database. Creates:
# - lists of relevant files,
# - orthographic labels based on the TIDIGIT filenames,
# - phonetic labels based on a dictionary
# - a loop-of-digit grammar
# Used for Lab 3 in the DT2118 Speech and Speaker Recognition course.
#
# Usage:
# ./prepare_data.sh
#
# (C) 2015 Giampiero Salvi <giampi@kth.se>
function recho {
    tput setaf 1;
    echo $1;
    tput sgr0;
}

recho "Preparing data for recognition experiment..."

recho "...creating working directory if not existent"
mkdir -p workdir

recho "...create list of training files"
find tidigits/disc_4.1.1/tidigits/train/ -name "*.wav" > workdir/train.lst
recho "...create list of test files"
find tidigits/disc_4.2.1/tidigits/test/ -name "*.wav" > workdir/test.lst

recho "...create Master Label File (word level, training data)"
tools/list2mlf.py workdir/train.lst > workdir/train_word.mlf
recho "...create Master Label File (word level, test data)"
tools/list2mlf.py workdir/test.lst > workdir/test_word.mlf

recho "...create dictionary with shory pauses"
cat config/pron0.dic | awk '{printf("%s sp\n", $0)}' > workdir/pron1.dic

recho "...expand pronunciations in labels into phonemes WITHOUT short pauses"
HLEd -d config/pron0.dic -i workdir/train_phone0.mlf config/mkphones0.led workdir/train_word.mlf
recho "...expand pronunciations in labels into phonemes WITH short pauses"
HLEd -d workdir/pron1.dic -i workdir/train_phone1.mlf config/mkphones1.led workdir/train_word.mlf

recho "...create list of monophones WITHOUT short pauses"
tools/dict2phones.py config/pron0.dic > workdir/phones0.lst
recho "...create list of monophones WITH short pauses"
tools/dict2phones.py workdir/pron1.dic > workdir/phones1.lst

recho "...generate list of words"
cat config/pron0.dic | awk '{print $1}' > workdir/words.lst

recho "...create recognition grammar (loop of digits)"
tools/words2grammar.py workdir/words.lst > workdir/digitloop.grm
recho "...compile recognition grammar"
HParse workdir/digitloop.grm workdir/digitloop.lat

recho "...add start and end symbols to recognition dictionary"
echo "SENT-START [] sil" > workdir/recdict.dic
echo "SENT-END [] sil" >> workdir/recdict.dic
cat workdir/pron1.dic >> workdir/recdict.dic
recho "Finished."
