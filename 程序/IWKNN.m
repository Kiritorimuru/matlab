%没有K均值的C_KNN
function  [L,p]=IWKNN(xt,M2_Coordinate_KPCARSS,a)
N=size(M2_Coordinate_KPCARSS,1);
for i=1:N
    dg(i)=sqrt(distance(xt,M2_Coordinate_KPCARSS(i,3:end))); %sqrt dg是G对应的相应的欧氏距离，已经被开方了
    %dg(i)=distEclud(xt,M2_Coordinate_KPCARSS(i,3:end));
end
dg1=sort(dg);      %the N-N算法的话 用min(dg1) index=find(dg==dg1) l= G（index,1:2）
dg3=1./(dg1+0.000000000000000000001);
k=chosenum(dg3,a);
dg4=dg3(1:k);
n1=k; %a %n1 是前n个最大的数 共n1个近邻坐标  $K-NN K 直接赋值即可
dg2=dg1(1:n1); %dg2为前n1个最小的欧氏距离
index=zeros(1,n1);
for j=1:n1
    index(j)=find(dg==dg2(j));
    L(j,:)=M2_Coordinate_KPCARSS(index(j),1:2);%所选K个指纹的坐标
end
s=sum(dg4,2);%所选k个指纹坐标到待测指纹坐标间距离的和
s1=dg4./s;%得到k个指纹坐标的权重
p=s1*L;