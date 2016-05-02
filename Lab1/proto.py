# DT2118, Lab 1 Feature Extraction
# Functions to be implemented ----------------------------------
import numpy as np
import scipy.signal as ss
import scipy.fftpack
import tools
import matplotlib.pyplot as plt

def enframe(samples, winlen, winshift):
    """
    Slices the input samples into overlapping windows.

    Args:
        winlen: window length in samples.
        winshift: shift of consecutive windows in samples
    Returns:
        numpy array [N x winlen], where N is the number of windows that fit
        in the input signal
    """

    ls = []
    for i in range(0, len(samples)/winlen*winlen, winshift):
        if i+winlen > len(samples):
            break
        ls.append(samples[i:i+winlen])

    return np.array(ls)

def preemp(input, p=0.97):
    """
    Pre-emphasis filter.

    Args:
        input: array of speech frames [N x M] where N is the number of frames and
               M the samples per frame
        p: preemhasis factor (defaults to the value specified in the exercise)

    Output:
        output: array of pre-emphasised speech samples
    Note (you can use the function lfilter from scipy.signal)
    """
    # Attention a mettre une virgule dans la creation du tableau b !!!!
    return ss.lfilter([1, -p], [1], input)


def windowing(input):
    """
    Applies hamming window to the input frames.

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
    Output:
        array of windoed speech samples [N x M]
    Note (you can use the function hamming from scipy.signal, include the sym=0 option
    if you want to get the same results as in the example)
    """
    N, M = input.shape
    window = ss.hamming(M, sym=False)
    return (input * window)
    
def powerSpectrum(input, nfft):
    """
    Calculates the power spectrum of the input signal, that is the square of the modulus of the FFT

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
        nfft: length of the FFT
    Output:
        array of power spectra [N x nfft]
    Note: you can use the function fft from scipy.fftpack
    """
    freq = scipy.fftpack.fft(input, nfft)
    return freq.real**2 + freq.imag**2


def logMelSpectrum(input, samplingrate):
    """
    Calculates the log output of a Mel filterbank when the input is the power spectrum

    Args:
        input: array of power spectrum coefficients [N x nfft] where N is the number of frames and
               nfft the length of each spectrum
        samplingrate: sampling rate of the original signal (used to calculate the filterbanks)
    Output:
        array of Mel filterbank log outputs [N x nmelfilters] where nmelfilters is the number
        of filters in the filterbank
    Note: use the trfbank function provided in tools.py to calculate the filterbank shapes and
          nmelfilters
    """
    N, nfft = input.shape
    flt = tools.trfbank(samplingrate, nfft)
    return np.log( np.dot( input, flt.transpose() ) )


def cepstrum(input, nceps):
    """
    Calulates Cepstral coefficients from mel spectrum applying Discrete Cosine Transform

    Args:
        input: array of log outputs of Mel scale filterbank [N x nmelfilters] where N is the
               number of frames and nmelfilters the length of the filterbank
        nceps: number of output cepstral coefficients
    Output:
        array of Cepstral coefficients [N x nceps]
    Note: you can use the function dct from scipy.fftpack.realtransforms
    """
    return scipy.fftpack.dct(input, norm='ortho')[:, 0:nceps]

def dtw(localdist):
    """Dynamic Time Warping.

    Args:
        localdist: array NxM of local distances computed between two sequences
                   of length N and M respectively

    Output:
        globaldist: scalar, global distance computed by Dynamic Time Warping
    """
    N, M = localdist.shape
    acc = np.zeros(localdist.shape)
    acc[0][0] = localdist[0][0]
    for i in range(1, N):
        off = localdist[i][0]
        acc[i][0] = acc[i-1][0] + off
    for j in range(1, M):
        off = localdist[0][j]
        acc[0][j] = acc[0][j-1] + off

    for i in range(1, N):
        for j in range(1, M):
            off = localdist[i][j]
            acc[i][j] = min( acc[i-1][j], acc[i-1][j-1], acc[i][j-1]  ) + off

    return acc[N-1][M-1]



def localDistances(ut1, ut2):
    """ Compute Euclidean distance between two uterances
    
    Args:
        ut1 and ut2 the two utterances of size N and M
    Output:
        Matrix [N x M] with the euclidean distance between each vector
    """
    N = len(ut1)
    M = len(ut2)
    ld = np.zeros([N, M])
    for i in range(N):
        for j in range(M):
            ld[i][j] = np.linalg.norm(ut1[i] - ut2[j])

    return ld



def show(input):
    plt.clf()
    plt.imshow(input.transpose(), origin='lower', interpolation='nearest', aspect='auto')
    plt.show()
