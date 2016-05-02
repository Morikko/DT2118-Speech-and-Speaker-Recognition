import numpy as np
from tools2 import *
import matplotlib.pyplot as plt

def gmmloglik(log_emlik, weights):
    """Log Likelihood for a GMM model based on Multivariate Normal Distribution.

    Args:
        log_emlik: array like, shape (N, K).
            contains the log likelihoods for each of N observations and
            each of K distributions
        weights:   weight vector for the K components in the mixture

    Output:
        gmmloglik: scalar, log likelihood of data given the GMM model.
    """
    # Or np.sum(tools2.logsumexp(A+w, axis=1)) with w the weights in log domain
    return np.sum( np.log( np.dot( np.exp(log_emlik), weights) ) )

def forward(log_emlik, log_startprob, log_transmat):
    """Forward probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: log transition probability from state i to j

    Output:
        forward_prob: NxM array of forward log probabilities for each of the M states in the model
    """
    N, M = log_emlik.shape
    log_alpha = np.zeros([N, M])
    for j in range(M):
        log_alpha[0, j] = log_startprob[j] + log_emlik[0, j]

    for i in range(1, N):
        for j in range(M):
            log_alpha[i, j] = logsumexp( log_alpha[i-1] +  log_transmat[:, j] ) + log_emlik[i, j]

    return log_alpha


def backward(log_emlik, log_startprob, log_transmat):
    """Backward probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        backward_prob: NxM array of backward log probabilities for each of the M states in the model
    """
    N, M = log_emlik.shape
    backward_prob = np.zeros([N, M])

    for n in range(N-2, -1, -1):
        for i in range(M):
            backward_prob[n, i] = logsumexp( log_transmat[i, :] + log_emlik[n+1, :] + backward_prob[n+1, :])

    return backward_prob


def viterbi(log_emlik, log_startprob, log_transmat):
    """Viterbi path.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        viterbi_loglik: log likelihood of the best path
        viterbi_path: best path
    """
    N, M = log_emlik.shape
    viterbi_path = np.zeros([N,])
    V = np.zeros([N, M])
    B = np.zeros([N, M])

    for j in range(M):
        V[0, j] = log_startprob[j] + log_emlik[0, j]

    for i in range(1, N):
        for j in range(M):
            V[i, j] = max( V[i-1, :] + log_transmat[:, j] ) + log_emlik[i, j]
            B[i, j] = np.argmax( V[i-1, :] + log_transmat[:, j] )

    viterbi_path[N-1] = np.argmax(V[N-1, :])
    viterbi_loglik = V[N-1, viterbi_path[N-1]]

    for i in range(N-2, -1, -1):
        viterbi_path[i] = B[i+1, viterbi_path[i+1]]
            
    return viterbi_loglik, viterbi_path

def show(data):
    plt.imshow(data.transpose(), origin='lower', interpolation='nearest', aspect='auto')
