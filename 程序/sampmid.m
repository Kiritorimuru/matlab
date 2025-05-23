%样本中心化 Y为 中心化的样本空间  b空间的均值样本
function [Y , b] = sampmid(X)
N=size(X,1);
b=sum(X,1)./N;
A=repmat(b,N,1);
Y=X-A;
