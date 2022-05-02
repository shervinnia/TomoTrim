#!/bin/bash
#SBATCH --mem=16G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL
python3 ~/Tomograms/Segmentation/Trimvol.py '/backup2/jargroup/batchtest/08-27_10min/Cry11b_10min_01/Cry11b_10min_01_full_recSIRT.mrc' '/backup2/jargroup/batchtest/08-27_10min/Cry11b_10min_01/Cry11b_10min_01_average.png'
