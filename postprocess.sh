#!/bin/bash
#SBATCH --mem=100G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL

SAMPLE="/speed/jargroup/Tomos/08-29-21_Cry11b_WT_UnprocessedData/Cry11b_WT_05/"
FILE="Cry11b_WT_05_full_rec.mrc"
INPUT="$SAMPLE""$FILE"

echo "Starting averaging for $d"
pwd=$(pwd)
python /home/shervinnia/Tomograms/TomoTrim/AvgSlices.py $INPUT

"AvgSlice png created! Opening selection box..."


echo "Starting selection box for $d"
pwd=$(pwd)
python /home/shervinnia/Tomograms/TomoTrim/SelectVol.py $INPUT $SAMPLE


echo "Starting trimming for $d"
pwd=$(pwd)
python /home/shervinnia/Tomograms/TomoTrim/TrimSel.py $INPUT $SAMPLE
