#!/bin/bash
#SBATCH --mem=16G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL

for d in * ; do
	pwd=$(pwd)
	INPUT="$pwd""/""$d""/""$d""_rec.mrc"
	SAMPLE="$pwd""/""$d""/"
	python3 ~/Tomograms/Segmentation/oldscripts/mrcstack2slices.py $INPUT
done
