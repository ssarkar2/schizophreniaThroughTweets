function analyseMiscFeature()
%this seems to work in windows only (and not linux), because of 'xlsread'
close all;
analyseOneFeature('control_favorite_count.csv', 'sch_favorite_count.csv', 'resultsDump\sayantan\favcount\')
analyseOneFeature('control_retweet_count.csv', 'sch_retweet_count.csv', 'resultsDump\sayantan\retweetcount\')
%analyseOneFeature('control_retweeted.csv', 'sch_retweeted.csv')
%everything is 0 for this one, so useless

analyseOneFeature('RhymeFeaturesCtrl.csv', 'RhymeFeaturesSch.csv', '')
analyseOneFeature('emoticonFeaturesCtrl.csv', 'emoticonFeaturesSch.csv', '')
end

function analyseOneFeature(ctrlCSV, schCSV, saveLoc)
%enter 2 csv names (control and sch)
if strcmp(saveLoc, '') == 0
    mymkdir(saveLoc);
end
saveLoc
c = xlsread(ctrlCSV); s  = xlsread(schCSV);
numFeatures = size(c,2);
for ft = 1:numFeatures
    figure;
    %blue is the 1st column, red is the second
    hist([s(:,ft), c(:,ft)], 20); grid on
    if strcmp(saveLoc, '') == 0
        print('-dpng', [saveLoc 'f' num2str(ft) '.png'])
    end
    [a,b] = ttest2(s(:,ft), c(:,ft))
end
end


function mymkdir(loc)
if ~exist(loc, 'dir')
    mkdir(loc);
end
end
