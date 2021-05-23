'''
Step 1: Generate DSSIM plots relating CGRs, using SSIM from skimage.
Just sees how different each plot is from eachother.

author: Jay Turnsek

'''

import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim
import pickle
import time

#########################
###### PARAMETERS #######
#########################

MIN_SIZE = 1000
IMG_SIZE = (2**7)


# Load data from CGR generation
chaosPlots = pickle.load(open(f'../output/plots/{IMG_SIZE}_{MIN_SIZE}.pkl', 'rb'))


# Initialize distance matrix
distMat = np.zeros((len(chaosPlots), len(chaosPlots)))

# Progress monitor
print(len(chaosPlots))
n = 0

# Compute distance matrix.
# TODO: implement parallel setup for this part.
for i, plotx in enumerate(chaosPlots):
	for j, ploty in enumerate(chaosPlots):

		# Get DSSIM of i and j
		# DSSIM = 1 - SSIM.
		distMat[i][j] = (1-(ssim(chaosPlots[i][1], chaosPlots[j][1])))

	# Progress monitor
	print(n)
	n += 1

# Optional Display
plt.imshow(distMat, cmap='Greys', interpolation='nearest')
plt.show()

pickle.dump(distMat, open('../output/distMats/' + str(IMG_SIZE) + '_' + str(MIN_SIZE) + '.pkl', 'wb'))

