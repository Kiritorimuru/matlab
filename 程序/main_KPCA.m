%% 主程序 main
clear all;
clear all;
%% 离线指纹数据--------------------
load("RSS.mat", "RSS");
load("LOC.mat", "LOC");
load("testrss.mat", "testrss");
load("testloc.mat", "testloc");

RSS = RSS;
LOC = LOC;

rss = testrss(1, :);
loc = testloc(1, :);

%% k-PCA 进行训练样本-------------------
d = 3; % 可以分别修改 %配置扩展后的样本次数
type = 'gaussian'; % 选用高斯核函数 poly simple gaussian
para = 2; % 可以在后边进行修改 进行仿真时用到
[Y, eigVector, eigValue] = kPCA(RSS, d, type, para);

FP = [LOC Y];
FP1 = [LOC RSS];
%% 计算在线的样本 ----------
[y, b] = kpca_online(rss, RSS, d, type, para); % 数据出现错误 因为数据的相近性 在做差的时候不能很好的去除并不能很好的解决，
% end

%% 进行定位改进KPCA_IWKNN进行定位
a = 0.3;
[L, p] = IWKNN(y, FP, a);
%% ----未加特征提取的 IWKNN
[L1, p1] = IWKNN(rss, FP1, a);
%% ------单纯的KNN
[L2, p2] = knn1(rss, FP1, 3);
%% -----未加特征提取的WKNN
[L3, p3] = KNN(rss, FP1, 3);
%% -----pca特征提取后的定位---所有算法已经变完。且用到的是改进的KNN算法
[Y1, eigVector1, eigValue1] = PCA_sammid(RSS, 4);
FP2 = [LOC Y1];
rss1 = PCA_sammid_online(rss, RSS, 4); % rss为在线样本；
%% ------仅仅通过PCA后 PCA-wknn未经过定位改进的
[L4, p4] = KNN(rss1, FP2, 7);

%% --------误差估计----
d = sqrt(distance(p, loc));
d1 = sqrt(distance(p1, loc));
d2 = sqrt(distance(p2, loc));
d3 = sqrt(distance(p3, loc));
d4 = sqrt(distance(p4, loc));
D = [d d1 d2 d3 d4];






