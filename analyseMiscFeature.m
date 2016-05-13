function analyseMiscFeature()
%this seems to work in windows only (and not linux), because of 'xlsread'
close all;
%analyseOneFeature('control_favorite_count.csv', 'sch_favorite_count.csv', 'resultsDump\sayantan\favcount\')
%analyseOneFeature('control_retweet_count.csv', 'sch_retweet_count.csv', 'resultsDump\sayantan\retweetcount\')
%%%analyseOneFeature('control_retweeted.csv', 'sch_retweeted.csv')
%%%everything is 0 for this one, so useless

%analyseOneFeature('resultsDump/allCSVs/RhymeFeaturesCtrl.csv', 'resultsDump/allCSVs/RhymeFeaturesSch.csv', '')
%analyseOneFeature('emoticonFeaturesCtrl.csv', 'emoticonFeaturesSch.csv', '')

%%%user features
% analyseOneFeature('control_user_favourites_count.csv', 'sch_user_favourites_count.csv', 'resultsDump\sayantan\user\favCount\')
% analyseOneFeature('control_user_followers_count.csv', 'sch_user_followers_count.csv', 'resultsDump\sayantan\user\followerCount\')
% analyseOneFeature('control_user_friends_count.csv', 'sch_user_friends_count.csv', 'resultsDump\sayantan\user\friendsCount\')
% analyseOneFeature('control_user_statuses_count.csv', 'sch_user_statuses_count.csv', 'resultsDump\sayantan\user\statusCount\')

%%%simple sentiment
%analyseOneFeature('control_simpleconnotation_features.csv', 'sch_simpleconnotation_features.csv', 'resultsDump\sayantan\simpleconnotation\')

%afinn
%analyseOneFeature('control_simplesentimentAFINN_features.csv', 'sch_simplesentimentAFINN_features.csv', 'resultsDump\sayantan\afinnsentiment\')

%frazier
%analyseOneFeature('resultsDump/allCSVs/FrazierControl.csv', 'resultsDump/allCSVs/FrazierSch.csv', 'resultsDump\arthita\frazier\')
%yngve
%analyseOneFeature('resultsDump/allCSVs/YngveControl.csv', 'resultsDump/allCSVs/YngveSch.csv', 'resultsDump\arthita\yngve\')

%sch specific words
%analyseOneFeature('resultsDump/allCSVs/control_schcount.csv', 'resultsDump/allCSVs/sch_schcount.csv', 'resultsDump\sayantan\schcount\')

%cpidr
%analyseOneFeature('resultsDump/allCSVs/CPIDRScoreControl.csv', 'resultsDump/allCSVs/CPIDRScoreSchiz.csv', 'resultsDump\arthita\cpidr\')

%neologism
analyseOneFeature('resultsDump/allCSVs/control_neologismcount.csv', 'resultsDump/allCSVs/sch_neologismcount.csv', 'resultsDump\sayantan\nelogism\')

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
    ss = s(:,ft)/sum(s(:,ft));
    cc = c(:,ft)/sum(c(:,ft));
    %hist([s(:,ft), c(:,ft)], 20); grid on
    hist([ss, cc], 20); grid on
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
