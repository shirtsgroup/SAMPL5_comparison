import numpy as np
import pdb

ofinterest = ['Bond', 'Angle', 'All dihedrals', 'Bonded', 'LJ-14', 'Coulomb-14',
              'van der Waals', 'Electrostatic', 'Nonbonded', 'Potential']

nums = {0: 'AMBER',
        1: 'GROMACS',
}
import sys

filename = sys.argv[1]
file = open(filename,'r')

lines = file.readlines()

outlines = dict()

for i in range(len(lines)):
    line = lines[i]

    if line[0:4] == 'INFO':
        continue
    if line[0:7] == 'gromacs':
        vals = line.split('/')

        name = vals[6]
    if line[0:6] == 'Energy':
        starti = i+3
        dictvals = {}
        for j in range(starti,starti+27):
            vals = lines[j].split()
            if len(vals) > 0:
                shortline = lines[j][20:]
                vals = shortline.split()
                typename = lines[j][:20].strip()
                dicttypes = {}
                if typename in ofinterest:
                    for n in nums.keys():
                        v = vals[n]
                        if v != 'n/a':
                            v = float(v)
                        dicttypes[nums[n]] = v
                    dictvals[typename] = dicttypes

        olines = list()
        olines.append("****************")
        olines.append(name)
        olines.append("****************")

        l = "              "
        names = nums.values()
        for k in names:
            l += "%13s" % (k)
        olines.append(l)
        for typename in ofinterest:
            if typename != 'Disper.corr.':
                l = "%14s" % typename
                for n in nums.values():
                    v = dictvals[typename][n]
                    if v == 'n/a':
                        l += "%15s" % v
                    else:
                        l += "%15.7f" % v
            olines.append(l)
        olines.append("\n")    
        olines.append("Potential energy differences")

        l = '        '
        for k in names:
            l += "%13s" % (k)
        olines.append(l)
        for k, n1 in enumerate(names):
            l = "%8s" % (names[k])
            for n2 in names:
                l += "%13.7f" % (dictvals['Potential'][n1] - dictvals['Potential'][n2])
            olines.append(l)
        outlines[name] = olines
        i = starti + 27

keylist = outlines.keys()
keylist.sort()
for key in keylist:
    lines = outlines[key]
    for l in lines:
        print l
