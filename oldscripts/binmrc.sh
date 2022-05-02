#!/bin/bash



for d in *.mrc ; do
	pwd=$(pwd)
	INPUT="$pwd""/""$d"
	SAMPLE="$pwd""/""$d""/"
	python ~/Tomograms/Segmentation/oldscripts/binmrc.py $INPUT 20
done
