Raw data file outputs of ./convert.py:
    gromacs_single_results.txt: GROMACS 5.0.4 with single precision
    gromacs_double_results.txt: GROMACS 5.0.4 with double precision

Parsing files:
    processfile.py: initial parsing file of raw output
    processtwo.py: do calculations using the output of the previous file

Commands run:
    python processfile.py gromacs_single_results.txt > processed_single.txt
    python processfile.py gromacs_double_results.txt > processed_double.txt
    paste processed_double.txt processed_single > singleanddouble.txt
    python processtwo.py singleanddouble.txt
