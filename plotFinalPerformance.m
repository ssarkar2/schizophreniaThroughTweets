function plotFinalPerformance()
close all;
data = [
    0.8064, 0.7950, 0.7811, 0.8063, 0.7829, 0.7761;  %all data
    0.7924, 0.7885, 0.7626, 0.7936, 0.7902, 0.7656;  %only ngrams
    0.7494, 0.7295, 0.7936, 0.7498, 0.7359, 0.7925;  %only liwc
    0.7123, 0.7257, 0.7263, 0.7654, 0.7581, 0.7305;  %only sch related words freq
    0.6710, 0.6832, 0.6446, 0.6852, 0.6923, 0.6432;  %only tree
    0.6598, 0.6734, 0.6104, 0.6987, 0.7039, 0.6061;  %only rhyme
    0.6175, 0.6003, 0.5709, 0.6261, 0.5932, 0.5696;  %only connotation and afinn
    0.5815, 0.6355, 0.6023, 0.6651, 0.6340, 0.5904;  %only nontext
 ];

figure
p1 = bar(data);
specs = {'all', 'ngrams', 'liwc', 'sch-related', 'tree', 'rhyme', 'sentiment', 'non-text'};
set(gca,'XTick',1:8, 'XTickLabel',specs)


data = [
    0.8064, 0.7950, 0.7811, 0.8063, 0.7829, 0.7761;  %all data
    0,0,0,0,0,0;
    0.7924, 0.7885, 0.7626, 0.7936, 0.7902, 0.7656;  %only ngrams
    0,0,0,0,0,0;
    0.7494, 0.7295, 0.7936, 0.7498, 0.7359, 0.7925;  %only liwc
    0,0,0,0,0,0;
    0.7123, 0.7257, 0.7263, 0.7654, 0.7581, 0.7305;  %only sch related words freq
    0,0,0,0,0,0;
    0.6710, 0.6832, 0.6446, 0.6852, 0.6923, 0.6432;  %only tree
    0,0,0,0,0,0;
    0.6598, 0.6734, 0.6104, 0.6987, 0.7039, 0.6061;  %only rhyme
    0,0,0,0,0,0;
    0.5815, 0.6355, 0.6023, 0.6651, 0.6340, 0.5904;  %only nontext
    0,0,0,0,0,0;
    0.6175, 0.6003, 0.5709, 0.6261, 0.5932, 0.5696;  %only connotation and afinn
 ];

figure
p1 = barh(data);
specs = {'all', '', 'ngrams', '', 'liwc', '', 'sch-related', '', 'tree', '', 'rhyme', '', 'sentiment', '', 'non-text'};
set(gca,'YTick',1:15, 'YTickLabel',specs);
lg = legend({'SVM-acc','MLP-acc','AB-acc','SVM-F1','MLP-F1','AB-F1'}, 'Position',[0.7,0.72,0.25,0.1]);
set(lg,'fontsize',8)
legend('boxoff');
grid on;
xlabel('Accuracy and F1'); ylabel('Feature types');

%figure
%bar3(data)
end