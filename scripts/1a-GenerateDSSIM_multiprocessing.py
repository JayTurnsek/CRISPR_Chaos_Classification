"""
TODO: Complete this.
Step 1: Generate DSSIM plots relating CGRs

author: Jay Turnsek *INCOMPLETE*

"""

import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim
import pickle
from joblib import Parallel, delayed
import time

#########################
###### PARAMETERS #######
#########################

MIN_SIZE = 1000
IMG_SIZE = (2**7)-1


## Load data from CGR generation ##
chaosPlots = pickle.load(open('../output/plots/' + str(IMG_SIZE) + '_' + str(MIN_SIZE) + '.pkl', 'rb'))


## Creating distance matrix ##
distMat = np.zeros((len(chaosPlots), len(chaosPlots)))


def getDSSIM(i1, i2, i, j, matrix):
	SSIM = ssim(i1, i2, data_range=1)
	DSSIM = (1 - SSIM) / 2
	matrix[i][j] = DSSIM



ts = time.time()
Parallel(n_jobs=-1)(delayed(getDSSIM)(chaosPlots[i], chaosPlots[j], i, j, distMat) for j, ploty in enumerate(chaosPlots) for i, plotx in enumerate(chaosPlots))
print('time elapsed: ' + str(time.time() - ts))

distMat = np.zeros((len(chaosPlots), len(chaosPlots)))

ts = time.time()
## Compute distance matrix ##
for i, plotx in enumerate(chaosPlots):
	for j, ploty in enumerate(chaosPlots):

		# Get DSSIM of i and j ##
		distMat[i][j] = (1-(ssim(chaosPlots[i], chaosPlots[j]))) / 2
print('time elapsed: ' + str(time.time() - ts))


'''
plt.imshow(distMat, cmap='hot', interpolation='nearest')
plt.show()

pickle.dump(distMat, open('../output/distMats/' + str(IMG_SIZE) + '_' + str(MIN_SIZE) + '.pkl', 'wb'))


result = ssim(chaosPlots[8], chaosPlots[9], win_size=5, gradient=True, data_range=1)
print(1-result[0])
plt.imshow(result[1], cmap='hot', interpolation='nearest')
plt.show()

'''
