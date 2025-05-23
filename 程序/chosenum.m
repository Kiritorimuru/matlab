%按照贡献率x提取前P最大个特征值X 为从打到小排列的特征值的向量  
%2015.3.19 
%copyright 李华亮  自主学习
function d=chosenum (X,x)
N=size(X,2);
c=sum(sqrt(X.*X),2);

s=0;
for i=1:N
    b=sqrt((X(:,i))^2);
    s=s+b;
    if (s/c) >= x;
    break;
    end;
    end;
    d=i;