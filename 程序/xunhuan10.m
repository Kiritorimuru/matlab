for i=1:10

[d_rss_mean,v_rightroom] = fun_main_knn_morerss(); 
d_rss_meanxunhuan(:,i)=d_rss_mean;


v_rightroom_xunhuan(:,i)=v_rightroom;


end
xunhuan=1:1:10;


%画图

%循环十次，即生成十次指纹数据库和测试指纹，平均定位误差变换情况

%figure(1)
%plot(xunhuan(1:10),d_rss_meanxunhuan(1,:));
figure(2)
plot(xunhuan(1:10),d_rss_meanxunhuan(2,:),'b-');
title('循环次数和平均定位误差曲线');
xlabel('循环次数');
ylabel('定位误差/m');

%figure(3)
%plot(xunhuan(1:10),d_rss_meanxunhuan(3,:));
%figure(4)
%plot(xunhuan(1:10),v_rightroom_xunhuan(1,:));
%figure(5)
%plot(xunhuan(1:10),v_rightroom_xunhuan(2,:));
%figure(6)
%plot(xunhuan(1:10),v_rightroom_xunhuan(3,:));
