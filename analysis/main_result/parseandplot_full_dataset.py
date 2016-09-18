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
figsuff = sys.argv[2] 
file = open(filename,'r')

lines = file.readlines()
nummol = 0

outlines = dict()
avevals = dict()
aveavals = dict()
averavals = dict()

# make a dict for each program
for o in ofinterest:
    avevals[o] = dict()
    aveavals[o] = dict()
    averavals[o] = dict()
    for n in nums:
        avevals[o][nums[n]] = 0
        aveavals[o][nums[n]] = 0
        averavals[o][nums[n]] = 0

nskip = 10
for i in range(len(lines)):
    line = lines[i]

    if line[0:4] == 'INFO':
        continue
    if line[0:7] == 'gromacs':
        vals = line.split('/')

        name = vals[6]
    if line[0:6] == 'Energy':
        starti = i+3
        dictvals = dict()
        dictdiff = dict()
        for j in range(starti,starti+nskip):
            shortline = lines[j][20:]
            vals = shortline.split()
            if len(vals) > 0:
                typename = lines[j][:20].strip()
                dicttypes = dict()
                dictdtypes = dict()
                if typename in ofinterest:
                    eave = 0
                    nprog = 0
                    for n in nums.keys():
                        v = vals[n]
                        if v != 'n/a':
                            v = float(v)
                            eave += v
                            nprog += 1
                        dicttypes[nums[n]] = v
                    eave /= nprog
                    dictvals[typename] = dicttypes
                    for n in nums.keys():
                        if dicttypes[nums[n]] != 'n/a':
                            dictdtypes[nums[n]] = dicttypes[nums[n]] - eave
                        else:
                            dictdtypes[nums[n]] = 'n/a'
                    dictdiff[typename] = dictdtypes

                    for n in nums.keys():
                        if dictdtypes[nums[n]] != 'n/a':
                            avevals[typename][nums[n]] += dictdtypes[nums[n]]
                            aveavals[typename][nums[n]] += abs(dictdtypes[nums[n]])
                            averavals[typename][nums[n]] += abs(dictdtypes[nums[n]])/abs(eave)
                        else:
                            avevals[typename][nums[n]] = 'n/a'
                            aveavals[typename][nums[n]] = 'n/a'
                            averavals[typename][nums[n]] = 'n/a'


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
        for typename in ofinterest:
            l = "%14s" % typename
            for n in nums.values():
                v = dictvals[typename][n]
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

'''
now generate the graphs 10 terms (or fewer), and 5 programs 10 groups,
with 5 points per group (one for each program) What do we plot in each
bar chart?  could plot the RMDS from the average of all five programs
for each molecule over 22 molecules, calculate for each molecule/term
the average energy between all programs. 

"Since we can't necessarily say which program is most right, we
compare the absolute deviation of each program from the mutual
average, averaged over 22 host-guest systems. In figure X, we show
this average relative deviation for 10 different components of the
potential energy. Because the magitude of these deviations is so
different.

''' 
for o in ofinterest:
    for n in nums:
        if avevals[o][nums[n]] != 'n/a':  # only need to check the first one
            avevals[o][nums[n]] /= nummol
            aveavals[o][nums[n]] /= nummol 
            averavals[o][nums[n]] /= nummol
import numpy as np
import matplotlib.pyplot as plt

types = ['Average', 'Average Absolute','Average Relative Absolute']
data = [avevals, aveavals, averavals]
units = ['kJ/mol', 'kJ/mol', 'fraction']  # because amber is input, energies are in kcal/mol.  Convert to kJ/mol
convert = [4.184, 4.184, 1]
for i, t in enumerate(types):
    # data to plot
    n_groups = len(ofinterest)
    allmeans = dict()
    for n in nums:
        means = []
        for o in ofinterest:
            if avevals[o][nums[n]] != 'n/a':
                means.append(data[i][o][nums[n]]*convert[i])
            else:
                means.append(0)
        allmeans[nums[n]] = means    

# create plot

    fig, ax = plt.subplots(figsize=(20,6))

    index = np.arange(n_groups)
    bar_width = 0.18
    opacity = 1
    colors = ('b','r','c','g','m')
    for  j, n in enumerate(nums):  
        rects = ax.bar(index+bar_width*j, allmeans[nums[n]], 
                       bar_width, alpha=opacity,
                       color=colors[j], label=nums[n])

    ax.set_xlabel('Energy Component', fontsize=20)
    ax.set_ylabel(('%s Deviation \n (%s)' % (t, units[i])), fontsize=20)
    ax.set_title(('%s Deviation in Energy Components for Each Program' % (t)), fontsize=24)
    ax.set_xticks(index + bar_width + 0.2)
    ax.set_xticklabels(ofinterest, fontsize=16)
    ax.legend(loc = 'upper left')

    #now we need to plot text 'N/A' on the chart
    nn = 0
    ylim = ax.get_ylim()
    for n in nums:
        no = 0
        for o in ofinterest:
            if avevals[o][nums[n]] == 'n/a':
                plt.text(no+nn*(bar_width)+0.05, (ylim[1]-ylim[0])/25.0, 'N/A', rotation=90)
            no+=1
        nn+=1  
    figname = t.replace(" ","") + figsuff + '.pdf'
    plt.savefig('../../figures/' + figname)

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
                print "%20.8f" % (data[i][o][nums[n]]*convert[i]),
            else:
                print '%20s' % ('n/a'),
        print ''
