fileID = fopen('./ProgOutput/pruneDuration-Measure.txt','r');
formatSpec = '%d';
datacell = textscan(fileID, '%d%f%f', 'Delimiter',',');
plot(datacell{1},datacell{2})
title('Size of association rules set over time');
xlabel('week');
ylabel('Size');

