"""
Step 0: Generate Chaos Game plots from raw CRISPR data.
ref:
https://towardsdatascience.com/chaos-game-representation-of-a-genetic-sequence-4681f1a67e14

author: Jay Turnsek

"""
import collections
import pickle
import numpy as np
import csv


#######################
##### PARAMETERS ######
#######################
KMER_SIZE = 7
MIN_SIZE = 1000


IMG_SIZE = (2**KMER_SIZE)

#############################
##### FUNCTIONS DEFINED #####
#############################


def count_kmers(sequence, k):
    """
    Counts amount of each kmer of size k in sequence.
    :param sequence: DNA sequence to be checked
    :param k: Size of kmer's to be read. See KMER_SIZE in parameters.
    :return: dict of each kmer and how many times it's found.
    """
    d = collections.defaultdict(int)
    for i in range(len(data) - (k - 1)):
        d[sequence[i:i + k]] += 1
    for key in list(d):
        if "N" in key:
            del d[key]
    return d


def probabilities(kmer_count, k):
    """
    Finds probabilities for each kmer, in the respective sub-quadrant of the chaos plot.
    :param kmer_count: Dict of occurrences of each kmer of size k.
    :param k: Size of kmer. See KMER_SIZE in parameters.
    :return: Dict of probabilities for each.
    """
    probabilitiesDict = collections.defaultdict(float)
    N = len(data)
    for key, value in kmer_count.items():
        probabilitiesDict[key] = float(value) / (N - k + 1)
    return probabilitiesDict


def createChaosPlot(probabilities, size):
    """
    Generate chaos game plot based on DNA sequence.

    Rules:
    0- unit square as follows:
    C    G

    A    T
    1- Divide quadrants in each direction based on kmer sequence
    2- Set color within range of white -> black as probability goes from 0 -> 1.

    :param probabilities: Dict of probabilities for each kmer in sequence
    :param: size: size of array/plot

    :return: 2D numpy array of cgp
    """

    # init 2D matrix
    plot = np.zeros((size, size))

    # start at middle
    maxx = size
    maxy = size
    posx = 1
    posy = 1

    for key, value in probabilities.items():
        # For each kmer, find correct plotting position
        for char in key:
            # Divide quadrants in direction of character
            if char == "T":
                posx += maxx / 2
            elif char == "C":
                posy += maxy / 2
            elif char == "G":
                posx += maxx / 2
                posy += maxy / 2
            maxx = maxx / 2
            maxy /= 2
        # Plot probability
        plot[int(posy) - 1][int(posx) - 1] = value

        # Reinitialize
        maxx = size
        maxy = size
        posx = 1
        posy = 1

    return plot


#################
#### LOADING ####
#################


# Load sequences to get CGR of
data = np.array(list(csv.reader(open(f'../data/crisprDB_{MIN_SIZE}.csv', 'r')))).flatten()
labels = list(csv.reader(open(f'../data/crisprDB_{MIN_SIZE}_labels.csv', 'r')))

# Data slicer
data = data[:250]
plots = []
for i, seq in enumerate(data):
    if labels[i][0] != 'Type I-U' and labels[i][0] != 'Other':
        # Create plot, add to plots list
        kmerData = count_kmers(seq, KMER_SIZE)
        probData = probabilities(kmerData, KMER_SIZE)
        curPlot = createChaosPlot(probData, IMG_SIZE)
        plots.append([labels[i], curPlot])

        # Optional display
        #plt.imshow(curPlot, cmap='Greys', interpolation='nearest')
        #plt.show()
        break

print('Saving output')
print(len(plots))
pickle.dump(plots, open(f'../output/plots/{IMG_SIZE}_{MIN_SIZE}.pkl', 'wb'))