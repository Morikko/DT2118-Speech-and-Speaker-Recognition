import numpy as np
import matplotlib.pyplot as plt
import sklearn.mixture as skm
import proto2
import tools2

reload(proto2)

tidigits = np.load('lab2_tidigits.npz')['tidigits']
models = np.load('lab2_models.npz')['models']
example = np.load('lab2_example.npz')['example'].item()

plt.figure(1)

# Plot Mfcc 
plt.subplot(511)
plt.imshow(example['mfcc'].transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 4: Multivariate Gaussian Density
gmm_obsloglik = skm.log_multivariate_normal_density(example['mfcc'],
                                models[0]['gmm']['means'],
                                models[0]['gmm']['covars'], 'diag')

hmm_obsloglik = skm.log_multivariate_normal_density(example['mfcc'],
                                models[0]['hmm']['means'],
                                models[0]['hmm']['covars'], 'diag')

plt.subplot(512)
plt.imshow(gmm_obsloglik.transpose(), origin='lower', interpolation='nearest', aspect='auto')
plt.subplot(513)
plt.imshow(hmm_obsloglik.transpose(), origin='lower', interpolation='nearest', aspect='auto')

# Compute 5 : GMM Likelihood and Recognition
# Retrieve example['gmm_loglik']
gmmloglik = proto2.gmmloglik(gmm_obsloglik, models[0]['gmm']['weights'])

## Try every models on each utterances (tidigits) and find the best --> conclude
gmm_class = []
# For each utterances
for i in range(len(tidigits)):
    loglik = np.zeros(len(models))
    for j in range(len(models)):
        model = skm.log_multivariate_normal_density(tidigits[i]['mfcc'],
                models[j]['gmm']['means'],
                models[j]['gmm']['covars'], 'diag')
        loglik[j] = proto2.gmmloglik(model, models[j]['gmm']['weights'])
    gmm_class.append(loglik)

gmm_class = np.array(gmm_class)
# Find bigger values for each utterances
gmm_ret_labels = np.argmax(gmm_class, axis=1)

# Compute 6: HMM Likelihood and Recognition
log_alpha = proto2.forward(hmm_obsloglik, np.log(models[0]['hmm']['startprob']), np.log(models[0]['hmm']['transmat']) )

# Compute marginalization:
hmm_loglik = tools2.logsumexp( log_alpha[-1, :] )

# Try every models on each utterances (tidigits) and find the best --> conclude
hmm_class = []
# For each utterances
for i in range(len(tidigits)):
    loglik = np.zeros(len(models))
    for j in range(len(models)):
        model = skm.log_multivariate_normal_density(tidigits[i]['mfcc'],
                models[j]['hmm']['means'],
                models[j]['hmm']['covars'], 'diag')
        log_alpha_class = proto2.forward(model, np.log(models[j]['hmm']['startprob']), np.log(models[j]['hmm']['transmat']) )
        loglik[j] = tools2.logsumexp( log_alpha_class[-1, :] )
    hmm_class.append(loglik)

hmm_class = np.array(hmm_class)
# Find bigger values for each utterances
hmm_ret_labels = np.argmax(hmm_class, axis=1)

# Verify the HMM model with the likelihood way of GMM whit equal weight
hmm_gmm_class = []
# For each utterances
for i in range(len(tidigits)):
    loglik = np.zeros(len(models))
    for j in range(len(models)):
        model = skm.log_multivariate_normal_density(tidigits[i]['mfcc'],
                models[j]['hmm']['means'],
                models[j]['hmm']['covars'], 'diag')
        #log_alpha_class = proto2.forward(model, np.log(models[j]['hmm']['startprob']), np.log(models[j]['hmm']['transmat']) )
        N, M = model.shape
        loglik[j] = proto2.gmmloglik(model, np.ones([M,])*(1./M))
    hmm_gmm_class.append(loglik)

hmm_gmm_class = np.array(hmm_gmm_class)
# Find bigger values for each utterances
hmm_gmm_ret_labels = np.argmax(hmm_gmm_class, axis=1)

# Part 2 - Viterbi approximation
vit_loglik, vit_path = proto2.viterbi(hmm_obsloglik, np.log(models[0]['hmm']['startprob']), np.log(models[0]['hmm']['transmat']))

# Try every models on each utterances (tidigits) and find the best --> conclude
viterbi_class = []
viterbi_level = []
# For each utterances
for i in range(len(tidigits)):
    loglik = np.zeros(len(models))
    path = np.zeros(len(models))
    for j in range(len(models)):
        model = skm.log_multivariate_normal_density(tidigits[i]['mfcc'],
                models[j]['hmm']['means'],
                models[j]['hmm']['covars'], 'diag')
        loglik[j], tmp = proto2.viterbi(model, np.log(models[j]['hmm']['startprob']), np.log(models[j]['hmm']['transmat']) )
        path[j] = tmp[-1]
    viterbi_class.append(loglik)
    viterbi_level.append(path)

viterbi_class = np.array(viterbi_class)
viterbi_level = np.array(viterbi_level)
# Find bigger values for each utterances
vit_ret_labels = np.argmax(viterbi_class, axis=1)

# Compute backward
log_beta= proto2.backward(hmm_obsloglik, np.log(models[0]['hmm']['startprob']), np.log(models[0]['hmm']['transmat']) )

# Try every models on each utterances (tidigits) and find the best --> conclude
hmm_bk_class = []
# For each utterances
for i in range(len(tidigits)):
    loglik = np.zeros(len(models))
    for j in range(len(models)):
        model = skm.log_multivariate_normal_density(tidigits[i]['mfcc'],
                models[j]['hmm']['means'],
                models[j]['hmm']['covars'], 'diag')
        log_beta_class = proto2.backward(model, np.log(models[j]['hmm']['startprob']), np.log(models[j]['hmm']['transmat']) )
        loglik[j] = tools2.logsumexp( log_beta_class[0, :] )
    hmm_bk_class.append(loglik)

hmm_bk_class = np.array(hmm_bk_class)
# Find bigger values for each utterances
hmm_bk_ret_labels = np.argmax(hmm_bk_class, axis=1)
