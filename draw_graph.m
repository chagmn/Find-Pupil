load 'LLCA_left_3.txt'
X = LLCA_left_3(:,2);
Y = LLCA_left_3(:,3);
figure('Name','BPPV','NumberTitle','off');


%�׷��� ������ �۾�
%coordinate_X = smoothdata(X);
%coordinate_Y = smoothdata(Y);


%��ũ�� ã��
hold on
% X��ǥ
subplot(2,1,1);
plot(X);
ylabel('coordinate');
title('Horizontal(X)');
grid on

% Y��ǥ
subplot(2,1,2);
plot(Y);
ylabel('coordinate');
title('Vertical(Y)');
grid on
