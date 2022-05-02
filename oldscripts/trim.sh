#!/bin/bash
#SBATCH --mem=16G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL
python3 ./Trimvol.py '/speed/jargroup/PNNL/workingstacks/Cry11b-08-27-21_10min_PhasePlate/01/Cry11b_10min_01_full_rec.mrc' '/speed/jargroup/PNNL/workingstacks/Cry11b-08-27-21_10min_PhasePlate/01/Cry11b_10min_01.mrc' 2778 5718 5148 7920
