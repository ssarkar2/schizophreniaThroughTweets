function emoticonAnalyse()
close all;
c = xlsread('emoticonFeaturesCtrl.csv');
s  = xlsread('emoticonFeaturesSch.csv');
plot(s(:,1), s(:,2), 'ro'); hold on
plot(c(:,1), c(:,2), 'bo'); hold on; grid on

%blue is the 1st column, red is the second
figure;
hist([s(:,1), c(:,1)], 20); grid on %we see more 'mean rhyming' for the blue
title('Histogram of mean emoticon scores')
xlabel('mean emoticon score')
ylabel('number of occurances')
[a,b] = ttest2(s(:,1), c(:,1))  %p val = 0.8271

figure;
hist([s(:,2), c(:,2)], 20); grid on
title('Histogram of variance of emoticon scores')
xlabel('emoticon score variance')
ylabel('number of occurances')
[a,b] = ttest2(s(:,2), c(:,2))  %p val = 0.6045

figure;
hist([s(:,3), c(:,3)], 20); grid on
title('Histogram of number of emoticons')
xlabel('number of emoticons')
ylabel('number of occurances')
[a,b] = ttest2(s(:,3), c(:,3))  %p val = 0.1568



mean(s(:,1))
mean(c(:,1))
mean(s(:,2))
mean(c(:,2))
mean(s(:,3))
mean(c(:,3))
end
