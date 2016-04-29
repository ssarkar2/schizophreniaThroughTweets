function untitled()
load('emoticonAnalyse.mat')
close all;
zs = double(zs); zc = double(zc);
s = [xs; ys;zs];
c = [xc; yc;zc];

% % % length(find(sum(abs(s)) == 0))  %488879
% % % length(find(sum(abs(c)) == 0))  %477206
% % % {size(s,2), size(c,2)}  %[529257]    [530154]
% % % s(:, find(sum(abs(s)) == 0)) = [] ;  %removing (0,0,0) points from data
% % % c(:, find(sum(abs(c)) == 0)) = [] ;
% % % {size(s,2), size(c,2)}  %[40378]    [52948]

xs = s(1,:); ys = s(2,:); zs = s(3,:);
xc = c(1,:); yc = c(2,:); zc = c(3,:);


% [h,p] = ttest2(xs,xc)
% [h,p] = ttest2(ys,yc)
% [h,p] = ttest2(zs,zc)
% 
% hist(xs, 100); waitforbuttonpress; hist(xc, 100); waitforbuttonpress;
% hist(ys, 100); waitforbuttonpress; hist(yc, 100); waitforbuttonpress;
% hist(zs, 100); waitforbuttonpress; hist(zc, 100); waitforbuttonpress;

mean(xs)
mean(xc)
mean(ys)
mean(yc)
mean(zs)
mean(zc)

plot(xs,ys, 'ro'); hold on; plot(xc,yc, 'b^');
figure; rotate3d on; scatter3(xs,ys,zs,'ro'); hold on; scatter3(xc,yc,zc,'b^');
pcaStuff(c,s)
end





function pcaStuff(c,s)
'pcastuff'
slen = size(s,2);
clen = size(c,2);
[coeff score latent] = pca([s';c']);
scoreS = score(1:slen,:);
scoreC = score(slen+1:end,:);

spca1 = scoreS(:,1); spca2 = scoreS(:,2); spca3 = scoreS(:,3);
cpca1 = scoreC(:,1); cpca2 = scoreC(:,2); cpca3 = scoreC(:,3);


figure;plot(spca1,spca2, 'ro'); hold on; plot(cpca1,cpca2, 'b^'); grid on;
nbins = [50,50];
figure; grid on; hist3([spca1 spca2], nbins);
figure; grid on; hist3([cpca1 cpca2], nbins);


figure; hist(spca1, 100, 'r'); figure; hist(cpca1, 100, 'b');



[h,p] = ttest2(spca1,cpca1)
[h,p] = ttest2(spca2,cpca2)
[h,p] = ttest2(spca3,cpca3)

end