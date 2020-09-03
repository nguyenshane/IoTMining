fileID1 = fopen('./ProgOutput/pruneDuration-Measure.txt','r');
fileID2 = fopen('./ProgOutput/pruneDurationUpgraded-Measure.txt','r');
fileID3 = fopen('./ProgOutput/pruneTimeThreshold-Measure.txt','r');

formatSpec = '%d';
datacell1 = textscan(fileID1, '%d%f%f', 'Delimiter',',');
datacell2 = textscan(fileID2, '%d%f%f', 'Delimiter',',');
datacell3 = textscan(fileID3, '%d%f%f', 'Delimiter',',');

plot(datacell1{1},datacell1{3})

hold on 

plot(datacell1{1},datacell2{3})

hold on 

plot(datacell1{1},datacell3{3})
title('Time comparisions between algorithms');
xlabel('Week');
ylabel('Time (in seconds)');
legend('pruneDuration','pruneDurationUpgraded','pruneTimeThreshold');
hold off 



