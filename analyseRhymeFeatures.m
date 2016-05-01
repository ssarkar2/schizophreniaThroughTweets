close all;
c = xlsread('RhymeFeaturesCtrl.csv');
s  = xlsread('RhymeFeaturesSch.csv');
plot(s(:,1), s(:,2), 'ro'); hold on
plot(c(:,1), c(:,2), 'bo'); hold on; grid on

%blue is the 1st column, red is the second
figure;
hist([s(:,1), c(:,1)], 20); grid on %we see more 'mean rhyming' for the blue
title('Histogram of mean rhyme scores')
xlabel('mean rhyme score')
ylabel('number of occurances')
[a,b] = ttest2(s(:,1), c(:,1))

figure;
hist([s(:,2), c(:,2)], 20); grid on
title('Histogram of variance of rhyme scores')
xlabel('rhyme score variance')
ylabel('number of occurances')
[a,b] = ttest2(s(:,2), c(:,2))

figure;
hist([s(:,3), c(:,3)], 20); grid on
title('Histogram of percentage of zero scores')
xlabel('percentage of zero score')
ylabel('number of occurances')
[a,b] = ttest2(s(:,3), c(:,3))

figure;
hist([s(:,4), c(:,4)], 20); grid on
title('Histogram of percentage of non-zero scores')
xlabel('percentage of non-zero score')
ylabel('number of occurances')
[a,b] = ttest2(s(:,4), c(:,4))
