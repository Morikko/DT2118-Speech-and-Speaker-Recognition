# Read and Write PFiles
#
# Requires the pfile_utils in the path. On KTH machines run
# module add quicknet pfile_utils
# If you are performing Lab 3B in the DT2118 Speech and Speaker Recognition course, the
# above commands are automatically run when you run source tools/modules
#
# (C) 2016 Giampiero Salvi <giampi@kth.se>

import subprocess
import numpy as np

def pfile_read(filename):
    """ Reads the data in the PFile filename

    Returns 4 arrays:
    utt_ids: utterance ids repeated for every frame (num_frames)
    frame_ids: frame ids (num_frames)
    features: array (num_frames, num_features) of feature values
    labels: array (num_frames, num_labels) of labels (usually num_labels=1) 

    See also pfile_write   
    """
    proc = subprocess.Popen('pfile_info -i '+filename, shell=True, stdout=subprocess.PIPE)
    res = proc.stdout.read()
    _, info = res.splitlines()
    infoa = info.split(' ')
    num_utts = int(infoa[0])
    num_frames = int(infoa[2])
    num_labels = int(infoa[4])
    num_features = int(infoa[6])
    proc = subprocess.Popen('pfile_print -q -i '+filename, shell=True, stdout=subprocess.PIPE)
    data = np.loadtxt(proc.stdout)
    utt_ids = data[:,0]
    frame_ids = data[:,1]
    features = data[:,2:(num_features+2)]
    labels = data[:, (num_features+2):]
    assert labels.shape[1] == num_labels
    return utt_ids, frame_ids, features, labels
    
def pfile_write(filename, utt_ids, frame_ids, features, labels):
    """ Writes a pfile to filename

    utt_ids: utterance ids repeated for every frame (num_frames)
    frame_ids: frame ids (num_frames)
    features: array (num_frames, num_features) of feature values
    labels: array (num_frames, num_labels) of labels (usually num_labels=1) 

    See also pfile_read
    """
    num_frames, num_features = features.shape
    num_label_frames, num_labels = labels.shape
    assert len(utt_ids) == num_frames
    assert len(frame_ids) == num_frames
    assert num_label_frames == num_frames
    cmd = 'pfile_create -i - -o '+filename+' -f '+str(num_features)+' -l '+str(num_labels)
    proc = subprocess.Popen(pfilecmd, shell=True, stdin=subprocess.PIPE)    
    for f in range(num_frames):
        row = str(utt_ids[f])+' '+str(frame_ids[f])+' '+' '.join(map(str, features[f,:]))+' '+' '.join(map(str, labels[f,:]))
        print(row, file=proc.stdin)
