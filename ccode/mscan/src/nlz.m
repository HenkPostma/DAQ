clear all; 
m=dlmread('/tmp/data.dat', ' ');
figure
subplot(3,1,1)
plot(m(:,1)/1e9, m(:,2))
axis('tight')
subplot(3,1, 2)
plot(m(:,1)/1e9, m(:,3))
axis('tight')
subplot(3, 1, 3)
plot(m(:,1)/1e9, m(:,4))
axis('tight')

