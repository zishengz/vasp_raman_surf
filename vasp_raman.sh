#!/bin/sh -f
#$ -l h_data=3G,h_rt=23:59:59
#$ -cwd
#$ -o LOG.$JOB_ID
#$ -j y
#$ -pe dc* 16
##$ -pe shared 16

source /u/home/z/zisheng/.bashrc

source /u/local/Modules/default/init/modules.sh
module purge
module load IDRE intel/17.0.7
export VASPHOME=/u/project/ana/shared/vasp/vasp.5.4.4-tpc/bin

PROJ=`pwd |rev|awk -F "/" '{print $1}'|rev`
CURDIR=`pwd`

echo Started on `date`
echo " > PROJECT name:" $PROJ
echo " > CURRENT dir :" $CURDIR
echo " > SCRATCH dir :" $SCRATCH
echo ''

#time mpirun -n $NSLOTS $VASPHOME/vasp_std > out

export VASP_RAMAN_RUN="mpirun -n $NSLOTS $VASPHOME/vasp_std &> job.out"

python -u vasp_raman_surf.py 15,16,17,18,22,23,24 0.01

echo Finished on `date`


