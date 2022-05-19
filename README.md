# TomoTrim
### A compilation of various tomography post-processing Python scripts


Note: oldscripts folder is mostly comprised of single-operation scripts, along with some old versions of the primary scripts. There may be some useful stuff in there.


## Setup
Simply download this repository however you like and place the folder wherever you like in your computer. 

## Basic Use
The four core scripts to this toolkit are AvgSlices.py, SelectVol.py, TrimVol.py, and postprocess.sh. Their functions are as follows:

### AvgSlices.py
This script takes several slices of the selected tomogram and averages them together, then saves them as a PNG to the directory.

### SelectVol.py
Here we open up the PNG created with AvgSlices.py in a GUI and drag a box aroudn the ROI (region of interest). *Note:* the box must be dragged top-left to bottom-right. This affects how the coordinates are saved and must be followed in that order. If not, an error will throw later on when reading the coordinates file.

### TrimVol.py
This script reads the coordinates saved by SelectVol.py and creates the new trimmed tomogram slice-by-slice (memory-mapped objects must be processed in a for-loop, as they still do take up RAM when being processed).
