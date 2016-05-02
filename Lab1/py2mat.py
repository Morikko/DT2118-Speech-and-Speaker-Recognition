from scipy.io import savemat
import numpy as np

tidigits = np.load('tidigits.npz')
savemat('tidigits.mat', tidigits)
