fileID = fopen('./ppRules/ruleSize.txt','r');
formatSpec = '%d';
A = fscanf(fileID,formatSpec);
x = 1:length(A);
plot(x,A);
title('Size of association rules set over time');
xlabel('time');
ylabel('Size');
