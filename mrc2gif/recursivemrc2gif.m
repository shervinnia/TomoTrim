for i = 1:8
     base = "Cry11b_1min_0";
%     origfolder = strcat(base,int2str(i));
%     origfile = strcat(base,int2str(i),"_full.rec");
%     origpath = strcat(origfolder,"/",origfile);
%     destpath = strcat("mrcfiles/",base,int2str(i),".mrc");
%     
%     origpath = convertStringsToChars(origpath);
%     destpath = convertStringsToChars(destpath);
%     
%     copyfile origpath destpath;
    mrc2gif(strcat(base,int2str(i),".mrc"),30,0.08)
end