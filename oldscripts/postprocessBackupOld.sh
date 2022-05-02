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

echo "AvgSlice png created! Opening in Fiji..."

xterm -hold -e "./Fiji.app/ImageJ-linux64 $INPUT.png" &

read -p "Enter MINX:" MINX
read -p "Enter MAXX:" MAXX
read -p "Enter MINY:" MINY
read -p "Enter MAXY:" MAXY

python3 ./Trimvol.py $INPUT $OUTPUT $MINX $MAXX $MINY $MAXY
