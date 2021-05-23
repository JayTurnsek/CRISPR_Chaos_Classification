"""
Step 2: Get MDS from DSSIM of sequence CGRs.
Uses sklearn's MDS to put distances in an easily understandable dimension; 2D by default.

author: Jay Turnsek

"""

import matplotlib.pyplot as plt
from sklearn.manifold import MDS as MDS
import pickle

####################
#### PARAMETERS ####
####################

## Sizes ##
IMG_SIZE = (2**7)
MIN_SIZE = 2000

## MDS Params ##
N_COMPONENTS = 2
METRIC = True                   # implies classical MDS when true
N_INIT = 15
MAX_ITER = 5000
DISSIMILARITY = 'precomputed'   # DO NOT CHANGE
N_JOBS = -1                     # DO NOT CHANGE

##########################
###### BUILDING MDS ######
##########################

# Meant to be changed. For plotting
colors = {
    'Type I-A': 'blue',
    'Type I-B': 'red',
    'Type I-C': 'green',
    'Type I-D': 'yellow',
    'Type I-E': 'orange',
    'Type I-F': 'purple',
    'Type I-U': 'pink',

    'Type II-A': 'red',
    'Type II-B': 'red',
    'Type II-C': 'red',
    'Type II-D': 'red',
    'Type II-E': 'red',
    'Type II-F': 'red',

    'Type III-A': 'yellow',
    'Type III-B': 'yellow',
    'Type III-C': 'yellow',
    'Type III-D': 'yellow',

    'Type IV': 'green',
    'Type IV-B': 'green',

    'Type V-A': 'black',
    'Type V-B': 'black',

    'CAS-TypeVIB1': 'grey',

    'CAS': 'white'
}

# Load Data
distMat = pickle.load(open(f'../output/distMats/{IMG_SIZE}_{MIN_SIZE}.pkl', 'rb'))
chaosPlots = pickle.load(open(f'../output/plots/{IMG_SIZE}_{MIN_SIZE}.pkl', 'rb'))

# Compute MDS
print('Computing MDS')
mds = MDS(
    n_components=N_COMPONENTS,
    metric=METRIC,
    n_init=N_INIT,
    max_iter=MAX_ITER,
    n_jobs=N_JOBS,
    dissimilarity=DISSIMILARITY
)
embedding = mds.fit_transform(distMat)

# Check if stress < 0.20
stress = mds.stress_
print(stress)


# Plotting
for i, pair in enumerate(embedding):
    # Get color for preexisting class of crispr sequence.
    CASClass = chaosPlots[i][0][0]
    curColor = colors[CASClass]

    # Add to plot
    plt.scatter(embedding[i][0], embedding[i][1], color=curColor)

plt.show()
