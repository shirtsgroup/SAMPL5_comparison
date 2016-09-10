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
file = open(filename,'r')

lines = file.readlines()
nummol = 0
numconfs = 20 # hard coded

outlines = dict()
avevals = dict()
aveavals = dict()
avevals2 = dict()
averavals = dict()
avermsd = dict()
avermsv = dict()

data = [avevals, aveavals, avevals2, averavals, avermsd, avermsv]
units = ['kJ/mol', 'kJ/mol', 'kJ/mol','fraction', 'kJ/mol', 'kJ/mol']
convert = [4.184, 4.184, 4.184, 1, 4.184, 4.184]
#convert = [1, 1, 1, 1, 1, 1]
types = ['Average', 'Average Absolute', 'Average RMSD','Average Relative Absolute','AverageRMSDifference','AverageRMSValue']

# make a dict for each program
for d in data:
    for o in ofinterest:
        d[o] = dict()
        for n in nums:
            d[o][nums[n]] = 0

oldbasename = 'dummy'
thisconf = 0

nskip = 10
for i in range(len(lines)):
    line = lines[i]

    if line[0:4] == 'INFO':
        continue
    if line[0:7] == 'gromacs':
        vals = line.split('/')
        name = vals[7]  # use the directory name to get the value
        [basename, thisconf] = vals[7].split('_') # don't use the configuration
        thisconf = int(thisconf)
        if basename != oldbasename:
            oldbasename = basename
            avepmol = np.array(numconfs) # create new array for the
                                         # average of the configuration
                                         # from the same molecule.
            dictvals_perconf = list()
            dictdiff_perconf = list()

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
        dictdiff_perconf.append(dictdiff.copy())
        dictvals_perconf.append(dictvals.copy())

        dictrmsdiff = dict()
        dictrmsvals = dict()
        if numconfs-1 == thisconf:
            for o in ofinterest:
                dictrmsdiff[o] = dict()
                dictrmsvals[o] = dict()
                dictdiffo = dict()
                dictvalso = dict()
                eave = 0 
                for n in nums:
                    if dictvals[o][nums[n]] != 'n/a':  # should still give the right answer
                        sumd = 0
                        sumv = 0
                        sumd2 = 0
                        sumv2 = 0
                        for j in range(numconfs):
                            sumd += dictdiff_perconf[j][o][nums[n]]
                            sumv += dictvals_perconf[j][o][nums[n]]
                            sumd2 += dictdiff_perconf[j][o][nums[n]]**2
                            sumv2 += dictvals_perconf[j][o][nums[n]]**2
                        dictdiffo[nums[n]] = sumd/numconfs
                        dictvalso[nums[n]] = sumv/numconfs
                        eave += dictvalso[nums[n]]
                        nprog += 1

                        # this is the RMSD of the difference from the average and the value 
                        # calculated over all configurations.
                        dictrmsdiff[o][nums[n]] = np.sqrt(sumd2/numconfs - dictdiffo[nums[n]]**2)
                        dictrmsvals[o][nums[n]] = np.sqrt(sumv2/numconfs - dictvalso[nums[n]]**2)
                    else: 
                        dictrmsvals[o][nums[n]] = 'n/a'
                        dictrmsdiff[o][nums[n]] = 'n/a'
                eave /= nprog

                for j in range(numconfs):
                    for n in nums:
                        v = dictdiff_perconf[j][o][nums[n]]
                        if v != 'n/a':
                            avevals[o][nums[n]] += v
                            aveavals[o][nums[n]] += abs(v)
                            avevals2[o][nums[n]] += v*v
                            averavals[o][nums[n]] += abs(v)/abs(eave)
                for n in nums:
                    if dictrmsdiff[o][nums[n]] != 'n/a':  # order doesn't matter, will work regardless
                        avermsd[o][nums[n]] += dictrmsdiff[o][nums[n]]
                        avermsv[o][nums[n]] += dictrmsvals[o][nums[n]]
                    else:
                        for d in data:
                            d[o][nums[n]] = 'n/a'

            olines = list()
            olines.append("\n****************")
            olines.append(basename)
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

'''
We have multiple configurations for each molecule.  What is the
hypothesis we are testing? We want to know different the molecules are
when averaged over configurations.
''' 

for o in ofinterest:
    for n in nums:
        if data[0][o][nums[n]] != 'n/a':  # only need to check the first one
            for d in data:
                d[o][nums[n]] /= nummol
            avevals[o][nums[n]] /= numconfs # these need to get divided by the total molecules
            aveavals[o][nums[n]] /= numconfs
            avevals2[o][nums[n]] /= numconfs
            averavals[o][nums[n]] /= numconfs

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
        

# what fraction of variance is because of molecular variability, and which of configurational variability

print "\nFraction of variance from conformational variability"
for n in nums:
    print "%20s" % (nums[n]),
print '\n'
difference = dict()
for o in ofinterest:
    print "%20s" % (o),
    do = dict()
    for n in nums:
        if avevals[o][nums[n]] != 'n/a':
            totalv = avevals2[o][nums[n]]**2
            # totalv is the variation from the program average over
            # all configurations.  avermsd, we average out the
            # variation from molecule to molecule.  if avermsd is
            # large, the difference is mainly between molecules, and
            # conformational variation is small.
            # 
            do[nums[n]] = (totalv - avermsd[o][nums[n]]**2)/totalv
            print "%20.8f" % (do[nums[n]]),
        else:
            do[nums[n]] = 'n/a'
            print '%20s' % ('n/a'),
    print ''    
    difference[o] = do

# data to plot
n_groups = len(ofinterest)
allmeans = dict()
for n in nums:
    means = []
    for o in ofinterest:
        if avevals[o][nums[n]] != 'n/a':
            means.append(difference[o][nums[n]])
        else:
            means.append(0)
        allmeans[nums[n]] = means
# create plot

for o in ofinterest:
    fig, ax = plt.subplots(figsize=(17,5))

    index = np.arange(n_groups)
    bar_width = 0.18
    opacity = 1
    colors = ('b','r','c','g','m')
    for  j ,n in enumerate(nums):  
        rects = ax.bar(index+bar_width*j, allmeans[nums[n]], 
                       bar_width, alpha=opacity,
                       color=colors[j], label=nums[n])

    ax.set_xlabel('Energy Component', fontsize=20)
    ax.set_ylabel('Fraction of Conformational Variance', fontsize=18)
    ax.set_title('Fraction of Conformational Variance Between Programs in Energy Output', fontsize=24)
    ax.set_xticks(index + bar_width + 0.2)
    ax.set_xticklabels(ofinterest, fontsize=14)
    ax.legend(loc = 'upper left')

    #now we need to plot text 'N/A' on the chart
    nn = 0
    ylim = ax.get_ylim()
    for n in nums:
        no = 0
        for o in ofinterest:
            if difference[o][nums[n]] == 'n/a':
                plt.text(no+nn*(bar_width)+0.05, (ylim[1]-ylim[0])/25.0, 'N/A', rotation=90)
            no+=1
        nn+=1  
    figname = '../../figures/fractionofvariation.pdf'
    plt.tight_layout()
    plt.savefig(figname)

