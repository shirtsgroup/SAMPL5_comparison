import pdb
import numpy as np
ofinterest = ['Bond', 'Angle', 'All dihedrals', 'Bonded', 'LJ-14', 'Coulomb-14',
              'van der Waals', 'Electrostatic', 'Nonbonded', 'Potential']

conv = 4.184
# how different are single and double precision gromacs?
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
        etype = line[0:14].strip()
        keyf = name + '-' + etype + '-'
        datap[keyf + 'AMBER'] = float(line[14:29])/conv
        datap[keyf + 'SINGLE'] = float(line[30:44])/conv
        datap[keyf + 'DOUBLE'] = float(line[74:89])/conv

diffgro = dict()
diffambsingle = dict()
diffambdouble = dict()
for o in ofinterest:
    diffgro[o] = []
    diffambsingle[o] = []
    diffambdouble[o] = []

for n in names:
    for o in ofinterest:
        keyfetch = n + '-' + o + '-'
        diffgro[o].append(datap[keyfetch + 'SINGLE'] - datap[keyfetch + 'DOUBLE'])
        diffambsingle[o].append(datap[keyfetch + 'AMBER'] - datap[keyfetch + 'SINGLE'])
        diffambdouble[o].append(datap[keyfetch + 'AMBER'] - datap[keyfetch + 'DOUBLE'])

#print output as latex table
print "% col 2: \nDifferences between single and double" 
print "% col 3: \nDifferences between amber and single" 
print "% col 4: \nDifferences between amber and double"
print "E term & RMS($E_{single} - E_{double}$) &  RMS($E_{amber} - E_{single}$) &  RMS($E_{amber} - E_{double}$) \\\\"  
for o in ofinterest:
    diffgro[o] = np.array(diffgro[o])
    rmsd1 = np.sqrt(np.average((diffgro[o])**2))
    diffambsingle[o] = np.array(diffambsingle[o])
    rmsd2 = np.sqrt(np.average((diffambsingle[o])**2))
    diffambdouble[o] = np.array(diffambdouble[o])
    rmsd3 = np.sqrt(np.average((diffambdouble[o])**2))
    print "%15s & %10.6f & %10.6f & %10.6f\\\\" % (o, rmsd1, rmsd2, rmsd3)

