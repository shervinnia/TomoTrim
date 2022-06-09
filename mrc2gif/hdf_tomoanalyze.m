function [zproj]=hdf_tomoanalyze(filelist,dsname)
% USAGE: [zproj]=hdf_tomoanalyze('tomofiles.txt');
% where 'tomofiles.txt' is a text file containing paths to .hdf files.
% dsname is an important variable - set to '/MDF/images/0/image' and
% depends on the conents of the hdf file (how it was created).

[filenames]=textread(filelist,'%s');
nimages=size(filenames,1);
warning('off','all');
zslab=50;
rebin=4;

if exist('dsname','var')==0
    dsname='/MDF/images/0/image';
end

for kk=1:nimages
    
    filename=char(filenames(kk));
    nametemp=textscan(filename,'%s','delimiter','.');
    nameonly=nametemp{1}{1};
    
    tomoin = single(h5read(filename,dsname));
    tomoin = abs(tomoin-max(max(max(tomoin))));
    tomoin= tomoin-0.5*mean(mean(tomoin,1),2); tomoin(tomoin<0)=0;
    tomoin = 256*tomoin/max(max(max(tomoin)));
    tomolin2 = squeeze(mean(mean(tomoin,1),2));
    
    idx=find(tomolin2==max(tomolin2)); idx=ceil(mean(idx)); %idx=125;
    tomoslab=tomoin(:,:,max(1,idx-zslab):min(size(tomoin,3),idx+zslab));
    zproj=squeeze(mean(tomoslab,3));
    tomoslab=imresize(tomoslab,(1/rebin));
    
    imwrite(uint8(tomoslab(:,:,1)),strcat(nameonly,'rebin',num2str(rebin),'.gif'),'gif','Loopcount',inf,'DelayTime',0);
    for jj=1:2*zslab+1
        imwrite(uint8(tomoslab(:,:,jj)),strcat(nameonly,'rebin',num2str(rebin),'.gif'),'gif','WriteMode','append','Loopcount',inf,'DelayTime',0);
    end
    
    imwrite(uint8(zproj),strcat(nameonly,'rebin',num2str(rebin),'_zproj.png'),'png');
    imwrite(uint8(tomoin(:,:,idx)),strcat(nameonly,'rebin',num2str(rebin),'_slice.png'),'png');
    
    figure(1), 
    subplot(1,2,1), imagesc(zproj), axis image, colormap bone, title(strcat(nameonly,' *Projection*'));
    subplot(1,2,2), imagesc(tomoin(:,:,idx)), axis image, colormap bone, title(strcat(nameonly,' *Slice*'));
    pause();
end
