%   X: data matrix, each row is one observation, each column is one feature
%   d: reduced dimension

function [Y, eigVector, eigValue]=kPCA(X,d,type,para)

%% check input
if ( strcmp(type,'simple') || strcmp(type,'poly') || ...
        strcmp(type,'gaussian') ) == 0
    Y=[];
    eigVector=[];
    fprintf(['\nError: Kernel type ' type ' is not supported. \n']);
    return;
end

N=size(X,1);

%% kernel PCA
K0=kernel(X,type,para);
oneN=ones(N,N)/N;
K=K0-oneN*K0-K0*oneN+oneN*K0*oneN;% 对K去中心化


%% eigenvalue analysis
[V,D]=eig(K/N); %K/N是C  这里是求C的特征值特征向量
eigValue=diag(D);%将特征值从特征值对角阵中取出
[G,IX]=sort(eigValue,'descend');% 对特征值向量做降序排列 放入G 同时 特征值所在原向量中的序号放入IX
eigVector=V(:,IX);% 得到对应特征值排列的特征向量矩阵
eigValue=eigValue(IX);%降序排列的特征向量 实际上与G相同

%% normailization
norm_eigVector=sqrt(sum(eigVector.^2));
eigVector=eigVector./repmat(norm_eigVector,size(eigVector,1),1);

%% dimensionality reduction
eigVector=eigVector(:,1:d);
Y=K*eigVector;

