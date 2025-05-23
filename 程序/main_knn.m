%主程序 main
clear all;
clear all;
%离线指纹数据--------------------
load("RSS.mat","RSS");
load("LOC.mat","LOC");
load("testrss.mat","testrss");
load("testloc.mat","testloc");

RSS=RSS;
LOC=LOC;

rss=testrss(1,:);
loc=testloc(1,:);


FP1=[LOC RSS];



%------单纯的KNN
[L2,p2]=knn1(rss,FP1,3);
%-----未加特征提取的WKNN
[L3,p3]=KNN(rss,FP1,3);
%-----pca特征提取后的定位---所有算法已经变完。且用到的是改进的KNN算法
[Y1,eigVector1,eigValue1]=PCA_sammid(RSS,4);
FP2=[LOC Y1];
rss1=PCA_sammid_online(rss,RSS,4) %rss为在线样本；
%------仅仅通过PCA后 PCA-wknn未经过定位改进的
[L4,p4]=KNN(rss1,FP2,7);

%--------误差估计----

d2=sqrt(distance(p2,loc));
d3=sqrt(distance(p3,loc));
d4=sqrt(distance(p4,loc));
D=[d2 d3 d4];









