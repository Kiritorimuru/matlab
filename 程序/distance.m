%计算在线样本与训练样本之间的欧式距离 x,y 是一维向量
%copyright lhl 2015.3.23
function d=distance(x,y)
a=x-y;
d=norm(a)^2;