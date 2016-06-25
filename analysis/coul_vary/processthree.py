import pdb
import numpy as np
ofinterest = ['Coulomb-14', 'Electrostatic', 'Potential']

# two things: calculate 'Coulomb-14', 'Electrostatic' for the two GROMACS
#             plot 'Coulomb-14', 'Electrostatic' and 'Potential', see how much closer to AMBER when matchin coul

import sys
filename = sys.argv[1]
file = open(filename,'r')
datap = dict()
lines = file.readlines()
names = []
for line in lines:
    if line[0] == 'C':
        name = line.split()[0]
        names.append(name)
    if any([x in line for x in ofinterest]): # are any of the outputs of variables of interest?
        if 'differences' in line:
            continue
        vals = line.split()
        keyf = name + '-' + vals[0] + '-'
        datap[keyf + 'AMBER'] = float(vals[1])
        datap[keyf + 'AMBRC'] = float(vals[2])
        datap[keyf + 'BESTC'] = float(vals[5])
        datap[keyf + 'ORIGC'] = float(vals[8])
#thesis
#GROMACS with AMBER Coul RMSD is much closer to AMBER than when using normal GROMACS         
difforig = dict()
diffamb = dict()
for o in ofinterest:
    difforig[o] = []
    diffamb[o] = []

for n in names:
    for o in ofinterest:
        keyfetch = n + '-' + o + '-' 
        diffamb[o].append(datap[keyfetch + 'AMBER'] - datap[keyfetch + 'AMBRC'])
        difforig[o].append(datap[keyfetch + 'AMBER'] - datap[keyfetch + 'ORIGC'])

print "\nDifferences from original coulomb" 
for o in ofinterest:
    difforig[o] = np.array(difforig[o])
    rmsd = np.sqrt(np.average((difforig[o])**2))
    print "%15s %10.6f" % (o, rmsd)

print "\nDifferences from modified coulomb" 
for o in ofinterest:
    diffamb[o] = np.array(diffamb[o])
    rmsd = np.sqrt(np.average((diffamb[o])**2))
    print "%15s %10.6f" % (o, rmsd)

