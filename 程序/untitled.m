function [outputArg1,outputArg2] = NUMroom(s_num_test_FP_xy,d_num_test_FP_xy,n_fanwei_x,fanwei_y,)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
outputArg1 = inputArg1;
outputArg2 = inputArg2;


%判断测试指纹得到的结果是在哪个房间

s_num_test_FP_xy=1:2:26;
d_num_test_FP_xy=2:2:26;
for i=1:n_fanwei_x
p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_x +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
    if n_fanwei_x(i,1) > p2(1)
        p_test_idx_upper =i; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif n_fanwei_x(i,1) <p2(1)
        p_test_idx_lower=i; % 更新下界索引
    end
end

p_test_x0=13-p_test_idx_lower+1;

for i=1:n_fanwei_y
p_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
p_test_idx_upper = n_fanwei_y +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
    if n_fanwei_y(i,1) > p2(2)
        p_test_idx_upper =i; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif n_fanwei_y(i,1) <p2(2)
        p_test_idx_lower=i; % 更新下界索引
    end
end
p_test_y0=p_test_idx_lower;

if p_test_y0==1
    P2_rss{i}(1,3)=200+d_num_test_FP_xy(p_test_x0);
elseif p_test_y0==2
    P2_rss{i}(1,3)=200;
   elseif p_test_y0==3
    P2_rss{i}(1,3)=200+s_num_test_FP_xy(p_test_x0); 
end














end