% README
% 
% mrc2gif
%
%
% Corresponding author: 
%
% Shervin S. Nia, B.S.
% UCLA Department of Chemistry and Biochemistry, 
% Rodriguez Lab, Boyer Hall, 
% 601 Charles E. Young Dr, 
% Los Angeles, CA 90095
% linkedin.com/in/shervinnia
% github.com/shervinnia
% niashervin@gmail.com
%
%
% This function takes an MRC stack and converts it to a GIF.
%
% Necessary functions to have in the same directory are ReadMRC.m and gif.m
% 
% Inputs are as follows:
% 
% mrc2gif(inputfile,fps,compressionfactor)
% 
% 
% The inputs are:
% 
%   inputfile: The name of the mrc file you are converting to a gif.
%       Please note this file must be in a current path of Matlab, and 
%       the output file will be in the same directory, with the same 
%       name (but with .gif instead of .mrc).
% 
%   fps: The frames-per-second of the resulting gif.
% 
%   (optional) compressionfactor: The ratio of the size of the output
%       file to the size of the original gif made. This process is done
%       using the imresize command if you want to look into the 
%       compression process further. This number may require some tuning 
%       depending on your specific need. Leave this parameter out if you
%       want to keep the original gif size. Please note this is NOT the
%       ratio of the input file, but rather the gif made with no 
%       compression, which already has great file size reduction.


function[] = mrc2gif(inputfile,fps,compressionfactor)
clear vars;

if nargin < 3
    compressionfactor = 1;
end

map = ReadMRC(inputfile);
filename = erase(inputfile,'.mrc');
file = strcat(filename,'.gif');


%IF YOU NEED TO ROTATE YOUR MATRIX, USE THE TWO BELOW LINES AND COMMENT OUT
%THE THIRD LINE
%maprotated = permute(map,[1 3 2]);
%map = flipud(maprotated);
map = maprotated;


sizex = size(map,1);
sizey = size(map,2);
sizez = size(map,3);

for i = 1:sizez
    framevar = map(1:sizex,1:sizey,i);
    framefixed = (framevar + 1)*128;
    framecontrast = (framefixed/4) + 190;
    image(imresize(framecontrast,compressionfactor));
    colormap(gray);
    ax = gca; ax.Position = [0 0 1 1];
    truesize();
    xticks([]);
    yticks([]);    
    if i == 1
        gif(convertStringsToChars(file),'DelayTime',1/fps)
    else
        gif
    end
end

uialert(uifigure,"GIF (hard G) created successfully!","Done",'Icon','success')
end
