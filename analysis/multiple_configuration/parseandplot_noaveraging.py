# -*- coding: utf-8 -*-
import numpy as np
import pdb

ofinterest = ['Bond', 'Angle', 'All dihedrals', 'Bonded', 'LJ-14', 'Coulomb-14',
              'van der Waals', 'Electrostatic', 'Nonbonded', 'Potential']

# columns each of the programs are found in.
nums = {0: 'AMBER',
        1: 'GROMACS',
        3: 'LAMMPS',
        5: 'DESMOND',
        7: 'CHARMM'
}
import sys
filename = sys.argv[1]
#figure suffix
#figsuff = sys.argv[2]
figsuff = 'DivConf' 
file = open(filename,'r')

lines = file.readlines()
nummol = 0

outlines = dict()
avevals = dict()
aveavals = dict()
avevals2 = dict()
averavals = dict()

data = [avevals, aveavals, avevals2, averavals]
units = ['kJ/mol', 'kJ/mol', 'kJ/mol','fraction']
convert = [4.184, 4.184, 4.184, 1]
#convert = [1, 1, 1, 1]
types = ['Average', 'Average Absolute', 'Average RMSD','Average Relative Absolute']

# make a dict for each program
for d in data:
    for o in ofinterest:
        d[o] = dict()
        for n in nums:
            d[o][nums[n]] = 0

nskip = 10
for i in range(len(lines)):
    line = lines[i]

    if line[0:4] == 'INFO':
        continue
    if line[0:7] == 'gromacs':
        vals = line.split('/')

        name = vals[7]

    if line[0:6] == 'Energy':
        starti = i+3
        dictvals = dict()
        dictdiff = dict()

        for j in range(starti,starti+nskip):
            shortline = lines[j][20:]
            vals = shortline.split()
            if len(vals) > 0:
                o = lines[j][:20].strip()
                dicttypes = dict()
                dictdtypes = dict()
                if o in ofinterest:
                    eave = 0
                    nprog = 0
                    for n in nums:
                        v = vals[n]
                        if v != 'n/a':
                            v = float(v)
                            eave += v
                            nprog += 1
                        dicttypes[nums[n]] = v
                    eave /= nprog
                    dictvals[o] = dicttypes
                    for n in nums:
                        if dicttypes[nums[n]] != 'n/a':
                            dictdtypes[nums[n]] = dicttypes[nums[n]] - eave
                        else:
                            dictdtypes[nums[n]] = 'n/a'
                    dictdiff[o] = dictdtypes

                    for n in nums:
                        v = dictdtypes[nums[n]]
                        if v != 'n/a':
                            avevals[o][nums[n]] += v
                            aveavals[o][nums[n]] += abs(v)
                            avevals2[o][nums[n]] += v*v
                            averavals[o][nums[n]] += abs(v)/abs(eave)
                        else:
                            for d in data:
                                d[o][nums[n]] = 'n/a'

        olines = list()
        olines.append("\n****************")
        olines.append(name)
        nummol += 1
        olines.append("****************")

        l = "              "
        names = nums.values()
        for k in names:
            l += "%13s" % (k)
        olines.append(l)
        for o in ofinterest:
            l = "%14s" % o
            for n in nums.values():
                v = dictvals[o][n]
                if v == 'n/a':
                    l += "%15s" % v
                else:
                    l += "%15.7f" % v
            olines.append(l)

        for o in ofinterest:
            olines.append("\n%s energy differences" % (o) )

            l = '        '
            for k in names:
                l += "%13s" % (k)
            olines.append(l)
            for k, n1 in enumerate(names):
                l = "%8s" % (names[k])
                for n2 in names:
                    if dictvals[o][n1] == 'n/a' or dictvals[o][n2] == 'n/a':
                        l += "%13s" % ('n/a')
                    else:
                        l += "%13.7f" % (dictvals[o][n1] - dictvals[o][n2])
                olines.append(l)
            outlines[name] = olines
        i = starti + nskip

keylist = outlines.keys()
keylist.sort()
for key in keylist:
    lines = outlines[key]
    for l in lines:
        print l

for o in ofinterest:
    for n in nums:
        if avevals[o][nums[n]] != 'n/a':  # only need to check the first one
            for d in data:
                d[o][nums[n]] /= nummol

for o in ofinterest:
    for n in nums:
        if avevals2[o][nums[n]] != 'n/a':  # only need to check the first one  
            avevals2[o][nums[n]] = np.sqrt(avevals2[o][nums[n]]-avevals[o][nums[n]]**2)

import numpy as np
import matplotlib.pyplot as plt

# print summary information
for i, t in enumerate(types):
    print ''
    print t
    print "%20s" % (''),
    for n in nums:
        print "%20s" % (nums[n]),
    print '\n'
    for o in ofinterest:
        print "%20s" % (o),
        for n in nums:
            if (data[i][o][nums[n]]) != 'n/a':
                print "%20.8f" % (data[i][o][nums[n]]),
            else:
                print '%20s' % ('n/a'),
        print ''

for i, t in enumerate(types):
    # data to plot
    n_groups = len(ofinterest)
    allmeans = dict()
    for n in nums:
        means = []
        for o in ofinterest:
            if avevals[o][nums[n]] != 'n/a':
                means.append(data[i][o][nums[n]]/convert[i])
            else:
                means.append(0)
        allmeans[nums[n]] = means    

