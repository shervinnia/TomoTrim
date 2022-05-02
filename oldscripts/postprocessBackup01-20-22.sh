#!/bin/bash
#SBATCH --mem=100G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL
read -p "Enter full path of input tomogram:" INPUT

read -p "Enter full path of output trimmed tomogram:" OUTPUT

python3 ./AvgSlices.py $INPUT

echo "AvgSlice png created! Opening selection box..."

python3 ./Trimvol.py $INPUT $OUTPUT
