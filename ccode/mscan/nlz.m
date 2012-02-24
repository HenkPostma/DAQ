clear all; 

files = dir('*dat');

figure(1);
for i=1:size(files),
    fn = files(i).name
    indices = regexp(fn, '-');
    dot = regexp(fn, '\.');
    nchan(i) = str2num(substr(fn, indices(1)+1, indices(2)-1-indices(1)));
    points(i) = str2num(substr(fn, indices(2)+1, indices(3)-1-indices(2)));
    period(i) = str2num(substr(fn, indices(3)+1, dot-1-indices(3)));
    m = dlmread(files(i).name, ' ');

    subplot(4, 3, i);
    plot(m(:,2));
    legend(fn);
    a(i) = mean(m(:,2));
    s(i) = sum(abs(m(:,2)-a(i)));
    rms(i) = std(m(:,2));
    
end;

s
a
rms
nchan
points
period

s./rms
