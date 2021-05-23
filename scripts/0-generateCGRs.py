'''
Step 0: Generate Chaos Game plots from raw CRISPR data.

author: Jay Turnsek

'''
import csv
import matplotlib.pylab as plt
import numpy as np
import pickle

##########################
####### PARAMETERS #######
##########################

IMG_SIZE = (2**5) - 1   # Odd so center point possible

MIN_SIZE = 4000     # Size of sequence


# This was edited from original; currently reflects use in referenced study
# C  G
# A  T (default)
CORNERS = {
    'C':np.array([0, 0]),
    'G':np.array([0, IMG_SIZE]),
    'A':np.array([IMG_SIZE, 0]),
    'T':np.array([IMG_SIZE, IMG_SIZE])
}

#############################
##### FUNCTIONS DEFINED #####
#############################

def createChaosPlot(seq, size):
    '''
    Rules:
    0- unit square as follows:
    C    G

    A    T
    1- start in centre
    2- go through sequence, letter denotes x
    3- find midpoint of current point and x
    4- plot and repeat


    :param seq: Sequence entered to be plotted
    :param: size: size of array/plot

    :return: 2D numpy array of cgp
    '''

    # init 2D matrix
    plot = np.zeros((size, size))

    # start at middle
    curPos = np.array([size/2, size/2])

    # Find midpoint
    for gene in seq:
        curPos = midpoint(curPos, CORNERS[gene])
        plot[tuple(curPos)] = 1

    return plot


def midpoint(p1, p2):
    '''
    finds midpoint between p1, p2
    :param p1: first point
    :param p2: second point
    :return: array containing rounded midpoint
    '''

    # convert to float
    p1f = p1.astype(np.float64)
    p2f = p2.astype(np.float64)

    # calculate midpoint
    mid = (p1f + p2f) / 2
    return np.around(mid).astype(np.int64)


#################
##### LOAD ######
#################

print('Loading data')
# Load raw CRISPR file
#data = np.array(list(csv.reader(open('../data/CRISPR_' + str(MIN_SIZE) + '.csv', 'r')))).flatten()

# Testing with colors
data = np.array(list(csv.reader(open('../data/CRISPR_' + str(MIN_SIZE) + '_catagorized.csv', 'r')))).flatten()
labels = list(csv.reader(open('../data/CRISPR_labels_' + str(MIN_SIZE) + '.csv', 'r')))

# Testing slice
data = data[:300]

print('Creating plots')



# List of all plots
plots = []
print(labels[0][0])
for i, seq in enumerate(data):
    if labels[i][0] != 'Other':
        # Create plot, add to plots list
        curPlot = createChaosPlot(seq, IMG_SIZE)
        plots.append([labels[i], curPlot])

        # Optional display
        #plt.matshow(curPlot, cmap='binary')
        #plt.axis('off')
        #plt.show()
        #break


print('Saving output')
print(len(plots))
pickle.dump(plots, open(f'../output/plots/{IMG_SIZE}_{MIN_SIZE}.pkl', 'wb'))
