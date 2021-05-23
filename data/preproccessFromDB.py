'''
Script to proccess data from CRISPR-CAS++ DB (https://crisprcas.i2bc.paris-saclay.fr/).
Takes in text file generated from QUERIES.txt in main directory.

Author: Jay Turnsek
'''
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Cleaning
f = open("out.txt", "r")
fData = f.readlines()
content = [x.strip('\n').split('\t') for x in fData]

# Size parameter. Sets minimum size of sequence
SIZE = 1000

o1 = open(f"crisprDB_{SIZE}.txt", "w")
o2 = open(f"crisprDB_{SIZE}_labels.txt", "w")

# Used to monitor progress.
counter = len(content)

# Get sequence from each crispr in CRISPR-CAS++ DB
for crispr in content:

    # Grab uid for NCBI sequence. This is not present in database but required for the GET request we need.
    URL = f'https://www.ncbi.nlm.nih.gov/nuccore/{crispr[3]}?report=fasta'
    soup = BeautifulSoup(urlopen(URL))
    data = soup.find("meta", {"name": "ncbi_uidlist"})
    uid = data['content']

    # Set sequence range.
    start = crispr[1]
    end = crispr[2]

    # GET the sequence we want, then put it in a single line string.
    outURL = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=' + str(
        uid) + '&db=nuccore&report=fasta&extrafeat=null&conwithfeat=on&hide-cdd=on&from=' + str(start) + '&to=' + str(
        end) + '&retmode=html&tool=portal&log$=seqview'
    soup = BeautifulSoup(urlopen(outURL), features='html.parser')
    text = soup.text
    text = text.splitlines()
    text = text[1:]
    out = ''
    for t in text:
        out += t

    # Test if meets desired size
    if len(out) >= SIZE:
        # Write sequence to each line
        o1.write(out)
        o1.write('\n')

        # Write corresponding class to same line # as related sequence
        o2.write(crispr[0])
        o2.write('\n')

    # Progress monitor
    print(counter)
    counter -= 1

f.close()
o1.close()
o2.close()

