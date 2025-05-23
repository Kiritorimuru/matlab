%PCA 经典算法的 在线样本的提取映射 y1为在线样本 ，x为样本空间（簇首）
function y=PCA_sammid_online(y1,x,k)
[Y,eigVector,eigValue]=PCA_sammid(x,k);
[Y1,b] = sampmid(x);
y2=y1-b;
y=y2*eigVector;