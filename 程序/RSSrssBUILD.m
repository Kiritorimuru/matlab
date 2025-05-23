clear 
%-----1.生成3.9米*6米老人房的位置数据（包括一个楼梯、一个工人房区域、厕所门前区域等）
%%-------1.1生成12个单数房间和楼梯、厕所前区域采集点位置数据，
for i=1:12
for j=1:5
for k=1:3
FP_F2_XY_single0{1,i}(j,k)=6+3.9*(12-i)+(3.9/4)*k;
FP_F2_XY_single0{1,i}(j,k+4)=6+2.7+(6/6)*j;
end
end
end
%%---1.2将以上数据，放在元胞数组中，每个房间的位置数据为元胞数组的一个元素，每个元胞数组元素都是2列数据，第一列为采集点的x坐标值，第二列为采集点的y坐标值，第三列为房间号，楼梯区域和厕所前区域也进行编号。209为楼梯，224为楼梯，223为厕所前区域。225为厕所。
home_single_n=201:2:226;
for i=1:12
for j=1:5
for k=1:3
FP_F2_XY_single1{1,i}((5*(k-1)+j),1)=FP_F2_XY_single0{1,i}(j,k);
FP_F2_XY_single1{1,i}((5*(k-1)+j),2)=FP_F2_XY_single0{1,i}(j,k+4);
FP_F2_XY_single1{1,i}((5*(k-1)+j),3)=home_single_n(i);
end
end
end
%%---1.3生成12个双数房间和楼梯、工人房采集点位置数据，
home_double_n=202:2:226;
for i=1:12
for j=1:5
for k=1:3
FP_F2_XY_double0{1,i}(j,k)=6+3.9*(12-i)+(3.9/4)*k;
FP_F2_XY_double0{1,i}(j,k+4)=(6/6)*j;
end
end
end
for i=1:12
for j=1:5
for k=1:3
FP_F2_XY_double1{1,i}((5*(k-1)+j),1)=FP_F2_XY_double0{1,i}(j,k);
FP_F2_XY_double1{1,i}((5*(k-1)+j),2)=FP_F2_XY_double0{1,i}(j,k+4);
FP_F2_XY_double1{1,i}((5*(k-1)+j),3)=home_double_n(i);
end
end
end
%%-------1.4生成厕所和活动室内采集点位置数据
home_WC_ACT_n=[226,225];
for i=1:2
for j=1:5
for k=1:5
FP_F2_XY_WC_ACT0{1,i}(j,k)=(6/6)*k;
FP_F2_XY_WC_ACT0{1,i}(j,k+7)=(6+2.7)*(i-1)+(6/6)*j;
end
end
end
for i=1:2
for j=1:5
for k=1:5
FP_F2_XY_WC_ACT1{1,i}((5*(k-1)+j),1)=FP_F2_XY_WC_ACT0{1,i}(j,k);
FP_F2_XY_WC_ACT1{1,i}((5*(k-1)+j),2)=FP_F2_XY_WC_ACT0{1,i}(j,k+7);
FP_F2_XY_WC_ACT1{1,i}((5*(k-1)+j),3)=home_WC_ACT_n(i);
end
end
end

%%------1.5生成走廊区域的位置数据
L=6+3.9*12;
FP_F2_XY_hallway_halfn=size(1:1:L,2);
for i=1:2
for j=1:FP_F2_XY_hallway_halfn
FP_F2_XY_hallway0(FP_F2_XY_hallway_halfn*(i-1)+j,1)=j;
FP_F2_XY_hallway0(FP_F2_XY_hallway_halfn*(i-1)+j,2)=6+(2.7/3)*i;
end
end

%%------1.6把所有的位置数据放在一起
FP_F2_XY_single2=cell2mat(FP_F2_XY_single1);%mm=cat(1,FP_F2_XY_single1{:});
FP_F2_XY_double2=cell2mat(FP_F2_XY_double1);
FP_F2_XY_WC_ACT2=cell2mat(FP_F2_XY_WC_ACT1);



FP_F2_XY0=[FP_F2_XY_single2;FP_F2_XY_double2];

for i=1:size(FP_F2_XY0,1)
for k=1:3
for j=(size(FP_F2_XY0,2)./3):-1:1
FP_F2_XY1(size(FP_F2_XY0,1)*((size(FP_F2_XY0,2)./3)-j)+i,k)=FP_F2_XY0(i,3*((size(FP_F2_XY0,2)./3)-j)+k);
end
end
end

n1_FP_F2_XY_WC_ACT2=size(FP_F2_XY_WC_ACT2,1);
n2_FP_F2_XY_WC_ACT2=size(FP_F2_XY_WC_ACT2,2)./3;
for i=1:n1_FP_F2_XY_WC_ACT2
for k=1:3
for j=n2_FP_F2_XY_WC_ACT2:-1:1
FP_F2_XY2(n1_FP_F2_XY_WC_ACT2*((n2_FP_F2_XY_WC_ACT2)-j)+i,k)=FP_F2_XY_WC_ACT2(i,3*(n2_FP_F2_XY_WC_ACT2-j)+k);
end
end
end

FP_F2_XY_hallway0(:,3)=200;
FP_F2_XY3=[FP_F2_XY1;FP_F2_XY2;FP_F2_XY_hallway0];

%%-----生成第二层的采集点的位置数据，采集点的高度选择距二楼楼板高1米处。
FP_F2_XY(:,1)=FP_F2_XY3(:,1);
FP_F2_XY(:,2)=FP_F2_XY3(:,2);
FP_F2_XY(:,3)=3.6+1;
FP_F2_XY(:,4)=FP_F2_XY3(:,3);

%%------1.6生成无线AP的位置数据（走廊棚顶部署4个无线AP）

w=6+2.7+6;%楼宽
APw=w/2-1;
FP_F2_APxy=[6+3.9,APw,6.9,1;6+3.9*4,APw,6.9,2; 6+3.9*7,APw,6.9,3;6+3.9*10,APw,6.9,4];

%(3)确定每个位置点距离每个AP的墙壁数量
%--每个房间的四个定点位置
%%--单数房间的四个顶点
 for i=1:12
singleding_xy0{i}(1,1)=6+3.9*(12-i);
singleding_xy0{i}(2,1)=6+3.9*(12-i+1);
singleding_xy0{i}(3,1)=6+2.7;
singleding_xy0{i}(4,1)=6+2.7+6;
end
singleding_xy0{13}(1,1)=0;
singleding_xy0{13}(2,1)=6;
singleding_xy0{13}(3,1)=6+2.7;
singleding_xy0{13}(4,1)=6+2.7+6;
%%--偶数房间的四个顶点
 for i=1:12
doubleding_xy0{i}(1,1)=6+3.9*(12-i);
doubleding_xy0{i}(2,1)=6+3.9*(12-i+1);
doubleding_xy0{i}(3,1)=0;
doubleding_xy0{i}(4,1)=6;
end
doubleding_xy0{13}(1,1)=0;
doubleding_xy0{13}(2,1)=6;
doubleding_xy0{13}(3,1)=0;
doubleding_xy0{13}(4,1)=6;
%%--顶点的储存方式是从左上角顶点顺时针到左下角顶点
for i=1:13
singleding_xy1{i}(1,1)=singleding_xy0{i}(1,1);
singleding_xy1{i}(1,2)=singleding_xy0{i}(3,1);
singleding_xy1{i}(2,1)=singleding_xy0{i}(2,1);
singleding_xy1{i}(2,2)=singleding_xy0{i}(3,1);
singleding_xy1{i}(3,1)=singleding_xy0{i}(2,1);
singleding_xy1{i}(3,2)=singleding_xy0{i}(4,1);
singleding_xy1{i}(4,1)=singleding_xy0{i}(1,1);
singleding_xy1{i}(4,2)=singleding_xy0{i}(4,1);
end

for i=1:13
doubleding_xy1{i}(1,1)=doubleding_xy0{i}(1,1);
doubleding_xy1{i}(1,2)=doubleding_xy0{i}(4,1);
doubleding_xy1{i}(2,1)=doubleding_xy0{i}(2,1);
doubleding_xy1{i}(2,2)=doubleding_xy0{i}(4,1);
doubleding_xy1{i}(3,1)=doubleding_xy0{i}(2,1);
doubleding_xy1{i}(3,2)=doubleding_xy0{i}(3,1);
doubleding_xy1{i}(4,1)=doubleding_xy0{i}(1,1);
doubleding_xy1{i}(4,2)=doubleding_xy0{i}(3,1);
end
%%---计算四个顶点与AP点坐标的直线斜率
for i=1:13
for j=1:4
for k=1:4
singleding_xy1{i}(j,2+k)=(singleding_xy1{i}(j,2)-FP_F2_APxy(k,2))./(singleding_xy1{i}(j,1)-FP_F2_APxy(k,1));
end
end
end
for i=1:13
for j=1:4
for k=1:4
doubleding_xy1{i}(j,2+k)=(doubleding_xy1{i}(j,2)-FP_F2_APxy(k,2))./(doubleding_xy1{i}(j,1)-FP_F2_APxy(k,1));
end
end
end
%%---计算所有点与AP点坐标的直线斜率
FP_F2_XY_slop=FP_F2_XY;
n_FP_F2_XY=size(FP_F2_XY,1);
for i=1:n_FP_F2_XY
for j=1:4
FP_F2_XY_slop(i,4+j)=(FP_F2_XY_slop(i,2)-FP_F2_APxy(j,2))./(FP_F2_XY_slop(i,1)-FP_F2_APxy(j,1));
end
end
%%---判断每个点到AP间的墙体数量

for i=1:13
n_slop0{i}=isinf(doubleding_xy1{i});%判断斜率是否为无穷，为无穷时，所在位置为1
end

for i=1:13
sum_n_slop0(i)=sum(n_slop0{i}(:));%所有元素之和，若都为0，说明没有斜率为无穷的情况
end
n_0=sum(sum_n_slop0(:)>0);%sum_n_slop0中元素大于0的个数，斜率为无穷的情况的房间个数
n_slop_inf0=find(sum_n_slop0>0);%sum_n_slop0中元素大于0的位置，斜率为无穷的情况的房间位置

%%---先找有些特殊的房间，对于某个AP来说，所有的点都是经过墙的数量为1.
for i=1:13
n_slop_inf1{i}=find(n_slop0{i}>0);%为了确定哪个AP对哪个房间是斜率为无穷，对于一个房间，哪个AP斜率是无穷的，得到的是序列
[row_indices1{i}, col_indices1{i}] = ind2sub(size(n_slop0{i}), n_slop_inf1{i});%将上面的序列变成，行列的形式。
end

%---因为单数房间和双数房间是对称的，所以穿墙壁个数为1的房间也是对称的。
single_room=201:2:225;
double_room=202:2:226;
n_wall1_single_room=single_room(n_slop_inf0);
n_wall1_double_room=double_room(n_slop_inf0);

for i=1:n_0
n_FP_F2_XY_double_wall1 = find( FP_F2_XY(:,4)== n_wall1_double_room(i));
FP_F2_XY(find( FP_F2_XY(:,4)== n_wall1_double_room(i)),4+col_indices1{n_slop_inf0(i)}(1,1)-2)=1;
end

for i=1:n_0
n_FP_F2_XY_double_wall1 = find( FP_F2_XY(:,4)== n_wall1_single_room(i));
FP_F2_XY(find( FP_F2_XY(:,4)== n_wall1_single_room(i)),4+col_indices1{n_slop_inf0(i)}(1,1)-2)=1;
end

%%---判断每个AP距离每个房间最多间距几堵墙

for i=1:12
for j=1:4
single_n_wall_max0{i}(j,1)=abs(FP_F2_APxy(j,1)-max(singleding_xy1{i}(:,1)))./3.9;
single_n_wall_max0{i}(j,2)=abs(FP_F2_APxy(j,1)-min(singleding_xy1{i}(:,1)))./3.9;
single_n_wall_max1(i,j)=max(single_n_wall_max0{i}(j,:));
end
end
for j=1:4
single_n_wall_max1(13,j)=abs(FP_F2_APxy(j,1)-max(singleding_xy1{13}(:,1)))./3.9+1;
end

for i=1:12
for j=1:4
double_n_wall_max0{i}(j,1)=abs(FP_F2_APxy(j,1)-max(doubleding_xy1{i}(:,1)))./3.9;
double_n_wall_max0{i}(j,2)=abs(FP_F2_APxy(j,1)-min(doubleding_xy1{i}(:,1)))./3.9;
double_n_wall_max1(i,j)=max(double_n_wall_max0{i}(j,:));
end
end
for j=1:4
double_n_wall_max1(13,j)=abs(FP_F2_APxy(j,1)-max(doubleding_xy1{13}(:,1)))./3.9+1;
end

%单数房间
%for i=1:13%每个房间
%for j=1:4%每个AP
%single_k0{i}(j,:)=singleding_xy1{i}(:,2+j);
%end
%end

for i=1:13%每个房间
for j=1:4%每个AP
single_k0{i,j}=singleding_xy1{i}(:,2+j);%每个房间顶点的AP的斜率
end
end

for i=1:13%每个房间
for j=1:4%每个AP
double_k0{i,j}=doubleding_xy1{i}(:,2+j);%每个房间顶点的AP的斜率
end
end

for i=1:13%每个房间
for j=1:4%每个AP
if single_n_wall_max1(i,j)>2
n00(i,j)=round(single_n_wall_max1(i,j)-2);%所需要的额外顶点数
else
n00(i,j)=0;
end
end
end

for i=1:13%每个房间
for j=1:4%每个AP
if double_n_wall_max1(i,j)>2
n00_double(i,j)=round(double_n_wall_max1(i,j)-2);%所需要的额外顶点数
else
n00_double(i,j)=0;
end
end
end

%%---判断所需额外点数在AP的左侧还是右侧,将判断位置点距AP的墙数所需要的斜率放在一起
for i=1:13%每个房间
for j=1:4%每个AP
for k=1:n00(i,j)
if singleding_xy1{i}(1,1)>FP_F2_APxy(j,1)
single_k0{i,j}(4+k,1)=singleding_xy1{i+k}(1,j+2);
else 
single_k0{i,j}(4+k,1)=singleding_xy1{i-k}(2,j+2);%%%%
end
end
end
end
single_k00=single_k0;

for i=1:13%每个房间
for j=1:4%每个AP
for k=1:n00_double(i,j)
if doubleding_xy1{i}(1,1)>FP_F2_APxy(j,1)
double_k0{i,j}(4+k,1)=doubleding_xy1{i+k}(1,j+2);
else 
double_k0{i,j}(4+k,1)=doubleding_xy1{i-k}(2,j+2);%%%%
end
end
end
end
double_k00=double_k0;

for i=1:13%每个房间
for j=1:4%每个AP
if singleding_xy1{i}(1,1)>FP_F2_APxy(j,1)
single_k0{i,j}=[single_k00{i,j}(1:2);single_k00{i,j}(4:end)];%删除第三个元素
else
single_k0{i,j}=[single_k00{i,j}(1:3);single_k00{i,j}(5:end)];%删除第四个元素%
end
end
end

for i=1:13%每个房间
for j=1:4%每个AP
if doubleding_xy1{i}(1,1)>FP_F2_APxy(j,1)
double_k0{i,j}=[double_k00{i,j}(1:2);double_k00{i,j}(4:end)];%删除第三个元素
else
double_k0{i,j}=[double_k00{i,j}(1:3);double_k00{i,j}(5:end)];%删除第四个元素%
end
end
end

single_k000=single_k0;
%删除一些无用的斜率，即大于顶点的斜率
for i=1:13
for j=1:4
shan_single_n_k{i,j}=find(abs(single_k0{i,j})>max(abs(single_k0{i,j}(1:3))));
end
end
%剩余都是有用的斜率
for i=1:13
for j=1:4
single_k0{i,j}(shan_single_n_k{i,j})=[];
end
end
for i=1:13
for j=1:4
sort_single_k0{i,j}=sort(abs(single_k0{i,j}));
end
end

double_k000=double_k0;
%删除一些无用的斜率，即大于顶点的斜率
for i=1:13
for j=1:4
shan_double_n_k{i,j}=find(abs(double_k0{i,j})>max(abs(double_k0{i,j}(1:3))));
end
end
%剩余都是有用的斜率
for i=1:13
for j=1:4
double_k0{i,j}(shan_double_n_k{i,j})=[];
end
end
for i=1:13
for j=1:4
sort_double_k0{i,j}=sort(abs(double_k0{i,j}));%取正之后，正序排列
end
end

%%---判断位置点到AP间的墙壁数量

%单数房间的位置点与AP的斜率
FP_F2_XY_single1{1,13}=FP_F2_XY_WC_ACT1{1,2};
for i=1:13
n_FP_F2_XY_single1(1,i)=size(FP_F2_XY_single1{1,i},1);
for l=1:n_FP_F2_XY_single1(1,i)
for j=1:4
FP_F2_XY_single1{1,i}(l,4+j)=(FP_F2_XY_single1{1,i}(l,2)-FP_F2_APxy(j,2))./(FP_F2_XY_single1{1,i}(l,1)-FP_F2_APxy(j,1));
end
end
end
%双数房间的位置点与AP的斜率
FP_F2_XY_double1{1,13}=FP_F2_XY_WC_ACT1{1,1};
for i=1:13
n_FP_F2_XY_double1(1,i)=size(FP_F2_XY_double1{1,i},1);
for l=1:n_FP_F2_XY_double1(1,i)
for j=1:4
FP_F2_XY_double1{1,i}(l,4+j)=(FP_F2_XY_double1{1,i}(l,2)-FP_F2_APxy(j,2))./(FP_F2_XY_double1{1,i}(l,1)-FP_F2_APxy(j,1));
end
end
end


%判断每个房间的位置点的斜率与重要斜率之间的关系
%把斜率都变成正数
for i=1:13
absFP_F2_XY_single1{1,i}=abs(FP_F2_XY_single1{1,i});
end

for i=1:13
absFP_F2_XY_double1{1,i}=abs(FP_F2_XY_double1{1,i});
end

%%单数房间
for i=1:13
n0_FP_F2_XY_single1(i)=size(FP_F2_XY_single1{1,i},1);
for j=1:n0_FP_F2_XY_single1(i)
for k=1:4
idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
idx_upper = size(sort_single_k0{i,k},1) +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
for p = 1:size(sort_single_k0{i,k},1)
    if sort_single_k0{i,k}(p,1) > absFP_F2_XY_single1{1,i}(j,4+k)
        idx_upper =p; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_single_k0{i,k}(p,1) < absFP_F2_XY_single1{1,i}(j,4+k)
        idx_lower= p; % 更新下界索引
end
FP_F2_XY_single1{1,i}(j,8+k)=idx_lower;
end
end
end
end


%%双数房间
for i=1:13
n0_FP_F2_XY_double1(i)=size(FP_F2_XY_double1{1,i},1);
for j=1:n0_FP_F2_XY_double1(i)
for k=1:4
idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
idx_upper = size(sort_double_k0{i,k},1) +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
for p = 1:size(sort_double_k0{i,k},1)
    if sort_double_k0{i,k}(p,1) > absFP_F2_XY_double1{1,i}(j,4+k)
        idx_upper =p; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_double_k0{i,k}(p,1) < absFP_F2_XY_double1{1,i}(j,4+k)
        idx_lower= p; % 更新下界索引
end
FP_F2_XY_double1{1,i}(j,8+k)=idx_lower;
end
end
end
end
%-----根据模型生成指纹
%--每个采集点与AP间的距离
for i=1:13
for j=1:4
for k=1:n0_FP_F2_XY_single1(i)
FP_F2_XY_single1{1,i}(k,13+j)=sqrt((FP_F2_XY_single1{1,i}(k,1)-FP_F2_APxy(j,1)).^2+(FP_F2_XY_single1{1,i}(k,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);
end
end
end

for i=1:13
for j=1:4
for k=1:n0_FP_F2_XY_double1(i)
FP_F2_XY_double1{1,i}(k,13+j)=sqrt((FP_F2_XY_double1{1,i}(k,1)-FP_F2_APxy(j,1)).^2+(FP_F2_XY_double1{1,i}(k,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);
end
end
end
%--走廊处位置点距离各AP的距离
n0_FP_F2_XY_hallway0=size(FP_F2_XY_hallway0,1);
for i=1:n0_FP_F2_XY_hallway0
for j=1:4
FP_F2_XY_hallway0(i,13+j)=sqrt((FP_F2_XY_hallway0(i,1)-FP_F2_APxy(j,1)).^2+(FP_F2_XY_hallway0(i,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);
end
end


%--根据公式生成指纹
for i=1:13
for j=1:4
for k=1:n0_FP_F2_XY_double1
FP_F2_XY_double1{1,i}(k,17+j)=20-40.2-20.*log10(FP_F2_XY_double1{1,i}(k,13+j))-6.9*FP_F2_XY_double1{1,i}(k,8+j);
end
end
end

for i=1:13
for j=1:4
for k=1:n0_FP_F2_XY_single1
FP_F2_XY_single1{1,i}(k,17+j)=20-40.2-20.*log10(FP_F2_XY_single1{1,i}(k,13+j))-6.9*FP_F2_XY_single1{1,i}(k,8+j);
end
end
end

%--生成走廊里的指纹数据
for i=1:n0_FP_F2_XY_hallway0
for j=1:4
FP_F2_XY_hallway0(i,17+j)=20-40.2-20.*log10(FP_F2_XY_hallway0(i,13+j))-6.9*0;
end
end

%将所有生成的指纹数据放在一起
FP_F2_XY=[FP_F2_XY_hallway0;FP_F2_XY_single1{1,1};FP_F2_XY_single1{1,2};FP_F2_XY_single1{1,3};FP_F2_XY_single1{1,4};FP_F2_XY_single1{1,5};FP_F2_XY_single1{1,6};FP_F2_XY_single1{1,7};FP_F2_XY_single1{1,8};FP_F2_XY_single1{1,9};FP_F2_XY_single1{1,10};FP_F2_XY_single1{1,11};FP_F2_XY_single1{1,12};FP_F2_XY_single1{1,13}];
FP_F2_XY=[FP_F2_XY;FP_F2_XY_double1{1,1};FP_F2_XY_double1{1,2};FP_F2_XY_double1{1,3};FP_F2_XY_double1{1,4};FP_F2_XY_double1{1,5};FP_F2_XY_double1{1,6};FP_F2_XY_double1{1,7};FP_F2_XY_double1{1,8};FP_F2_XY_double1{1,9};FP_F2_XY_double1{1,10};FP_F2_XY_double1{1,11};FP_F2_XY_double1{1,12};FP_F2_XY_double1{1,13}];

%生成测试指纹
%每个房间生成位置数据
%--生成每个房间的位置范围

for i=1:13
fanwei_x0(i)=6+3.9*(12-i+1);
end
fanwei_y=[0,6,6+2.7,6+2.7+6];
fanwei_x=[fanwei_x0,0];
n_fanwei_x=size(fanwei_x,2);
n_fanwei_y=size(fanwei_y,2);
sort_fanwei_x=sort(fanwei_x, 'descend');
sort_fanwei_y=sort(fanwei_y);
%--在指定范围内生成任意数，每个房间20个个测试指纹点
x_fanwei0=1;
x_fanwei1=52;
y_fanwei0=1;
y_fanwei1=14;
%单数房间
s_test_n=20;
s_num_test_FP_xy=1:2:26;
for i=1:13
for j=1:n_fanwei_x
s_test_FP_xy{i}(:,1)=sort_fanwei_x(i+1)+(sort_fanwei_x(i)-sort_fanwei_x(i+1))* rand(1, s_test_n);

end
s_test_FP_xy{i}(:,2)=sort_fanwei_y(3)+(sort_fanwei_y(4)-sort_fanwei_y(3))* rand(1, s_test_n);
end
for i=1:13
 for j=1:s_test_n   
s_test_FP_xy{i}(j,3)=200+s_num_test_FP_xy(i);
 end
end


%双数房间
d_test_n=20;
d_num_test_FP_xy=2:2:26;
for i=1:13
for j=1:n_fanwei_x
d_test_FP_xy{i}(:,1)=sort_fanwei_x(i+1)+(sort_fanwei_x(i)-sort_fanwei_x(i+1))* rand(1, d_test_n);
end
d_test_FP_xy{i}(:,2)=sort_fanwei_y(1)+(sort_fanwei_y(2)-sort_fanwei_y(1))* rand(1, d_test_n);
end

for i=1:13
 for j=1:d_test_n 
d_test_FP_xy{i}(j,3)=200+d_num_test_FP_xy(i);
 end
end

%走廊
h_test_n=100;
h_test_FP_xy(:,1)=sort_fanwei_x(1)+(sort_fanwei_x(14)-sort_fanwei_x(1))* rand(1, h_test_n);
h_test_FP_xy(:,2)=sort_fanwei_y(1)+(sort_fanwei_y(4)-sort_fanwei_y(1))* rand(1, h_test_n);

%%每个房间的位置数据生成与AP的斜率
%单数房间

for i=1:13
for j=1: s_test_n
for k=1:4
s_test_FP_xy{i}(j,4+k)=(s_test_FP_xy{i}(j,2)-FP_F2_APxy(k,2))./(s_test_FP_xy{i}(j,1)-FP_F2_APxy(k,1));
end
end
end

%双数房间
for i=1:13
for j=1: d_test_n
for k=1:4
d_test_FP_xy{i}(j,4+k)=(d_test_FP_xy{i}(j,2)-FP_F2_APxy(k,2))./(d_test_FP_xy{i}(j,1)-FP_F2_APxy(k,1));
end
end
end


%走廊
for j=1: h_test_n
for k=1:4
h_test_FP_xy(j,4+k)=(h_test_FP_xy(j,2)-FP_F2_APxy(k,2))./(h_test_FP_xy(j,1)-FP_F2_APxy(k,1));
end
end

%判断每个位置距AP的墙壁数
%把斜率都变成正数
%单数房间
for i=1:13
abss_test_FP_xy{1,i}=abs(s_test_FP_xy{1,i});
end
%双数房间
for i=1:13
absd_test_FP_xy{1,i}=abs(d_test_FP_xy{1,i});
end

%判断房间内测试位置到ap的斜率与重要点到ap的斜率之间的关系
%%单数房间
for i=1:13
for j=1:s_test_n
for k=1:4
s_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
s_test_idx_upper = size(sort_single_k0{i,k},1) +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
for s_test_p = 1:size(sort_single_k0{i,k},1)
    if sort_single_k0{i,k}(s_test_p,1) > abss_test_FP_xy{1,i}(j,4+k)
        s_test_idx_upper =s_test_p; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_single_k0{i,k}(s_test_p,1) <abss_test_FP_xy{1,i}(j,4+k)
        s_test_idx_lower= s_test_p; % 更新下界索引
end

end
s_test_FP_xy{1,i}(j,8+k)=s_test_idx_lower;
end
end
end
%%双数房间
for i=1:13
for j=1:d_test_n
for k=1:4
d_test_idx_lower= 0; % 下界索引，初始化为0表示x小于向量中的任何元素
d_test_idx_upper = size(sort_single_k0{i,k},1) +1; % 上界索引，初始化为向量长度+1表示x大于向量中的任何元素
% 在向量中搜索x应该插入的位置
for d_test_p = 1:size(sort_single_k0{i,k},1)
    if sort_single_k0{i,k}(d_test_p,1) > absd_test_FP_xy{1,i}(j,4+k)
        d_test_idx_upper =s_test_p; % 更新上界索引
        break; % 退出循环，因为x不可能再大于后面的元素了
    elseif sort_single_k0{i,k}(d_test_p,1) <absd_test_FP_xy{1,i}(j,4+k)
        d_test_idx_lower= d_test_p; % 更新下界索引
end
end
d_test_FP_xy{1,i}(j,8+k)=d_test_idx_lower;
end
end
end

%计算位置指纹与AP的距离
%单数房间
for i=1:13
for j=1:4
for k=1:s_test_n
s_test_FP_xy{1,i}(k,13+j)=sqrt((s_test_FP_xy{1,i}(k,1)-FP_F2_APxy(j,1)).^2+(s_test_FP_xy{1,i}(k,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);%AP是吸顶式，所以高为10.2，测试指纹选择距本楼层1米高处
end
end
end

%双数房间
for i=1:13
for j=1:4
for k=1:d_test_n
d_test_FP_xy{1,i}(k,13+j)=sqrt((d_test_FP_xy{1,i}(k,1)-FP_F2_APxy(j,1)).^2+(d_test_FP_xy{1,i}(k,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);%AP是吸顶式，所以高为10.2，测试指纹选择距本楼层1米高处
end
end
end

%走廊
for i=1:h_test_n
for j=1:4
h_test_FP_xy(i,13+j)=sqrt((h_test_FP_xy(i,1)-FP_F2_APxy(j,1)).^2+(h_test_FP_xy(i,2)-FP_F2_APxy(j,2)).^2+(7.9-10.2).^2);
end
end
%生成测试指纹
%单数房间
for i=1:13
for j=1:4
for k=1:s_test_n
s_test_FP_xy{1,i}(k,17+j)=20-40.2-20.*log10(s_test_FP_xy{1,i}(k,13+j))-6.9*s_test_FP_xy{1,i}(k,8+j);
end
end
end

%双数房间
for i=1:13
for j=1:4
for k=1:d_test_n
d_test_FP_xy{1,i}(k,17+j)=20-40.2-20.*log10(d_test_FP_xy{1,i}(k,13+j))-6.9*d_test_FP_xy{1,i}(k,8+j);
end
end
end
%走廊 信号穿的墙壁数量为0
for i=1:h_test_n
for j=1:4
h_test_FP_xy(i,17+j)=20-40.2-20.*log10(h_test_FP_xy(i,13+j))-6.9*0;
h_test_FP_xy(i,3)=200;
end
end

%%将所有的测试指纹数据放在一起
s_test_allFP_xy=[s_test_FP_xy{1,1};s_test_FP_xy{1,2};s_test_FP_xy{1,3};s_test_FP_xy{1,4};s_test_FP_xy{1,5};s_test_FP_xy{1,6};s_test_FP_xy{1,7};s_test_FP_xy{1,8};s_test_FP_xy{1,9};s_test_FP_xy{1,10};s_test_FP_xy{1,11};s_test_FP_xy{1,12};s_test_FP_xy{1,13};];
d_test_allFP_xy=[d_test_FP_xy{1,1};d_test_FP_xy{1,2};d_test_FP_xy{1,3};d_test_FP_xy{1,4};d_test_FP_xy{1,5};d_test_FP_xy{1,6};d_test_FP_xy{1,7};d_test_FP_xy{1,8};d_test_FP_xy{1,9};d_test_FP_xy{1,10};d_test_FP_xy{1,11};d_test_FP_xy{1,12};d_test_FP_xy{1,13};];

test_allFP_xy=[s_test_allFP_xy;d_test_allFP_xy;h_test_FP_xy];

RSS=[FP_F2_XY(:,18:21)];%指纹数据库
testrss=[test_allFP_xy(:,18:21)];%测试指纹
LOC=[FP_F2_XY(:,1:2)];%指纹数据库指纹的位置
testloc=[test_allFP_xy(:,1:2)];%测试指纹的位置
save('RSS.mat', 'RSS');
csvwrite('RSS.csv', RSS);

save('testrss.mat','testrss');
csvwrite('testrss.csv',testrss);
save('LOC.mat', 'LOC');
csvwrite('LOC.csv', LOC);
save('testloc.mat', 'testloc');
csvwrite('testloc.csv', testloc);
save('test_allFP_xy.mat', 'test_allFP_xy');
csvwrite('test_allFP_xy.csv', test_allFP_xy);
