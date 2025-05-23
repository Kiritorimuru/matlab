%需要编写一个将在线样本 映射到高维空间的 一个程序本程序就是
%通过高斯核映射得到 虽然达到降维的可以省略计算时间  但是硬件的快速发展 时间计算复杂度不是问题  准确率更加关键
%映射后 需要对映射后的空间进行k均值分类 Xt 必须是行向量 缺点是 必须每次只能对一个样本进行定位 要对训练后的样本进行 分簇 
function [Y,b]=kpca_online(Xt,X,d,type,para)
N=size(X,1);
K0=kernel(X,type,para);
k0=kernal_online(Xt,X,type,para);
[y, eigVector, eigValue]=kPCA(X,d,type,para);
b=y;
k1=sum(K0,2)./N;
K2=sum(k0',2);
k2=repmat(K2,N,1)./N;
K3=sum((sum(K0))')./N;
k3=repmat(K3,N,1)./N;
k=k0-k1-k2+k3;
Y=(k')*eigVector;
