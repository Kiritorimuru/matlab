% main.m
clear all;
clc;

% ========== 添加路径 ==========
addpath(genpath('C:\Users\30291\Desktop\Pytorch-Gan-based-dataset-expansion-main/merged_data')); % 合并数据路径
addpath(genpath('functions'));                % 算法函数路径

% ========== 加载数据 ==========
building = 0;   % 目标楼栋
floor = 3;      % 目标楼层

% 1. 加载合并后的训练数据
merged_train_file = sprintf('merged_building_%d_floor_%d.mat', building, floor);
load(merged_train_file, 'RSS', 'LOC');
fprintf('已加载训练数据：%s\n', merged_train_file);

% 2. 加载合并后的测试数据（需提前处理）
merged_test_file = sprintf('merged_test_building_%d_floor_%d.mat', building, floor);
load(merged_test_file, 'RSS_test', 'LOC_test');
fprintf('已加载测试数据：%s\n', merged_test_file);

% 随机选择测试样本
sample_idx = randi(size(RSS_test, 1));
rss = RSS_test(sample_idx, :);
loc = LOC_test(sample_idx, :);

% ========== 数据预处理验证 ==========
% 检查是否存在未处理的100值
if any(RSS(:) == 100) || any(RSS_test(:) == 100)
    error('存在未处理的100值！');
end

% 检查维度一致性
assert(size(RSS, 2) == size(rss, 2), '特征维度不匹配！');

% ========== 核PCA处理 ==========
d = min(3, size(RSS, 2)); % 动态设置降维维度
type = 'gaussian';
para = 2;
[Y, ~, ~] = kPCA(RSS, d, type, para);

% 构建指纹库
FP = [LOC, Y];
FP1 = [LOC, RSS]; % 原始特征指纹库

% ========== 在线定位处理 ==========
[y, ~] = kpca_online(rss, RSS, d, type, para);

% ========== 定位算法 ==========
a = 0.3;
[~, p] = IWKNN(y, FP, a);      % 改进WKNN（核PCA）
[~, p1] = IWKNN(rss, FP1, a);  % 改进WKNN（原始特征）
[~, p2] = knn1(rss, FP1, 3);   % KNN
[~, p3] = KNN(rss, FP1, 3);    % WKNN

% ========== PCA对比 ==========
[Y1, ~, ~] = PCA_sammid(RSS, 4);
FP2 = [LOC, Y1];
rss1 = PCA_sammid_online(rss, RSS, 4);
[~, p4] = KNN(rss1, FP2, 7);   % PCA-WKNN

% ========== 误差计算 ==========
d = sqrt(sum((p - loc).^2));   % 核PCA-IWKNN
d1 = sqrt(sum((p1 - loc).^2)); % 原始IWKNN
d2 = sqrt(sum((p2 - loc).^2)); % KNN
d3 = sqrt(sum((p3 - loc).^2)); % WKNN
d4 = sqrt(sum((p4 - loc).^2)); % PCA-WKNN

D = [d, d1, d2, d3, d4];
disp('定位误差（米）:');
disp(D);







