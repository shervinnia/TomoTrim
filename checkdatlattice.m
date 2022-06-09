function[tomo2]=checkdatlattice(filepath)

%tomoin = tom_mrcread('/cold2/jargroup/FinishedTomos/08-29-21_Cry11b_WT_UnprocessedData/Cry11b_WT_05/Cry11b_WT_05_rec.mrc_iso10xbin.mrc');
splitpath=split(filepath,'.');
%noext = strcat(splitpath{1},'_',splitpath{2});
noext = splitpath{1};

binfactor=4;
tomoin = tom_mrcread(filepath);
tomogram = tomoin.Value(:,:,floor(1500/binfactor):floor(3000/binfactor));


tomoft = fftshift(fftn(tomogram));
tomoabft = abs(tomoft);
threshold = (14-binfactor)*mean(mean(mean(tomoabft)));

f1=figure(1); colormap jet;
subplot(3,3,1), imagesc(log(squeeze(mean(tomoabft,1)))), axis image;
subplot(3,3,2), imagesc(log(squeeze(mean(tomoabft,2)))), axis image;
subplot(3,3,3), imagesc(log(squeeze(mean(tomoabft,3)))), axis image;
subplot(3,3,4), imagesc(log(squeeze(max(tomoabft,[],1)))), axis image;
subplot(3,3,5), imagesc(log(squeeze(max(tomoabft,[],2)))), axis image;
subplot(3,3,6), imagesc(log(squeeze(max(tomoabft,[],3)))), axis image;
subplot(3,3,7), imagesc(log(squeeze(tomoabft(ceil(size(tomoabft,1)/2),:,:)))), axis image;
subplot(3,3,8), imagesc(log(squeeze(tomoabft(:,ceil(size(tomoabft,2)/2),:)))), axis image;
subplot(3,3,9), imagesc(log(squeeze(tomoabft(:,:,ceil(size(tomoabft,3)/2))))), axis image;

tomoAFc= tomoft;
tomoAF = abs(tomoAFc);
tomoAF(tomoabft<threshold)=0;
tomoAFc(tomoabft<threshold)=0;

f2=figure(2); colormap jet;
subplot(3,3,1), imagesc(log(squeeze(mean(tomoAF,1)))), axis image;
subplot(3,3,2), imagesc(log(squeeze(mean(tomoAF,2)))), axis image;
subplot(3,3,3), imagesc(log(squeeze(mean(tomoAF,3)))), axis image;
subplot(3,3,4), imagesc(log(squeeze(max(tomoAF,[],1)))), axis image;
subplot(3,3,5), imagesc(log(squeeze(max(tomoAF,[],2)))), axis image;
subplot(3,3,6), imagesc(log(squeeze(max(tomoAF,[],3)))), axis image;
subplot(3,3,7), imagesc(log(squeeze(tomoAF(ceil(size(tomoabft,1)/2),:,:)))), axis image;
subplot(3,3,8), imagesc(log(squeeze(tomoAF(:,ceil(size(tomoabft,2)/2),:)))), axis image;
subplot(3,3,9), imagesc(log(squeeze(tomoAF(:,:,ceil(size(tomoabft,3)/2))))), axis image;

tomo2 = ifftn(ifftshift(tomoAFc));

f3= figure(3); colormap bone;
subplot(2,3,1), imagesc(squeeze(mean(tomogram,1))), axis image;
subplot(2,3,2), imagesc(squeeze(mean(tomogram,2))), axis image;
subplot(2,3,3), imagesc(squeeze(mean(tomogram,3))), axis image;
subplot(2,3,4), imagesc(squeeze(mean(tomo2,1))), axis image;
subplot(2,3,5), imagesc(squeeze(mean(tomo2,2))), axis image;
subplot(2,3,6), imagesc(squeeze(mean(tomo2,3))), axis image;


for kk=1:size(tomo2,3)-5
    if mod(kk,ceil(size(tomo2,3)/(20*binfactor)))==0
        figure(4); colormap bone;
        subplot(1,2,1), imagesc(imgaussfilt(squeeze(mean(tomogram(:,:,kk:kk+5),3)),0.5)), axis image;
        title(strcat('original image: ',num2str(kk))), caxis([-binfactor binfactor]);
        subplot(1,2,2), imagesc(imgaussfilt(squeeze(mean(tomo2(:,:,kk:kk+5),3)),0.5)), axis image;
        title(strcat('filtered image: ',num2str(kk))), caxis([-binfactor binfactor]);
    end
    pause(0.05);
end

saveas(f1,strcat(noext,'_ogfft_projs.png'),'png');
saveas(f2,strcat(noext,'_filtfft_proj.png'),'png');
saveas(f3,strcat(noext,'_og_vs_Ffilter_proj.png'),'png');
