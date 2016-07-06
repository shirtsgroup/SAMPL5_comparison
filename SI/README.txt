README.txt - This file.

configuration files (CBC.tgz, OAH.tgz, OAMe.tgz) converted input
simulation files in AMBER, CHARMM, DESMOND, GROMACS, and LAMMPS
formats for the 22 host-guest systems.  20 configurations used in the
paper for the comparison of average simulation energies are only
included with the original AMBER files for storage space reasons (1.3
GB total).
               
CBC/(.tarred and gzipped as CBC.tgz)
	CBC-G*/ 
		amber/
			CBC-G*.prmtop
			CBC-G*.rst7
		charmm/
			CBC-G*_converted.crd
			CBC-G*_converted.inp
			CBC-G*_converted.prm
			CBC-G*_converted.psf
			CBC-G*_converted.rtf
		desmond/
			CBC-G*-converted.cms
		gromacs/
			CBC-G*-converted.gro
			CBC-G*-converted.top
		lammps/
			CBC-G*-converted.lmp
			CBC-G*-converted.input

OAH/ (.tarred and gzipped as OAH.tgz)
	OAH-G*/ 
		amber/
			OAH-G*.prmtop
			OAH-G*.rst7
			altconfs/
				OAH-G*_%.prmtop: where % runs from 0-19
				OAH-G*_*.rst7: where % runs from 0-19
		charmm/
			OAH-G*_converted.crd
			OAH-G*_converted.inp
			OAH-G*_converted.prm
			OAH-G*_converted.psf
			OAH-G*_converted.rtf
		desmond/
			OAH-G*-converted.cms
		gromacs/
			OAH-G*-converted.gro
			OAH-G*-converted.top
		lammps/
			OAH-G*-converted.lmp
			OAH -G*-converted.input

OAMe/ (.tarred and gzipped as OAMe.tgz)
	OAMe-G*/ 
		amber/
			OAMe-G*.prmtop
			OAMe-G*.rst7
				OAMe-G*_%.prmtop: where % runs from 0-19
				OAMe-G*_*.rst7: where % runs from 0-19
		charmm/
			OAMe-G*_converted.crd
			OAMe-G*_converted.inp
			OAMe-G*_converted.prm
			OAMe-G*_converted.psf
			OAMe-G*_converted.rtf
		desmond/
			OAMe-G*-converted.cms
		gromacs/
			OAMe-G*-converted.gro
			OAMe-G*-converted.top
		lammps/
			OAMe-G*-converted.lmp
			OAMe-G*-converted.input

runfiles/  (as runfiles.tgz) Simulation command files to run the files above.
	ideal/
		min_ideal.in: AMBER simulation run file	
		grompp_ideal.mdp: GROMACS simulation run file
		onepoint_ideal.cfg: DESMOND simulation run file
		charmm and lammps simulation commands are in *.inp and *.input respectively.
	default/
		min_default.in: AMBER simulation run file	
		grompp_default.mdp: GROMACS simulation run file
		onepoint_default.cfg: DESMOND simulation run file
		charmm and lammps simulation commands are the same as the *.inp and *.input files, with the 
		following changes:
		charmm: nbond inbfrq -1 imgfrq -1 
			elec ewald pmew fftx 48 ffty 48 fftz 48 kappa 0.34 order 4 
			vdw vips cutnb 12. cutim  12. ctofnb 10. ctonnb 9.
		lammps: pair_style lj/cut/coul/long 9.0 9.0\npair_modify tail yes\nkspace_style pppm 1.0e-5 

analysis/ (as analysis.tgz)
	main_results/
	    * full_results_ideal_settings.txt: main results with energies of 22 host-guest 
	      complexes with simulation parameters at 'ideal' settings (as described in text)
	    * full_results_default_settings.txt: main results with energies of 22 host-guest 
	      complexes with simulation parameters at 'ideal' settings (as described in text)
	vary_coulomb_constant/
	    * originalcoul.txt: energies of 22 host-guest complexes compared between AMBER 
	      and GROMACS compiled with GROMACS 5.0.4's original Coulomb's constant
	    * NISTcoul.txt: energies of 22 host-guest complexes compared between AMBER 
	      and GROMACS compiled with the NIST CODATA 2014 Coulomb's constant
    	    * ambercoul.txt: energies of 22 host-guest complexes compared between AMBER 
	      and GROMACS compiled with the AMBER tleap's Coulomb's constant
	multiple_configurations/
	    * average_configurations_analysis.txt: energies of 12 host-guest complexes
	      averaged over 20 configurations (generated as described in the text)
            * single_configurations_analysis.txt: energies of 12 host-guest complexes 
	      with individual energies of 20 configurations (generated as described in the text)
	vary_configuration_precision/
	    * precision4.txt: energies of all host-guest complexes
	      with GROMACS input .gro files truncated to 4 digits after the decimal point 
	    * precision5.txt: energies of all host-guest complexes
	      with GROMACS input .gro files truncated to 5 digits after the decimal point 
	    * precision6.txt: energies of all host-guest complexes 
	      with GROMACS input .gro files truncated to 6 digits after the decimal point 
    	    * precision7.txt: energies of all host-guest complexes 
	      with GROMACS input .gro files truncated to 7 digits after the decimal point 
    	    * precision8.txt: energies of all host-guest complexes 
	      with GROMACS input .gro files truncated to 8 digits after the decimal point 
	double_versus_single_precision/
	    * gromacs_double_results.txt: energies of all host-guest complexes 
	      with GROMACS compiled in double precision
    	    * gromacs_single_results.txt: energies of all host-guest complexes
	      with GROMACS compiled in single precision
