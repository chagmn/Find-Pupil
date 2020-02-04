load 'LLCA_left_3.txt'
X = LLCA_left_3(:,2);
Y = LLCA_left_3(:,3);
figure('Name','BPPV','NumberTitle','off');


%그래프 스무딩 작업
%coordinate_X = smoothdata(X);
%coordinate_Y = smoothdata(Y);


%피크값 찾기
hold on
% X좌표
subplot(2,1,1);
plot(X);
ylabel('coordinate');
title('Horizontal(X)');
grid on

% Y좌표
subplot(2,1,2);
plot(Y);
ylabel('coordinate');
title('Vertical(Y)');
grid on
