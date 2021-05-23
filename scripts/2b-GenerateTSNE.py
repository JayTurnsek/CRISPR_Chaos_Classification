"""
Step 2: Get t-SNE from DSSIM of sequence CGRs.
Uses sklearn's t-SNE to put distances in an easily understandable dimension; 2D by default.

author: Jay Turnsek

"""

import matplotlib.pyplot as plt
import sklearn.manifold as mani
import pickle

###########################
####### PARAMETERS ########
###########################

IMG_SIZE = (2**7)
MIN_SIZE = 1000

# All of these greatly affect tSNE representation. Will take some tweaking based on each dataset.
COMPONENTS = 2
PERPLEXITY = 20
EARLY_EXAGGERATION = 15
LEARNING_RATE = 200
N_ITER = 5000
METRIC = 'precomputed'      # DO NOT CHANGE

# Meant to be changed. For plotting
colors = {
    'CAS-TypeIA': 'blue',
    'CAS-TypeIB': 'blue',
    'CAS-TypeIC': 'blue',
    'CAS-TypeID': 'blue',
    'CAS-TypeIE': 'blue',
    'CAS-TypeIF': 'blue',
    'CAS-TypeIU': 'blue',

    'CAS-TypeIIA': 'red',
    'CAS-TypeIIB': 'red',
    'CAS-TypeIIC': 'red',
    'CAS-TypeIID': 'red',
    'CAS-TypeIIE': 'red',
    'CAS-TypeIIF': 'red',

    'CAS-TypeIIIA': 'yellow',
    'CAS-TypeIIIB': 'yellow',
    'CAS-TypeIIIC': 'yellow',
    'CAS-TypeIIID': 'yellow',

    'CAS-TypeIV': 'green',

    'CAS-TypeVA': 'black',
    'CAS-TypeVB': 'black',

    'CAS-TypeVIB1': 'grey',

    'CAS': 'white'
}

# Load Data
distMat = pickle.load(open(f'../output/distMats/{IMG_SIZE}_{MIN_SIZE}.pkl', 'rb'))
chaosPlots = pickle.load(open(f'../output/plots/{IMG_SIZE}_{MIN_SIZE}.pkl', 'rb'))

# Compute TSNE
tsne = mani.TSNE(
    n_components=COMPONENTS,
    perplexity=PERPLEXITY,
    early_exaggeration=EARLY_EXAGGERATION,
    learning_rate=LEARNING_RATE,
    n_iter=N_ITER,
    metric=METRIC)
embedding = tsne.fit_transform(distMat)

# Plotting
for i, pair in enumerate(embedding):
    # Get color for preexisting classification of crispr sequence.
    CASClass = chaosPlots[i][0][0]
    curColor = colors[CASClass]

    # Add to plot
    plt.scatter(embedding[i, 0], embedding[i, 1], color=curColor)


plt.show()

# Try 3d
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
#ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2])
#plt.show()


