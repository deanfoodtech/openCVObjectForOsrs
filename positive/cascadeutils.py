import os
import sys

# Add the directory containing cascadeutils.py to sys.path
sys.path.append(r'C:/Users/Nunu/PycharmProjects/openCVscanRed')

# Now you should be able to import the module
from cascadeutils import generate_neg_description_file
def generate_neg_description_file():
    #open the outpu file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        #loop over all the file names
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')