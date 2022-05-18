#!/bin/bash
#SBATCH --mem=100G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL

for d in * ; do
	echo "Starting averaging for $d"
	pwd=$(pwd)
	INPUT="$pwd""/""$d""/""$d""_full_rec.mrc"
	SAMPLE="$pwd""/""$d""/"
	#echo $INPUT
	#echo $SAMPLE
	python3 /home/shervin/PycharmProjects/cry11btomo/Segmentation/AvgSlices.py $INPUT
done
echo "AvgSlice png created! Opening selection box..."

for d in * ; do
        echo "Starting selection box for $d"
        pwd=$(pwd)
        INPUT="$pwd""/""$d""/""$d""_full_rec.mrc"
        SAMPLE="$pwd""/""$d""/"
        #echo $INPUT
        #echo $SAMPLE
        python3 /home/shervin/PycharmProjects/cry11btomo/Segmentation/SelectVol.py $INPUT $SAMPLE
done


for d in * ; do
        echo "Starting trimming for $d"
        pwd=$(pwd)
        INPUT="$pwd""/""$d""/""$d""_full_rec.mrc"
        SAMPLE="$pwd""/""$d""/"
        #echo $INPUT
        #echo $SAMPLE
        python3 /home/shervin/PycharmProjects/cry11btomo/Segmentation/TrimSel.py $INPUT $SAMPLE
done
