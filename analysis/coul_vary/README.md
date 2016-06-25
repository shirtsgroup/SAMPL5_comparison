Raw data file outputs of ./convert.py:
    energy_originalcoul.txt: GROMACS 5.0.4 with original Coulomb's constant
    energy_bestcoul.txt: GROMACS 5.0.4 with NIST 2014 Coulomb's constant
    energy_badcoul.txt: GROMACS 5.0.4 with AMBER's Coulomb constant

Parsing files:
    processfile.py: initial parsing file of raw output
    processthree.py: do calculations using the output of the previous file

Commands run:
    python processfile.py energy_originalcoul.txt > originalcoul.txt
    python processfile.py energy_bestcoul.txt > bestcoul.txt
    python processfile.py energy_badcoul.txt > badcoul.txt
    paste badcoul.txt bestcoul.txt originalcoul.txt > threecoul.txt
    python processthree.py threecoul.txt
