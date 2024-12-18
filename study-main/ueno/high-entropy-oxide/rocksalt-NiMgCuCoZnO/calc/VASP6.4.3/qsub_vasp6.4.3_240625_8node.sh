#!/bin/bash
#PBS -T necmpi
#PBS -q sxs
#PBS --venode 8
#PBS -l elapstim_req=24:00:00
#PBS -jo N vasp6.4.3

LANG=C
source /opt/nec/ve3/nlc/3.0.0/bin/nlcvars.sh

cd $PBS_O_WORKDIR

export PATH=/uhome/a01576/syc/vasp_6.4.3_nec_240625/bin:$PATH
export LD_LIBRARY_PATH=/uhome/a01576/syc/vasp_6.4.3_nec_240625/lib:$LD_LIBRARY_PATH

#export VE_LIMIT_OPT="-s 1048576"
export VE_FORT_SETBUF87=0


mpirun -np 128 /uhome/a01576/syc/vasp_6.4.3_nec_240625/bin/vasp_std > log

