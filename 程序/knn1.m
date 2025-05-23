%knn算法 参数平均
function  [L,p]=knn(xt,FP,k)
N=size(FP,1);
for i=1:N
    dg(i)=sqrt(distance(xt,FP(i,3:end))); %sqrt dg是G对应的相应的欧氏距离，已经被开方了
end
dg1=sort(dg);      %the N-N算法的话 用min(dg1) index=find(dg==dg1) l= G（index,1:2）
dg3=1/k;
n1=k; %a %n1 是前n个最大的数 共n1个近邻坐标  $K-NN K 直接赋值即可
dg2=dg1(1:n1); %dg2为前n1个最小的欧氏距离
index=zeros(1,n1);
for j=1:n1
    index(j)=find(dg==dg2(j));
    L(j,:)=FP(index(j),1:2);
end
p=dg3*sum(L);