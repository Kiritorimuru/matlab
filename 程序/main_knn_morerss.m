%主程序 main
clear all;
clear all;
%离线指纹数据--------------------


disp('开始执行 RSSrssBUILD.m');
run('RSSrssBUILD.m'); % 执行 script1.m 脚本
disp('结束执行 RSSrssBUILD.m');

load("RSS.mat","RSS");
load("LOC.mat","LOC");
load("testrss.mat","testrss");
load("testloc.mat","testloc");
load("test_allFP_xy.mat","test_allFP_xy");


%%房间布局的范围，为了生成测试指纹，这里是为了判断测试指纹属于哪个房间
for i=1:13
fanwei_x0(i)=6+3.9*(12-i+1);
end
fanwei_y=[0,6,6+2.7,6+2.7+6];
fanwei_x=[fanwei_x0,0];
n_fanwei_x=size(fanwei_x,2);
n_fanwei_y=size(fanwei_y,2);
sort_fanwei_x_order=sort(fanwei_x);%升序
sort_fanwei_y=sort(fanwei_y);



RSS=RSS;
LOC=LOC;
FP1=[LOC RSS];

test_allFP=test_allFP_xy;

rss=testrss;
loc=testloc;
n_rss=size(rss,1);

s_num_test_FP_xy=1:2:26;
d_num_test_FP_xy=2:2:26;

for i=1:n_rss

rss=testrss(i,:);
loc=testloc(i,:);


%------单纯的KNN
[L2,p2]=knn1(rss,FP1,3);
%-----未加特征提取的WKNN
[L3,p3]=KNN(rss,FP1,3);
%-----pca特征提取后的定位---所有算法已经变完。且用到的是改进的KNN算法
[Y1,eigVector1,eigValue1]=PCA_sammid(RSS,4);
FP2=[LOC Y1];
rss1=PCA_sammid_online(rss,RSS,4); %rss为在线样本；
%------仅仅通过PCA后 PCA-wknn未经过定位改进的
[L4,p4]=KNN(rss1,FP2,7);

%--------误差估计----

d2=sqrt(distance(p2,loc));
d3=sqrt(distance(p3,loc));
d4=sqrt(distance(p4,loc));
D=[d2 d3 d4];

L2_rss{i}=L2;
p2_rss{i}=p2;

L3_rss{i}=L3;
p3_rss{i}=p3;

L4_rss{i}=L4;
p4_rss{i}=p4;

d2_rss(i)=d2;
d3_rss(i)=d3;
d4_rss(i)=d4;

%判断测试指纹得到的结果是在哪个房间
%判断p2_rss
p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_x +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素

for j=1:n_fanwei_x
% 在向量中搜索x应该插入的位置
    if sort_fanwei_x_order(1,j) > p2(1)
        p_test_idx_upper =j; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_x_order(1,j) <p2(1)
        p_test_idx_lower=j; % 更新下界索引
    end
end

p_test_x0=13-p_test_idx_lower+1;


p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_y +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
for k=1:n_fanwei_y
% 在向量中搜索x应该插入的位置
    if sort_fanwei_y(1,k) > p2(2)
        p_test_idx_upper =k; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_y(1,k) <p2(2)
        p_test_idx_lower=k; % 更新下界索引
    end
end
p_test_y0=p_test_idx_lower;


if p_test_y0==1
    p2_rss{i}(1,3)=200+d_num_test_FP_xy(p_test_x0);
elseif p_test_y0==2
    p2_rss{i}(1,3)=200;
   elseif p_test_y0==3
    p2_rss{i}(1,3)=200+s_num_test_FP_xy(p_test_x0); 
end

%判断p3_rss
p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_x +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素

for j=1:n_fanwei_x
% 在向量中搜索x应该插入的位置
    if sort_fanwei_x_order(1,j) > p3(1)
        p_test_idx_upper =j; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_x_order(1,j) <p3(1)
        p_test_idx_lower=j; % 更新下界索引
    end
end

p_test_x0=13-p_test_idx_lower+1;


p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_y +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
for k=1:n_fanwei_y
% 在向量中搜索x应该插入的位置
    if sort_fanwei_y(1,k) > p3(2)
        p_test_idx_upper =k; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_y(1,k) <p3(2)
        p_test_idx_lower=k; % 更新下界索引
    end
end
p_test_y0=p_test_idx_lower;


if p_test_y0==1
    p3_rss{i}(1,3)=200+d_num_test_FP_xy(p_test_x0);
elseif p_test_y0==2
    p3_rss{i}(1,3)=200;
   elseif p_test_y0==3
    p3_rss{i}(1,3)=200+s_num_test_FP_xy(p_test_x0); 
end

%判断p4_rss

p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_x +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素

for j=1:n_fanwei_x
% 在向量中搜索x应该插入的位置
    if sort_fanwei_x_order(1,j) > p4(1)
        p_test_idx_upper =j; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_x_order(1,j) <p4(1)
        p_test_idx_lower=j; % 更新下界索引
    end
end

p_test_x0=13-p_test_idx_lower+1;


p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_y +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
for k=1:n_fanwei_y
% 在向量中搜索x应该插入的位置
    if sort_fanwei_y(1,k) > p4(2)
        p_test_idx_upper =k; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_fanwei_y(1,k) <p4(2)
        p_test_idx_lower=k; % 更新下界索引
    end
end
p_test_y0=p_test_idx_lower;


if p_test_y0==1
    p4_rss{i}(1,3)=200+d_num_test_FP_xy(p_test_x0);
elseif p_test_y0==2
    p4_rss{i}(1,3)=200;
   elseif p_test_y0==3
    p4_rss{i}(1,3)=200+s_num_test_FP_xy(p_test_x0); 
end

end
n2_rightroom=0;
for i=1:n_rss
if p2_rss{i}(1,3)==test_allFP(i,3)
n2_rightroom=n2_rightroom+1;
end
end

v2_rightroom=n2_rightroom./n_rss;

n3_rightroom=0;
for i=1:n_rss
if p3_rss{i}(1,3)==test_allFP(i,3)
n3_rightroom=n3_rightroom+1;
end
end

v3_rightroom=n3_rightroom./n_rss;

n4_rightroom=0;
for i=1:n_rss
if p4_rss{i}(1,3)==test_allFP(i,3)
n4_rightroom=n4_rightroom+1;
end
end

v4_rightroom=n4_rightroom./n_rss;

d2_rss_mean=mean(d2);
d3_rss_mean=mean(d3);
d4_rss_mean=mean(d4);

%%绘制累积分布函数
% 对数据进行排序
sorted_d2_rss = sort(d2_rss);

% 计算每个值的累积概率
n_d2_rss = length(sorted_d2_rss);
cumulative_d2_rss = (1:n_d2_rss) / n_d2_rss;

% 对数据进行排序
sorted_d3_rss = sort(d3_rss);

% 计算每个值的累积概率
n_d3_rss = length(sorted_d3_rss);
cumulative_d3_rss = (1:n_d3_rss) / n_d3_rss;

% 对数据进行排序
sorted_d4_rss = sort(d4_rss);

% 计算每个值的累积概率
n_d4_rss = length(sorted_d4_rss);
cumulative_d4_rss = (1:n_d4_rss) / n_d4_rss;




%绘制 CDF
%figure(1);
%plot(sorted_d2_rss, cumulative_d2_rss, 'LineWidth', 2);
%grid on;
%xlabel('Value');
%ylabel('Cumulative Probability');
%title('Cumulative Distribution Function (CDF)');

%绘制 CDF
figure(2);
plot(sorted_d3_rss, cumulative_d3_rss, 'LineWidth', 2);
grid on;
xlabel('定位误差/m');
ylabel('累计概率');
title('Cumulative Distribution Function (CDF)');

%绘制 CDF
%figure(3);
%plot(sorted_d4_rss, cumulative_d4_rss, 'LineWidth', 2);
%grid on;
%xlabel('Value');
%ylabel('Cumulative Probability');
%title('Cumulative Distribution Function (CDF)');

%%判断一下每个测试指纹被定位到房间的精度

