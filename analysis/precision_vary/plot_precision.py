# -*- coding: utf-8 -*-
import numpy as np
import pdb
import matplotlib.pyplot as plt

ofinterest = ['Bond', 'Angle', 'All dihedrals', 'Bonded', 'LJ-14', 'Coulomb-14',
              'van der Waals', 'Electrostatic', 'Nonbonded', 'Potential']

figsuff = 'precision'
files = ['analyze7.txt','analyze6.txt','analyze5.txt','analyze4.txt','analyze3.txt']
labels = ['8 decimal places' ,'7 decimal places','6 decimal places','5 decimal places','4 decimal places']  
           # number of decimal places in nm 
precisions = list()
n_groups = len(ofinterest)
for f in files:
    values = dict()
    lines = open(f,'r').readlines()
    for i, line in enumerate(lines):
        if 'Average Relative Absolute' in line:
            start = i+3
    for i in range(start,len(lines)):
        line = lines[i]
        name = line[:20].strip()
        values[name] = -np.log10(float((line[20:].split())[1]))    # just use the GROMACS number
    precisions.append(values)
    
fig, ax = plt.subplots(figsize=(20,6))

index = np.arange(n_groups)
bar_width = 0.18
opacity = 1
colors = ('b','r','c','g','m')
for  j, l in enumerate(labels):  
    rects = ax.bar(index+bar_width*j, precisions[j].values(), 
                   bar_width, alpha=opacity,
                   color=colors[j], label=str(labels[j]))

ax.set_xlabel('Energy Component', fontsize=20)
ax.set_ylabel(r'$-\log_{10}$(Relative Deviation'+'\nfrom AMBER Full Precision)', fontsize=18)
ax.set_title('Log Deviation in Energy Components as a Function of Coordinate Precision', fontsize=24)
ax.set_xticks(index + bar_width + 0.2)
ax.set_xticklabels(ofinterest, fontsize=16)
ax.legend(loc = 'upper left')

plt.savefig('../../figures/precisioncomparison.pdf')

