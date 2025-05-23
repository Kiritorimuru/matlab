%求在线的pca映射后的样本 x输入样本 y为样本空间  k为降到的维数
%在对样本进行和提取之前进行去中心化
function [y,eigVector,eigValue]=PCA_sammid(x,k)
[X,b] = sampmid(x);
Sx=cov(X);
[V,D]=eig(Sx);
eigValuee=diag(D);
[eigValue,IX]=sort(eigValuee,'descend');
eigVector=V(:,IX);

%% normailization
norm_eigVector=sqrt(sum(eigVector.^2));
eigVector=eigVector./repmat(norm_eigVector,size(eigVector,1),1);

%% dimensionality reduction
eigVector=eigVector(:,1:k);
y=X*eigVector;
