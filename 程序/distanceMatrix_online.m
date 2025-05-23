%在在现阶段 将在线样本映射的高维空间时 先求出K0 协方差矩阵 Xt is a line vector;X is a M-N matrix; D
%is a column vector;
%copyright:lhl 2005.3.23
function D=distanceMatrix_online(Xt,X)
N=size(X,1);
m=sum(Xt.*Xt,2);
mm=repmat(m,N,1);
nn=sum(X.*X,2);
D1=mm+nn-2*(X*Xt');
D=sqrt(D1);